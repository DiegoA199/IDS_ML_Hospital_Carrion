"""
Persistencia del mejor modelo y artefactos para inferencia sobre tráfico nuevo.

El bundle guardado incluye el estimador entrenado, el ``ColumnTransformer`` ya
ajustado, metadatos de columnas y métricas para reproducir predicciones sin fuga.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src.preprocessing.pipeline import PreparedDataset

ARTIFACTS_DIR = Path("artifacts/models")
DEFAULT_BUNDLE_FILENAME = "idsml_latest_bundle.joblib"


@dataclass
class ModelBundle:
    """
    Artefacto serializable con todo lo necesario para transformar y predecir.

    Attributes
    ----------
    estimator :
        Clasificador sklearn ya entrenado (mismo espacio de features que ``preprocessor``).
    preprocessor :
        ``ColumnTransformer`` ajustado con datos de entrenamiento.
    feature_columns : list[str]
        Columnas de entrada en el orden esperado (sin la columna objetivo).
    target_column : str
        Nombre de la columna objetivo usada en el entrenamiento (referencia).
    target_encoder : LabelEncoder | None
        Codificador de etiquetas si el objetivo era categórico; ``None`` si era numérico.
    model_name : str
        Nombre legible del algoritmo seleccionado.
    f1_score : float
        F1-score (ponderado) obtenido en la comparación al guardar el modelo.
    trained_at : str
        Marca temporal ISO 8601 (UTC) del guardado.
    """

    estimator: Any
    preprocessor: Any
    feature_columns: list[str]
    target_column: str
    target_encoder: LabelEncoder | None
    model_name: str
    f1_score: float
    trained_at: str


def default_bundle_path() -> Path:
    """Ruta por defecto del archivo joblib del último modelo guardado."""
    return ARTIFACTS_DIR / DEFAULT_BUNDLE_FILENAME


def ensure_artifacts_dir() -> Path:
    """Crea ``artifacts/models`` si no existe y devuelve su ruta."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR


def save_model_bundle(
    estimator: Any,
    prepared: PreparedDataset,
    *,
    model_name: str,
    f1_score: float,
    path: Path | str | None = None,
) -> Path:
    """
    Serializa el estimador, preprocesador y metadatos con joblib.

    Parameters
    ----------
    estimator :
        Modelo sklearn entrenado (mejor según F1 en la sesión).
    prepared : PreparedDataset
        Resultado de ``prepare_dataset`` usado para entrenar ese modelo.
    model_name : str
        Etiqueta del modelo (p. ej. ``Random Forest``).
    f1_score : float
        Métrica F1 con la que se seleccionó el modelo.
    path : Path | str | None
        Ruta del archivo ``.joblib``. Si es ``None``, usa ``default_bundle_path()``.

    Returns
    -------
    Path
        Ruta del archivo escrito.
    """
    ensure_artifacts_dir()
    bundle_path = Path(path) if path else default_bundle_path()
    bundle = ModelBundle(
        estimator=estimator,
        preprocessor=prepared.preprocessor,
        feature_columns=list(prepared.feature_columns),
        target_column=prepared.target_column,
        target_encoder=prepared.target_encoder,
        model_name=model_name,
        f1_score=float(f1_score),
        trained_at=datetime.now(timezone.utc).isoformat(),
    )
    joblib.dump(bundle, bundle_path)
    return bundle_path


def load_model_bundle(path: Path | str | None = None) -> ModelBundle:
    """
    Carga un ``ModelBundle`` desde disco.

    Parameters
    ----------
    path : Path | str | None
        Archivo joblib. Si es ``None``, intenta ``default_bundle_path()``.

    Returns
    -------
    ModelBundle
        Bundle listo para ``align_features`` y ``predict_dataframe``.

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    TypeError
        Si el contenido no es un ``ModelBundle``.
    """
    p = Path(path) if path else default_bundle_path()
    if not p.is_file():
        raise FileNotFoundError(f"No existe el bundle de modelo: {p}")
    obj = joblib.load(p)
    if not isinstance(obj, ModelBundle):
        raise TypeError("El archivo joblib no contiene un ModelBundle válido.")
    return obj


