"""
Preparación rigurosa de datos para el prototipo IDS-ML.

El flujo evita fuga de información: primero se separa entrenamiento y prueba,
luego se ajustan transformadores únicamente con datos de entrenamiento.
El balanceo de clases (SMOTE) se aplica solo al conjunto de entrenamiento ya
transformado, sin alterar el particionamiento estratificado inicial.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler


@dataclass(frozen=True)
class PreparedDataset:
    """
    Resultado del preprocesamiento listo para entrenar clasificadores sklearn.

    Attributes
    ----------
    X_train : np.ndarray
        Matriz de entrenamiento transformada (numérica).
    X_test : np.ndarray
        Matriz de prueba transformada con el mismo preprocesador ajustado en train.
    y_train : np.ndarray
        Etiquetas de entrenamiento codificas (enteras).
    y_test : np.ndarray
        Etiquetas de prueba codificas con el mismo codificador de ``y`` ajustado en train.
    preprocessor : ColumnTransformer
        Transformador ajustado solo con ``X_train`` (imputación, escalado, one-hot).
    target_encoder : LabelEncoder | None
        Codificador de la variable objetivo si era categórica; ``None`` si ``y`` ya era numérica.
    feature_columns : tuple[str, ...]
        Nombres y orden de columnas de entrada usadas al ajustar el preprocesador (sin objetivo).
    target_column : str
        Nombre de la columna objetivo en el dataset original.
    """

    x_train: np.ndarray
    x_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    preprocessor: ColumnTransformer
    target_encoder: LabelEncoder | None
    feature_columns: tuple[str, ...]
    target_column: str

def _split_feature_columns(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Separa nombres de columnas numéricas frente a categóricas según dtypes.

    Usa ``select_dtypes(include=number)`` y ``exclude=number`` para evitar ambigüedad
    con el tipo ``str`` de pandas y advertencias de compatibilidad.

    Parameters
    ----------
    X : pd.DataFrame
        Solo características (sin la columna objetivo).

    Returns
    -------
    tuple[list[str], list[str]]
        (columnas_numéricas, columnas_categóricas).
    """
    numeric = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical = X.select_dtypes(exclude=[np.number]).columns.tolist()
    return numeric, categorical


def _build_column_transformer(numeric_cols: list[str], categorical_cols: list[str]) -> ColumnTransformer:
    """
    Construye un ``ColumnTransformer`` con pipelines por tipo de columna.

    Las variables numéricas se imputan (mediana) y escalan con estadísticos de train.
    Las categóricas se imputan (moda) y codifican en one-hot ignorando categorías
    desconocidas en prueba.

    Parameters
    ----------
    numeric_cols : list[str]
        Nombres de columnas tratadas como numéricas.
    categorical_cols : list[str]
        Nombres de columnas tratadas como categóricas.

    Returns
    -------
    ColumnTransformer
        Transformador sin ajustar; debe llamarse ``fit`` solo con datos de entrenamiento.
    """
    transformers: list[tuple[str, Pipeline, list[str]]] = []

    if numeric_cols:
        numeric_pipe = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ],
            memory=None,
        )
        transformers.append(("num", numeric_pipe, numeric_cols))

    if categorical_cols:
        categorical_pipe = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "onehot",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                ),
            ],
            memory=None,
        )
        transformers.append(("cat", categorical_pipe, categorical_cols))

    if not transformers:
        raise ValueError("No quedaron columnas de características para transformar.")

    return ColumnTransformer(transformers=transformers, remainder="drop", verbose_feature_names_out=False)


def _stratify_if_possible(y: pd.Series) -> pd.Series | None:
    """
    Devuelve ``y`` para usar como ``stratify`` solo si cada clase tiene al menos 2 muestras.

    ``train_test_split`` con ``stratify`` exige al menos dos ejemplos por clase.

    Parameters
    ----------
    y : pd.Series
        Objetivo en bruto (antes de codificar numéricamente).

    Returns
    -------
    pd.Series | None
        La misma serie si se puede estratificar; si no, ``None``.
    """
    counts = y.value_counts()
    if len(counts) < 2:
        return None
    if counts.min() < 2:
        return None
    return y


def _encode_target_after_split(
    y_train: pd.Series,
    y_test: pd.Series,
) -> tuple[np.ndarray, np.ndarray, LabelEncoder | None]:
    """
    Codifica la variable objetivo usando únicamente las etiquetas vistas en entrenamiento.

    Si ``y`` ya es numérica con valores enteros (p. ej. 0/1 o clases 0..K-1), se convierte
    a ``int64`` sin ajustar un codificador sobre el conjunto global.
    Si es categórica/texto, ``LabelEncoder`` se ajusta solo con ``y_train``; si en prueba
    aparecen clases no vistas, se lanza un error explícito.

    Parameters
    ----------
    y_train : pd.Series
        Objetivo del conjunto de entrenamiento.
    y_test : pd.Series
        Objetivo del conjunto de prueba.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, LabelEncoder | None]
        ``y_train`` y ``y_test`` codificados, y el codificador o ``None``.
    """
    if pd.api.types.is_numeric_dtype(y_train) and pd.api.types.is_numeric_dtype(y_test):
        y_tr = np.asarray(y_train.to_numpy(), dtype=float)
        y_te = np.asarray(y_test.to_numpy(), dtype=float)
        if not (np.allclose(y_tr, np.round(y_tr)) and np.allclose(y_te, np.round(y_te))):
            raise ValueError(
                "La columna objetivo es numérica pero no entera; use etiquetas categóricas o enteras."
            )
        return np.round(y_tr).astype(np.int64), np.round(y_te).astype(np.int64), None

    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train.astype(str))
    test_labels = y_test.astype(str)
    unseen = set(test_labels.unique()) - set(le.classes_)
    if unseen:
        raise ValueError(
            "El conjunto de prueba contiene etiquetas no vistas en entrenamiento: "
            f"{sorted(unseen)!s}. Revise el particionamiento o use un split estratificado."
        )
    y_test_enc = le.transform(test_labels)
    return y_train_enc, y_test_enc, le


def _maybe_resample_training(
    X_train: np.ndarray,
    y_train: np.ndarray,
    *,
    random_state: int,
    apply_smote: bool,
) -> tuple[np.ndarray, np.ndarray, bool]:
    """
    Aplica SMOTE solo al conjunto de entrenamiento transformado.

    No modifica ``X_test`` ni ``y_test``. Si SMOTE no aplica (pocas muestras, una sola
    clase, etc.), se devuelve el mismo ``X_train``, ``y_train`` y ``False``.

    Parameters
    ----------
    X_train : np.ndarray
        Características de entrenamiento ya preprocesadas.
    y_train : np.ndarray
        Etiquetas de entrenamiento codificas.
    random_state : int
        Semilla para SMOTE.
    apply_smote : bool
        Si es ``False``, no se intenta remuestreo.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, bool]
        Datos de entrenamiento posiblemente remuestreados y bandera ``smote_applied``.
    """
    if not apply_smote:
        return X_train, y_train, False
    unique, counts = np.unique(y_train, return_counts=True)
    if len(unique) < 2:
        return X_train, y_train, False
    if counts.min() < 2:
        return X_train, y_train, False
    try:
        smote = SMOTE(random_state=random_state)
        x_resampled, y_resampled = smote.fit_resample(X_train, y_train)
        return x_resampled, y_resampled, True
    except ValueError:
        return X_train, y_train, False


def prepare_dataset(
    df: pd.DataFrame,
    target_col: str,
    *,
    test_size: float = 0.25,
    random_state: int = 42,
    apply_smote: bool = True,
    drop_na_rows: bool = True,
) -> PreparedDataset:
    """
    Particiona datos y construye matrices listas para ``model.fit`` sin fuga de datos.

    Pasos:
        1. Elimina filas con objetivo ausente (opcionalmente todas las filas con NA).
        2. Separa ``X`` e ``y``.
        3. ``train_test_split`` sobre filas en bruto (estratificación si es posible).
        4. Ajusta ``ColumnTransformer`` solo con ``X_train``; transforma train y test.
        5. Codifica ``y`` con información solo de ``y_train``.
        6. Opcionalmente aplica SMOTE solo a ``(X_train, y_train)`` ya transformados.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset completo incluyendo la columna objetivo.
    target_col : str
        Nombre de la columna de clase / etiqueta.
    test_size : float, default=0.25
        Proporción del conjunto de prueba.
    random_state : int, default=42
        Semilla para partición y SMOTE.
    apply_smote : bool, default=True
        Si intentar balancear clases en train con SMOTE tras el preprocesado.
    drop_na_rows : bool, default=True
        Si ``True``, elimina filas con cualquier NA (comportamiento conservador del
        prototipo anterior). Si ``False``, solo elimina filas con NA en ``y``; el resto
        lo gestionan los imputadores del pipeline.

    Returns
    -------
    PreparedDataset
        Contenedores con matrices y el ``ColumnTransformer`` ajustado.
    """
    if target_col not in df.columns:
        raise KeyError(f"No existe la columna objetivo {target_col!r} en el DataFrame.")

    data = df.copy()
    if drop_na_rows:
        data = data.dropna(axis=0)
    else:
        data = data.dropna(axis=0, subset=[target_col])

    y = data[target_col]
    X = data.drop(columns=[target_col])

    stratify = _stratify_if_possible(y)
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify,
        )
    except ValueError:
        # Muestras insuficientes para estratificar (p. ej. test_size muy pequeño y muchas clases).
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=None,
        )

    numeric_cols, categorical_cols = _split_feature_columns(X_train)
    preprocessor = _build_column_transformer(numeric_cols, categorical_cols)
    preprocessor.fit(X_train)
    x_train_transformed = preprocessor.transform(X_train)
    x_test_transformed = preprocessor.transform(X_test)

    y_train_enc, y_test_enc, target_encoder = _encode_target_after_split(y_train, y_test)

    x_train_final, y_train_final, _ = _maybe_resample_training(
        x_train_transformed,
        y_train_enc,
        random_state=random_state,
        apply_smote=apply_smote,
    )

    return PreparedDataset(
        x_train=np.asarray(x_train_final, dtype=np.float64),
        x_test=np.asarray(x_test_transformed, dtype=np.float64),
        y_train=np.asarray(y_train_final),
        y_test=np.asarray(y_test_enc),
        preprocessor=preprocessor,
        target_encoder=target_encoder,
        feature_columns=tuple(X_train.columns.tolist()),
        target_column=target_col,
    )