def align_features(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    """
    Alinea un DataFrame nuevo al esquema de entrenamiento.

    Las columnas faltantes se rellenan con ``NaN`` (el preprocesador las imputará).
    El orden coincide con ``feature_columns``; las columnas extra del CSV se omiten.

    Parameters
    ----------
    df : pd.DataFrame
        Registros nuevos (sin columna objetivo).
    feature_columns : list[str]
        Lista esperada de nombres de columnas.

    Returns
    -------
    pd.DataFrame
        Vista alineada con exactamente las columnas ``feature_columns``.
    """
    out = pd.DataFrame(index=df.index)
    for col in feature_columns:
        if col in df.columns:
            out[col] = df[col]
        else:
            out[col] = np.nan
    return out


def _decode_class_labels(bundle: ModelBundle, y_pred: np.ndarray) -> np.ndarray:
    """Convierte predicciones numéricas en etiquetas originales si hay codificador."""
    if bundle.target_encoder is not None:
        return bundle.target_encoder.inverse_transform(np.asarray(y_pred).astype(int))
    return np.asarray(y_pred)


def _rowwise_proba(bundle: ModelBundle, x_transformed: np.ndarray) -> np.ndarray | None:
    """Probabilidad del modelo para la clase predicha en cada fila, si existe ``predict_proba``."""
    est = bundle.estimator
    if not hasattr(est, "predict_proba"):
        return None
    proba = est.predict_proba(x_transformed)
    preds = est.predict(x_transformed)
    classes = np.asarray(est.classes_)
    col_idx = np.array([int(np.flatnonzero(classes == pi)[0]) for pi in preds], dtype=int)
    return proba[np.arange(len(preds)), col_idx]


def predict_dataframe(bundle: ModelBundle, df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica preprocesamiento y genera predicciones (y confianza si aplica).

    Parameters
    ----------
    bundle : ModelBundle
        Artefacto cargado desde disco.
    df : pd.DataFrame
        Datos sin la columna objetivo; debe poder alinearse a ``feature_columns``.

    Returns
    -------
    pd.DataFrame
        Copia enriquecida con columnas ``prediccion_codigo``, ``prediccion_etiqueta``,
        y opcionalmente ``confianza``.
    """
    X = align_features(df, bundle.feature_columns)
    x_transformed = bundle.preprocessor.transform(X)
    y_hat = bundle.estimator.predict(x_transformed)
    labels = _decode_class_labels(bundle, y_hat)
    conf = _rowwise_proba(bundle, x_transformed)

    out = df.copy()
    out["prediccion_codigo"] = np.asarray(y_hat)
    out["prediccion_etiqueta"] = labels.astype(str)
    if conf is not None:
        out["confianza"] = conf
    return out


def predictions_to_json_records(df_out: pd.DataFrame, max_rows: int = 2000) -> str:
    """
    Serializa un subconjunto de columnas de predicción a JSON para SQLite.

    Parameters
    ----------
    df_out : pd.DataFrame
        Salida de ``predict_dataframe``.
    max_rows : int
        Límite de filas para no inflar excesivamente la base local.

    Returns
    -------
    str
        JSON con lista de registros ``{fila, etiqueta, confianza}``.
    """
    n = min(len(df_out), max_rows)
    recs: list[dict[str, Any]] = []
    for i in range(n):
        item: dict[str, Any] = {"fila": i, "etiqueta": str(df_out["prediccion_etiqueta"].iloc[i])}
        if "confianza" in df_out.columns:
            c = df_out["confianza"].iloc[i]
            item["confianza"] = float(c) if pd.notna(c) else None
        recs.append(item)
    return json.dumps(recs, ensure_ascii=False)
