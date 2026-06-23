"""Páginas Streamlit del IDS-ML (UI orquestadora, lógica ML en módulos dedicados)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.alerts.engine import build_alert
from src.audit.service import log_action
from src.data.profile import profile_dataframe
from src.models.persistence import (
    default_bundle_path,
    load_model_bundle,
    predict_dataframe,
    predictions_to_json_records,
    save_model_bundle,
)
from src.models.trainer import MODELS, select_best_model, train_and_evaluate
from src.preprocessing.pipeline import prepare_dataset
from src.reports import generator as report_gen
from src.security import rbac
from src.services.dashboard_service import build_dashboard_context
from src.services.database_model_service import (
    DBML_PATH,
    POSTGRES_SCHEMA_PATH,
    SQLITE_SCHEMA_PATH,
    build_relationship_dot,
    parse_tables,
    read_schema,
    summarize_modules,
    summarize_tables,
)
from src.services.system_status_service import build_status_payload, firestore_ping_ok
from src.ui.theme import (
    PALETTE,
    chip_row,
    empty_state,
    format_int,
    format_percent,
    metric_card,
    page_header,
    pipeline_steps,
    render_card,
    section_title,
    severity_tone,
    themed_plotly,
    threat_mask,
)

if TYPE_CHECKING:
    from src.preprocessing.pipeline import PreparedDataset
    from src.storage.base_repository import IDSMLRepository


def _init_session() -> None:
    defaults = {
        "df": None,
        "dataset_profile": None,
        "dataset_upload_key": None,
        "prepared_dataset": None,
        "prepared_target_col": None,
        "preprocessing_options": None,
        "results": None,
        "best_model": None,
        "last_pred_df": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _profile_metrics(df: pd.DataFrame, profile: dict[str, Any]) -> dict[str, float]:
    total_cells = max(1, int(profile["rows"]) * int(profile["columns"]))
    missing_pct = (float(profile["missing_total"]) / total_cells) * 100
    duplicate_pct = (float(profile["duplicated_rows"]) / max(1, int(profile["rows"]))) * 100
    memory_mb = float(df.memory_usage(deep=True).sum()) / (1024 * 1024)
    numeric_cols = len(df.select_dtypes(include="number").columns)
    categorical_cols = int(profile["columns"]) - numeric_cols
    quality = max(0.0, min(100.0, 100.0 - missing_pct - duplicate_pct))
    return {
        "missing_pct": missing_pct,
        "duplicate_pct": duplicate_pct,
        "memory_mb": memory_mb,
        "numeric_cols": float(numeric_cols),
        "categorical_cols": float(categorical_cols),
        "quality": quality,
    }


def _column_profile_df(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in df.columns:
        sample = df[col].dropna().head(1)
        rows.append(
            {
                "columna": col,
                "tipo": str(df[col].dtype),
                "nulos": int(df[col].isna().sum()),
                "valores_unicos": int(df[col].nunique(dropna=True)),
                "muestra": "" if sample.empty else str(sample.iloc[0])[:80],
            }
        )
    return pd.DataFrame(rows)


def _results_dataframe(results: list[Any], best_name: str | None = None) -> pd.DataFrame:
    rows = []
    for result in results:
        rows.append(
            {
                "modelo": result.name,
                "accuracy": result.metrics.get("accuracy", 0.0),
                "precision": result.metrics.get("precision", 0.0),
                "recall": result.metrics.get("recall", 0.0),
                "f1_score": result.metrics.get("f1_score", 0.0),
                "estado": "Mejor F1" if result.name == best_name else "Candidato",
            }
        )
    return pd.DataFrame(rows)


def _backend_label(backend_name: str) -> str:
    labels = {
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "sqlite": "SQLite local",
        "firestore": "Firestore",
        "auto": "Automático",
    }
    return labels.get(str(backend_name).lower(), str(backend_name).upper())


def _register_training_results(
    repo: "IDSMLRepository",
    prepared: "PreparedDataset",
    results: list[Any],
) -> None:
    best = select_best_model(results)
    st.session_state["results"] = results
    st.session_state["best_model"] = best

    for result in results:
        repo.save_experiment(result.name, result.metrics)

    bundle_path = save_model_bundle(
        best.model,
        prepared,
        model_name=best.name,
        f1_score=best.metrics.get("f1_score", 0.0),
    )
    version_label = f"v-{datetime.now().strftime('%Y%m%dT%H%M%S')}"
    repo.register_model_version(
        model_name=best.name,
        f1_score=float(best.metrics.get("f1_score", 0.0)),
        bundle_path=str(bundle_path),
        version_label=version_label,
    )
    log_action(
        repo,
        action="entrenamiento_completo",
        module="entrenamiento",
        result="ok",
        observation=(
            f"mejor={best.name}, f1={best.metrics.get('f1_score')}, "
            f"bundle={bundle_path}, version={version_label}"
        ),
    )
    st.success(f"Mejor modelo: {best.name}. Artefacto: {bundle_path} (versión {version_label}).")


def _render_results_panel(results: list[Any]) -> None:
    best = st.session_state.get("best_model")
    best_name = best.name if best else None
    metrics_df = _results_dataframe(results, best_name)

    if best is not None:
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            metric_card("Accuracy", format_percent(best.metrics.get("accuracy")), best.name, tone="blue")
        with k2:
            metric_card("Precisión", format_percent(best.metrics.get("precision")), "Comparación ponderada", tone="green")
        with k3:
            metric_card("Recall", format_percent(best.metrics.get("recall")), "Cobertura de clases", tone="slate")
        with k4:
            metric_card("F1-score", format_percent(best.metrics.get("f1_score")), "Criterio de selección", tone="amber")

    section_title("Tabla comparativa", "El mejor modelo se selecciona por F1-score ponderado.")
    st.dataframe(metrics_df, width="stretch", hide_index=True)

    left, right = st.columns([1.2, 1])
    with left:
        fig = px.bar(
            metrics_df,
            x="modelo",
            y="f1_score",
            color="estado",
            color_discrete_map={"Mejor F1": PALETTE["green"], "Candidato": PALETTE["blue"]},
            title="F1-score por modelo",
        )
        st.plotly_chart(themed_plotly(fig, height=360), width="stretch")

    with right:
        if best is not None:
            cm = pd.DataFrame(best.confusion_matrix)
            fig = px.imshow(
                cm,
                text_auto=True,
                color_continuous_scale=[[0, PALETTE["surface"]], [1, PALETTE["blue"]]],
                title="Matriz de confusión del mejor modelo",
            )
            st.plotly_chart(themed_plotly(fig, height=360), width="stretch")


def render_dashboard(repo: "IDSMLRepository") -> None:
    _init_session()
    page_header(
        "Dashboard ejecutivo",
        "Vista consolidada del prototipo IDS-ML: modelo activo, inferencias, alertas y auditoría.",
        tag=f"Motor de datos: {_backend_label(repo.backend_name)}",
    )

    ctx = build_dashboard_context(repo)
    counts = ctx["counts"]
    active_model = ctx.get("active_model") or {}
    active_f1 = active_model.get("f1_score") or ctx.get("best_f1_session")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Eventos evaluados", format_int(counts.get("prediction_rows", 0)), "Filas persistidas", tone="blue")
    with c2:
        metric_card("Amenazas detectadas", format_int(counts.get("amenazas_detectadas", 0)), "Predicciones no benignas", tone="red")
    with c3:
        metric_card("Precisión ML", format_percent(active_f1, 2), active_model.get("model_name", "Sin modelo activo"), tone="green", progress=(float(active_f1 or 0) * 100))
    with c4:
        metric_card("Alertas activas", format_int(counts.get("alerts", 0)), f"Persistencia {_backend_label(repo.backend_name)}", tone="amber")

    normal_rows = max(0, int(counts.get("prediction_rows", 0)) - int(counts.get("amenazas_detectadas", 0)))
    threat_rows = int(counts.get("amenazas_detectadas", 0))
    left, right = st.columns([0.9, 1.6])
    with left:
        section_title("Distribución de tráfico", "Proporción operacional basada en inferencias persistidas.")
        if normal_rows or threat_rows:
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=["Normal", "Amenaza"],
                        values=[normal_rows, threat_rows],
                        hole=0.62,
                        marker=dict(colors=[PALETTE["blue"], PALETTE["red"]]),
                    )
                ]
            )
            st.plotly_chart(themed_plotly(fig, height=330), width="stretch")
        else:
            empty_state("Ejecute una inferencia y persista predicciones para construir esta vista.")

    with right:
        section_title("Paisaje de amenazas", "Severidad registrada en la muestra reciente de alertas.")
        severity = ctx.get("severity_distribution") or {}
        if severity:
            sev_df = pd.DataFrame({"severidad": list(severity.keys()), "alertas": list(severity.values())})
            fig = px.bar(
                sev_df,
                x="severidad",
                y="alertas",
                color="severidad",
                color_discrete_map={
                    "Alta": PALETTE["red"],
                    "Crítica": PALETTE["red"],
                    "Media": PALETTE["amber"],
                    "Baja": PALETTE["green"],
                },
                title="Alertas por severidad",
            )
            st.plotly_chart(themed_plotly(fig, height=330), width="stretch")
        else:
            empty_state("Aún no hay alertas almacenadas.")

    if st.session_state.get("results"):
        section_title("Comparación de la sesión actual", "Resultados recientes aún disponibles en memoria.")
        _render_results_panel(st.session_state["results"])

    section_title("Eventos de seguridad recientes", "Últimas alertas generadas por inferencia o pruebas manuales.")
    recent_alerts = ctx.get("recent_alerts") or []
    if recent_alerts:
        alerts_df = pd.DataFrame(recent_alerts)
        columns = [c for c in ["created_at", "tipo", "severidad", "probabilidad", "modelo_usado", "estado"] if c in alerts_df.columns]
        st.dataframe(alerts_df[columns], width="stretch", hide_index=True)
    else:
        empty_state("El centro de alertas todavía no tiene eventos.")

    section_title("Bitácora estructurada", "Actividad operativa más reciente del sistema.")
    recent_audit = ctx.get("recent_audit") or []
    st.dataframe(pd.DataFrame(recent_audit) if recent_audit else pd.DataFrame(), width="stretch", hide_index=True)


def render_dataset(repo: "IDSMLRepository") -> None:
    _init_session()
    if not rbac.can_access_dataset(st.session_state.get("role", "")):
        st.warning("Sin permisos para este módulo.")
        return

    page_header(
        "Gestión de datasets",
        "Carga y perfilado de CSV autorizados para entrenar y validar el prototipo IDS-ML.",
        tag="CSV controlado",
    )

    upload_col, status_col = st.columns([1.8, 0.9])
    with upload_col:
        uploaded = st.file_uploader("Arrastra o selecciona un archivo CSV de tráfico IDS", type=["csv"])
    with status_col:
        profile = st.session_state.get("dataset_profile")
        df = st.session_state.get("df")
        if df is not None and profile is not None:
            metrics = _profile_metrics(df, profile)
            metric_card("Estado del dataset", "Procesado", f"{format_int(profile['rows'])} filas", tone="green", progress=metrics["quality"])
        else:
            metric_card("Estado del dataset", "Pendiente", "Esperando carga CSV", tone="amber")

    if uploaded is not None:
        upload_key = f"{uploaded.name}:{getattr(uploaded, 'size', 0)}"
        if st.session_state.get("dataset_upload_key") != upload_key:
            df = pd.read_csv(uploaded)
            profile = profile_dataframe(df)
            st.session_state["df"] = df
            st.session_state["dataset_profile"] = profile
            st.session_state["dataset_upload_key"] = upload_key
            st.session_state["prepared_dataset"] = None
            st.session_state["prepared_target_col"] = None
            st.session_state["results"] = None
            st.session_state["best_model"] = None
            log_action(
                repo,
                action="carga_dataset",
                module="dataset",
                result="ok",
                observation=f"archivo={uploaded.name}, filas={len(df)}, columnas={df.shape[1]}",
            )
            st.success("Dataset cargado correctamente.")

    df = st.session_state.get("df")
    profile = st.session_state.get("dataset_profile")
    if df is None or profile is None:
        empty_state("Seleccione un CSV para activar el perfilado, la validación y el flujo de entrenamiento.")
        return

    metrics = _profile_metrics(df, profile)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Tamaño total", f"{metrics['memory_mb']:.2f} MB", f"{format_int(profile['rows'])} registros", tone="blue")
    with c2:
        metric_card("Nulls / missing", f"{metrics['missing_pct']:.2f}%", "Valores ausentes", tone="green" if metrics["missing_pct"] < 5 else "amber", progress=100 - metrics["missing_pct"])
    with c3:
        metric_card("Duplicados", f"{metrics['duplicate_pct']:.2f}%", "Filas repetidas", tone="amber" if metrics["duplicate_pct"] else "green", progress=max(0, 100 - metrics["duplicate_pct"]))
    with c4:
        metric_card("Consistencia", f"{metrics['quality']:.1f}%", f"{int(metrics['numeric_cols'])} num / {int(metrics['categorical_cols'])} cat", tone="green", progress=metrics["quality"])

    section_title("Vista previa", "Primeras filas del dataset cargado.")
    st.dataframe(df.head(30), width="stretch")

    section_title("Exploración de columnas", "Tipos de datos, nulos, cardinalidad y muestra por columna.")
    st.dataframe(_column_profile_df(df), width="stretch", hide_index=True)

    if st.button("Validar dataset para preprocesamiento"):
        st.success("Dataset validado para seleccionar columna objetivo en el módulo Preprocesamiento.")
        log_action(
            repo,
            action="validacion_dataset",
            module="dataset",
            result="ok",
            observation=f"filas={profile['rows']}, columnas={profile['columns']}, calidad={metrics['quality']:.2f}",
        )


def render_preprocessing(repo: "IDSMLRepository") -> None:
    _init_session()
    if not rbac.can_train(st.session_state.get("role", "")):
        st.warning("Solo personal TI (Administrador o Analista) puede ejecutar preprocesamiento.")
        return

    page_header(
        "Preprocesamiento de datos",
        "Preparación sin fuga de información: limpieza, codificación, escalado, split train/test y SMOTE opcional.",
        tag="Pipeline ML",
    )

    df = st.session_state.get("df")
    if df is None:
        empty_state("Primero cargue un dataset CSV en el módulo Dataset.")
        return

    control_col, summary_col = st.columns([1.25, 0.9])
    with control_col:
        target_col = st.selectbox("Columna objetivo / clase", list(df.columns), key="preprocess_target_col")
        test_size = st.slider("Tamaño del conjunto de prueba", 0.10, 0.40, 0.25, 0.05)
        apply_smote = st.checkbox("Aplicar SMOTE solo en entrenamiento", value=True)
        drop_na_rows = st.checkbox("Eliminar filas con cualquier NA antes del split", value=True)
        run_preprocessing = st.button("Ejecutar preprocesamiento")
    with summary_col:
        profile = st.session_state.get("dataset_profile") or profile_dataframe(df)
        metrics = _profile_metrics(df, profile)
        metric_card("Data quality score", f"{metrics['quality']:.1f}%", "Antes del pipeline", tone="green", progress=metrics["quality"])

    if run_preprocessing:
        try:
            with st.spinner("Ejecutando pipeline de preprocesamiento..."):
                prepared = prepare_dataset(
                    df,
                    target_col,
                    test_size=float(test_size),
                    apply_smote=apply_smote,
                    drop_na_rows=drop_na_rows,
                )
            st.session_state["prepared_dataset"] = prepared
            st.session_state["prepared_target_col"] = target_col
            st.session_state["preprocessing_options"] = {
                "test_size": test_size,
                "apply_smote": apply_smote,
                "drop_na_rows": drop_na_rows,
            }
            log_action(
                repo,
                action="preprocesamiento_dataset",
                module="preprocesamiento",
                result="ok",
                observation=(
                    f"target={target_col}, train={prepared.x_train.shape[0]}, "
                    f"test={prepared.x_test.shape[0]}, features={prepared.x_train.shape[1]}"
                ),
            )
            st.success("Preprocesamiento completado. Puede continuar con Entrenamiento.")
        except Exception as exc:
            try:
                repo.save_system_error("preprocesamiento", str(exc), {"target": target_col})
            except Exception:
                pass
            st.error(f"No se pudo completar el preprocesamiento: {exc}")

    prepared = st.session_state.get("prepared_dataset")
    prepared_target = st.session_state.get("prepared_target_col")
    if prepared is None:
        pipeline_steps(
            [
                {"name": "Cleaning", "status": "pendiente", "state": "pending", "description": "Validación de NA y filas útiles."},
                {"name": "Encoding", "status": "pendiente", "state": "pending", "description": "One-hot para variables categóricas."},
                {"name": "Normalization", "status": "pendiente", "state": "pending", "description": "Imputación y escalado numérico."},
                {"name": "Split", "status": "pendiente", "state": "pending", "description": "Separación train/test sin fuga."},
                {"name": "SMOTE", "status": "opcional", "state": "pending", "description": "Balanceo solo sobre entrenamiento."},
            ]
        )
        return

    pipeline_steps(
        [
            {"name": "Cleaning", "status": "completed", "state": "done", "description": "Filas y objetivo preparados."},
            {"name": "Encoding", "status": "completed", "state": "done", "description": "Variables categóricas codificadas."},
            {"name": "Normalization", "status": "completed", "state": "done", "description": "Numéricas imputadas y escaladas."},
            {"name": "Split", "status": "completed", "state": "done", "description": "Partición train/test generada."},
            {"name": "Selection", "status": "ready", "state": "active", "description": "Listo para comparación de modelos."},
        ]
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        metric_card("Target", prepared_target, "Variable objetivo seleccionada", tone="blue")
    with k2:
        metric_card("Train rows", format_int(prepared.x_train.shape[0]), "Matriz transformada", tone="green")
    with k3:
        metric_card("Test rows", format_int(prepared.x_test.shape[0]), "Evaluación retenida", tone="slate")
    with k4:
        metric_card("Features", format_int(prepared.x_train.shape[1]), "Después del transformador", tone="amber")

    section_title("Muestra transformada", "Primeras columnas numéricas que recibirá scikit-learn.")
    try:
        feature_names = list(prepared.preprocessor.get_feature_names_out())
    except Exception:
        feature_names = [f"feature_{i + 1}" for i in range(prepared.x_train.shape[1])]
    n_cols = min(10, prepared.x_train.shape[1])
    sample_df = pd.DataFrame(prepared.x_train[:10, :n_cols], columns=feature_names[:n_cols])
    st.dataframe(sample_df, width="stretch")


def render_training(repo: "IDSMLRepository") -> None:
    _init_session()
    if not rbac.can_train(st.session_state.get("role", "")):
        st.warning("Solo personal TI (Administrador o Analista) puede entrenar modelos.")
        return

    page_header(
        "Comparación y entrenamiento",
        "Entrena modelos candidatos, compara métricas y registra como activo el mejor clasificador por F1-score.",
        tag="Model node active",
    )

    df = st.session_state.get("df")
    if df is None:
        empty_state("Primero cargue un dataset en el módulo Dataset.")
        return

    left, right = st.columns([1.05, 1.6])
    with left:
        section_title("Modelos candidatos", "Configuración actual de scikit-learn.")
        for model_name in MODELS:
            render_card(model_name, "Candidato listo para entrenamiento comparativo.", tone="blue")
    with right:
        target_col = st.selectbox("Seleccione columna objetivo/clase", list(df.columns), key="training_target_col")
        prepared = st.session_state.get("prepared_dataset")
        can_reuse = prepared is not None and st.session_state.get("prepared_target_col") == target_col
        if can_reuse:
            st.info("Se reutilizará el preprocesamiento validado para esta columna objetivo.")
        else:
            st.info("Si no existe preprocesamiento validado para este objetivo, se ejecutará el pipeline antes de entrenar.")

        if st.button("Entrenar y comparar modelos"):
            try:
                with st.spinner("Preparando datos y entrenando modelos..."):
                    prepared_for_training = prepared if can_reuse else prepare_dataset(df, target_col)
                    results = train_and_evaluate(
                        prepared_for_training.x_train,
                        prepared_for_training.x_test,
                        prepared_for_training.y_train,
                        prepared_for_training.y_test,
                    )
                    if not can_reuse:
                        st.session_state["prepared_dataset"] = prepared_for_training
                        st.session_state["prepared_target_col"] = target_col
                    _register_training_results(repo, prepared_for_training, results)
            except Exception as exc:
                try:
                    repo.save_system_error("entrenamiento", str(exc), {"target": target_col})
                except Exception:
                    pass
                st.error(f"No se pudo entrenar: {exc}")

    if st.session_state.get("results"):
        _render_results_panel(st.session_state["results"])


def render_inference(repo: "IDSMLRepository") -> None:
    _init_session()
    if not rbac.can_infer(st.session_state.get("role", "")):
        st.warning("Solo personal TI autorizado puede ejecutar inferencia.")
        return

    page_header(
        "Análisis de tráfico nuevo",
        "Carga registros sin columna objetivo, aplica el bundle activo y genera predicciones, alertas y persistencia.",
        tag="Traffic analysis",
    )

    config_col, upload_col = st.columns([0.9, 1.4])
    with config_col:
        bundle_upload = st.file_uploader("Bundle .joblib opcional", type=["joblib"])
        bundle_path = default_bundle_path()
        if bundle_upload is not None:
            bundle_path.parent.mkdir(parents=True, exist_ok=True)
            bundle_path = bundle_path.parent / "uploaded_infer_bundle.joblib"
            bundle_path.write_bytes(bundle_upload.getbuffer())

        try:
            bundle = load_model_bundle(bundle_path)
        except FileNotFoundError:
            empty_state(f"No hay modelo en {default_bundle_path()}. Entrene primero o cargue un bundle.")
            return

        metric_card("Motor de detección", bundle.model_name, f"F1 guardado {bundle.f1_score:.4f}", tone="blue", progress=bundle.f1_score * 100)
        metric_card("Features esperadas", format_int(len(bundle.feature_columns)), f"Entrenado {bundle.trained_at}", tone="green")

    with upload_col:
        uploaded_infer = st.file_uploader("CSV de registros nuevos", type=["csv"], key="infer_csv")
        if uploaded_infer is not None:
            df_new = pd.read_csv(uploaded_infer)
            st.caption(f"Archivo listo: {uploaded_infer.name} ({format_int(len(df_new))} filas).")
            if st.button("Ejecutar análisis"):
                try:
                    with st.spinner("Aplicando preprocesamiento y modelo activo..."):
                        pred_df = predict_dataframe(bundle, df_new)
                        st.session_state["last_pred_df"] = pred_df
                    log_action(
                        repo,
                        action="prediccion_lote",
                        module="inferencia",
                        result="ok",
                        observation=f"filas={len(pred_df)}, modelo={bundle.model_name}",
                    )
                    st.success(f"Predicciones listas ({len(pred_df)} filas).")
                except Exception as exc:
                    try:
                        repo.save_system_error("inferencia", str(exc), {"modelo": bundle.model_name})
                    except Exception:
                        pass
                    st.error(f"No se pudo ejecutar la inferencia: {exc}")

    pred_df = st.session_state.get("last_pred_df")
    if pred_df is None:
        empty_state("Cargue un CSV nuevo y ejecute el análisis para visualizar patrones y predicciones.")
        return

    labels = pred_df["prediccion_etiqueta"].astype(str)
    threats = threat_mask(labels)
    threat_count = int(threats.sum())
    confidence = pred_df["confianza"] if "confianza" in pred_df.columns else pd.Series(dtype=float)
    max_confidence = float(confidence.max()) if not confidence.empty else None

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("System threat status", "THREAT" if threat_count else "NORMAL", f"{threat_count} hallazgos", tone="red" if threat_count else "green")
    with c2:
        metric_card("Probabilidad máx.", format_percent(max_confidence, 2), "Confianza del modelo", tone="red" if threat_count else "blue", progress=(max_confidence or 0) * 100)
    with c3:
        metric_card("Registros analizados", format_int(len(pred_df)), "Lote actual", tone="blue")
    with c4:
        metric_card("Modelo agente", bundle.model_name, "Bundle activo", tone="green")

    section_title("Visualización de patrón", "Primeros registros del lote con énfasis en anomalías.")
    plot_df = pred_df.head(80).copy()
    plot_df["_fila"] = range(len(plot_df))
    plot_df["_amenaza"] = threat_mask(plot_df["prediccion_etiqueta"].astype(str))
    if "confianza" not in plot_df.columns:
        plot_df["confianza"] = 1.0
    fig = px.bar(
        plot_df,
        x="_fila",
        y="confianza",
        color="_amenaza",
        color_discrete_map={True: PALETTE["red"], False: PALETTE["blue"]},
        title="Densidad de confianza por registro",
    )
    st.plotly_chart(themed_plotly(fig, height=320), width="stretch")

    section_title("Predicciones del lote", "Resultado generado por el pipeline y modelo activo.")
    st.dataframe(pred_df, width="stretch")

    if st.button("Persistir predicciones, filas y alertas"):
        details_json = predictions_to_json_records(pred_df)
        run_id = repo.save_prediction_run(
            model_name=bundle.model_name,
            f1_score=bundle.f1_score,
            n_rows=len(pred_df),
            trained_at_model=bundle.trained_at,
            details=details_json,
        )
        rows_detail = []
        for idx, (_, row) in enumerate(pred_df.iterrows()):
            conf = None
            if "confianza" in pred_df.columns and pd.notna(row.get("confianza")):
                conf = float(row["confianza"])
            rows_detail.append(
                {
                    "row_index": idx,
                    "label": str(row["prediccion_etiqueta"]),
                    "confidence": conf,
                }
            )
        repo.save_prediction_rows(run_id, rows_detail)

        max_alerts = 100
        n_alert = min(len(pred_df), max_alerts)
        for _, row in pred_df.head(max_alerts).iterrows():
            prob = None
            if "confianza" in pred_df.columns and pd.notna(row.get("confianza")):
                prob = float(row["confianza"])
            alert = build_alert(
                str(row["prediccion_etiqueta"]),
                prob,
                modelo_usado=bundle.model_name,
                backend=repo.backend_name,
            )
            repo.save_alert(alert)

        log_action(
            repo,
            action="persistencia_inferencia",
            module="inferencia",
            result="ok",
            observation=f"run_id={run_id}, alertas={n_alert}",
        )
        st.success(f"Run {run_id}: filas detalle, {n_alert} alertas y bitácora registradas.")


def render_alerts(repo: "IDSMLRepository") -> None:
    if not rbac.can_manage_alerts(st.session_state.get("role", "")):
        st.warning("Sin permisos para gestión de alertas.")
        return

    page_header(
        "Centro de alertas",
        "Revisión de eventos generados por inferencia, filtros por severidad y gestión de estado.",
        tag="Alerts center",
    )

    alerts = repo.list_alerts(limit=200)
    alerts_df = pd.DataFrame(alerts)
    active_model = repo.get_active_model_version() or {}

    if alerts_df.empty:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("System status", "Operacional", "Sin alertas registradas", tone="green")
        with c2:
            metric_card("Critical alerts", "0", "Muestra actual", tone="red")
        with c3:
            metric_card("Model confidence", format_percent(active_model.get("f1_score"), 2), active_model.get("model_name", "Sin modelo"), tone="blue")
        with c4:
            metric_card("Persistencia", _backend_label(repo.backend_name), "Motor activo", tone="slate")
        empty_state("Las alertas automáticas aparecerán después de persistir una inferencia.")
    else:
        severe_mask = alerts_df["severidad"].astype(str).str.lower().isin(["alta", "crítica", "critica", "critical"])
        new_mask = alerts_df.get("estado", pd.Series(dtype=str)).astype(str).str.lower().eq("nueva")
        avg_prob = alerts_df["probabilidad"].dropna().mean() if "probabilidad" in alerts_df.columns else None

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("System status", "Operacional", "Monitoreo activo", tone="green")
        with c2:
            metric_card("Alertas críticas/altas", format_int(severe_mask.sum()), "Prioridad de revisión", tone="red")
        with c3:
            metric_card("Confianza promedio", format_percent(avg_prob, 2), "Alertas con probabilidad", tone="blue", progress=(float(avg_prob or 0) * 100))
        with c4:
            metric_card("Nuevas", format_int(new_mask.sum()), "Pendientes de gestión", tone="amber")

        filter_col, table_col = st.columns([0.7, 1.8])
        with filter_col:
            section_title("Filtros", "Acote la lista operacional.")
            severities = sorted(alerts_df["severidad"].dropna().astype(str).unique().tolist())
            statuses = sorted(alerts_df["estado"].dropna().astype(str).unique().tolist()) if "estado" in alerts_df.columns else []
            selected_sev = st.multiselect("Severidad", severities, default=severities)
            selected_status = st.multiselect("Estado", statuses, default=statuses)
            if rbac.can_manual_alert_demo(st.session_state.get("role", "")):
                with st.expander("Registrar alerta manual"):
                    prediction = st.text_input("Tipo de amenaza", value="ataque")
                    if st.button("Registrar alerta manual"):
                        alert = build_alert(prediction, backend=repo.backend_name)
                        repo.save_alert(alert)
                        log_action(repo, action="alerta_manual", module="alertas", result="ok", observation=prediction)
                        st.success("Alerta registrada.")
                        st.rerun()

        filtered = alerts_df.copy()
        if selected_sev:
            filtered = filtered[filtered["severidad"].astype(str).isin(selected_sev)]
        if selected_status and "estado" in filtered.columns:
            filtered = filtered[filtered["estado"].astype(str).isin(selected_status)]

        with table_col:
            section_title("Lista de alertas activas", "Eventos recientes ordenados por persistencia.")
            columns = [
                c
                for c in ["id", "alert_uuid", "created_at", "tipo", "severidad", "probabilidad", "modelo_usado", "estado"]
                if c in filtered.columns
            ]
            st.dataframe(filtered[columns], width="stretch", hide_index=True)

        if not filtered.empty:
            section_title("Tendencia por severidad", "Distribución visual de la lista filtrada.")
            sev_counts = filtered["severidad"].value_counts().reset_index()
            sev_counts.columns = ["severidad", "alertas"]
            fig = px.bar(
                sev_counts,
                x="severidad",
                y="alertas",
                color="severidad",
                color_discrete_map={sev: PALETTE[severity_tone(sev)] for sev in sev_counts["severidad"]},
                title="Alertas filtradas",
            )
            st.plotly_chart(themed_plotly(fig, height=300), width="stretch")

    if rbac.can_change_alert_status(st.session_state.get("role", "")):
        section_title("Cambiar estado", "Administradores TI pueden cerrar o marcar revisión de alertas.")
        aid_col, status_col, button_col = st.columns([1.1, 0.7, 0.5])
        with aid_col:
            aid = st.text_input("ID alerta (UUID o id SQLite)", "")
        with status_col:
            status = st.selectbox("Nuevo estado", ["nueva", "revisada", "cerrada"])
        with button_col:
            st.write("")
            st.write("")
            if st.button("Actualizar") and aid:
                ok = repo.update_alert_status(aid, status, st.session_state.get("role", ""))
                st.success("Actualizado.") if ok else st.error("No se encontró la alerta.")

    section_title("Historial de inferencias", "Lotes persistidos con modelo, F1 y número de filas.")
    runs = repo.list_prediction_runs(limit=30)
    st.dataframe(pd.DataFrame(runs) if runs else pd.DataFrame(), width="stretch", hide_index=True)

    section_title("Bitácora estructurada", "Eventos de auditoría recientes.")
    logs = repo.list_audit_events(limit=60)
    st.dataframe(pd.DataFrame(logs) if logs else pd.DataFrame(), width="stretch", hide_index=True)

    errs = repo.list_system_errors(limit=20)
    if errs:
        section_title("Errores recientes", "Diagnósticos persistidos por los flujos operativos.")
        st.dataframe(pd.DataFrame(errs), width="stretch", hide_index=True)


def render_reports(repo: "IDSMLRepository") -> None:
    if not rbac.can_reports(st.session_state.get("role", "")):
        st.warning("Sin permisos para reportes.")
        return

    page_header(
        "Reportes exportables",
        "Generación de evidencias CSV/PDF con trazabilidad en el repositorio activo.",
        tag="Reports",
    )

    user = str(st.session_state.get("username", "usuario"))
    csv_col, pdf_col = st.columns(2)
    with csv_col:
        render_card("CSV de experimentos", "Exporta métricas de modelos, conteos y resumen operativo.", tone="blue")
        if st.button("Generar CSV de experimentos"):
            path = report_gen.export_summary_csv(repo, user)
            log_action(repo, action="export_csv", module="reportes", result="ok", observation=str(path))
            st.success(f"CSV generado: {path}")
    with pdf_col:
        render_card("PDF ejecutivo", "Resumen visual para revisión académica o institucional.", tone="green")
        if st.button("Generar PDF resumen"):
            path = report_gen.export_summary_pdf(repo, user)
            if path:
                log_action(repo, action="export_pdf", module="reportes", result="ok", observation=str(path))
                st.success(f"PDF generado: {path}")
            else:
                st.warning("No se pudo generar PDF. Revise dependencias o registros disponibles.")

    section_title("Historial de reportes", "Archivos generados y registrados en persistencia.")
    reports = repo.list_reports(limit=20)
    st.dataframe(pd.DataFrame(reports) if reports else pd.DataFrame(), width="stretch", hide_index=True)


def render_database_model(repo: "IDSMLRepository") -> None:
    if not rbac.can_system_status(st.session_state.get("role", "")):
        st.warning("Solo roles TI pueden revisar el modelo de base de datos.")
        return

    page_header(
        "Modelo de base de datos",
        "Vista academica del esquema relacional IDS-ML: tablas, modulos y relaciones principales.",
        tag="Data model",
    )

    try:
        sqlite_schema = read_schema(SQLITE_SCHEMA_PATH)
        tables = parse_tables(sqlite_schema)
    except OSError as exc:
        st.error(f"No se pudo leer el esquema SQL: {exc}")
        return

    relationships_count = sum(len(table.foreign_keys) for table in tables)
    modules_count = len({table.module for table in tables})

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Tablas", format_int(len(tables)), "Modelo relacional", tone="blue")
    with c2:
        metric_card("Relaciones FK", format_int(relationships_count), "Integridad referencial", tone="green")
    with c3:
        metric_card("Modulos", format_int(modules_count), "Agrupacion funcional", tone="amber")
    with c4:
        metric_card("Motor objetivo", "PostgreSQL", "Docker / produccion", tone="slate")

    overview_tab, diagram_tab, sql_tab = st.tabs(["Resumen", "Diagrama ER", "SQL y DBML"])

    with overview_tab:
        section_title("Resumen por modulo", "Conteo de tablas, campos y relaciones documentadas.")
        st.dataframe(summarize_modules(tables), width="stretch", hide_index=True)

        section_title("Inventario de tablas", "Listado verificable para sustentacion y revision tecnica.")
        st.dataframe(summarize_tables(tables), width="stretch", hide_index=True)

    with diagram_tab:
        modules = ["Todos"] + sorted({table.module for table in tables})
        default_index = modules.index("Alertas IDS") if "Alertas IDS" in modules else 0
        selected_module = st.selectbox("Modulo del diagrama", modules, index=default_index)
        st.graphviz_chart(build_relationship_dot(tables, selected_module), width="stretch")
        st.caption("Para revisar todo el modelo en detalle, use el archivo DBML en dbdiagram.io.")

    with sql_tab:
        section_title("Archivos del modelo", "Rutas locales para abrir el esquema en herramientas externas.")
        st.dataframe(
            pd.DataFrame(
                [
                    {"formato": "SQLite", "archivo": str(SQLITE_SCHEMA_PATH)},
                    {"formato": "PostgreSQL", "archivo": str(POSTGRES_SCHEMA_PATH)},
                    {"formato": "DBML / dbdiagram.io", "archivo": str(DBML_PATH)},
                ]
            ),
            width="stretch",
            hide_index=True,
        )

        with st.expander("Ver schema.sql para SQLite"):
            st.code(sqlite_schema, language="sql")

        if POSTGRES_SCHEMA_PATH.exists():
            with st.expander("Ver schema.sql para PostgreSQL"):
                st.code(read_schema(POSTGRES_SCHEMA_PATH), language="sql")

        if DBML_PATH.exists():
            with st.expander("Ver modelo DBML"):
                st.code(DBML_PATH.read_text(encoding="utf-8"), language="sql")


def render_users(repo: "IDSMLRepository") -> None:
    if not rbac.can_system_status(st.session_state.get("role", "")):
        st.warning("Solo roles TI pueden revisar administración de usuarios.")
        return

    page_header(
        "Administración de usuarios y roles",
        "Vista de roles demo y permisos operativos del prototipo. Lista para reemplazo por IAM institucional.",
        tag="RBAC",
    )

    users_df = pd.DataFrame(
        [
            {"usuario": "admin", "rol": "Administrador TI", "estado": "activo", "alcance": "Administración completa"},
            {"usuario": "analista", "rol": "Analista TI", "estado": "activo", "alcance": "Dataset, entrenamiento, inferencia y reportes"},
            {"usuario": "invitado", "rol": "Invitado/demo", "estado": "activo", "alcance": "Lectura y carga demostrativa"},
        ]
    )
    role_df = pd.DataFrame(
        [
            {"permiso": "dataset", "Administrador TI": True, "Analista TI": True, "Invitado/demo": True},
            {"permiso": "entrenamiento", "Administrador TI": True, "Analista TI": True, "Invitado/demo": False},
            {"permiso": "inferencia", "Administrador TI": True, "Analista TI": True, "Invitado/demo": False},
            {"permiso": "alertas", "Administrador TI": True, "Analista TI": True, "Invitado/demo": False},
            {"permiso": "cambio_estado_alerta", "Administrador TI": True, "Analista TI": False, "Invitado/demo": False},
            {"permiso": "reportes", "Administrador TI": True, "Analista TI": True, "Invitado/demo": False},
        ]
    )

    left, right = st.columns([1.25, 1])
    with left:
        section_title("Usuarios demo", "No contiene credenciales reales ni identidad institucional.")
        st.dataframe(users_df, width="stretch", hide_index=True)
    with right:
        section_title("Permisos por rol", "Resumen RBAC aplicado por la capa de seguridad.")
        st.dataframe(role_df, width="stretch", hide_index=True)

    section_title("Trazabilidad de accesos", "Eventos recientes de autenticación y auditoría.")
    logs = repo.list_audit_events(limit=50)
    log_df = pd.DataFrame(logs)
    if not log_df.empty:
        columns = [c for c in ["created_at", "username", "role", "action", "module", "result"] if c in log_df.columns]
        st.dataframe(log_df[columns], width="stretch", hide_index=True)
    else:
        empty_state("Aún no hay eventos de acceso registrados.")


def render_settings(repo: "IDSMLRepository") -> None:
    if not rbac.can_system_status(st.session_state.get("role", "")):
        st.warning("Solo roles TI pueden revisar configuración del sistema.")
        return

    page_header(
        "Configuración del sistema",
        "Parámetros operativos visibles para tesis. Los secretos siguen fuera del código fuente.",
        tag="Settings",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Persistencia activa", _backend_label(repo.backend_name), "Repository factory", tone="blue")
    with c2:
        metric_card("Alertas por lote", "100", "Límite operativo UI", tone="amber")
    with c3:
        metric_card("Ejecución", "Streamlit", "Prototipo local/cloud", tone="green")

    section_title("Configuración no sensible", "Valores esperados por entorno.")
    settings_df = pd.DataFrame(
        [
            {"clave": "IDSML_PERSISTENCE_BACKEND", "propósito": "postgres | sqlite | firestore | auto", "secreto": "no"},
            {"clave": "FIREBASE_PROJECT_ID", "propósito": "Proyecto Firebase/Firestore", "secreto": "sí, fuera del repo"},
            {"clave": "GOOGLE_APPLICATION_CREDENTIALS", "propósito": "Ruta segura a credencial", "secreto": "sí, fuera del repo"},
        ]
    )
    st.dataframe(settings_df, width="stretch", hide_index=True)

    section_title("Buenas prácticas activas", "Controles básicos para revisión académica y Sonar.")
    chip_row(
        [
            ("Secrets fuera del repo", "green"),
            ("SQLite local", "blue"),
            ("Firestore desacoplado", "blue"),
            ("Pruebas pytest", "green"),
            ("Sonar configurado", "amber"),
        ]
    )


def render_system_status(repo: "IDSMLRepository") -> None:
    if not rbac.can_system_status(st.session_state.get("role", "")):
        st.warning("Sin permisos para Estado del sistema.")
        return

    page_header(
        "Estado del sistema",
        "Diagnóstico operativo de persistencia, auditoría, errores, reportes y conectividad Firestore.",
        tag="System status",
    )

    payload = build_status_payload(repo)
    counts = payload.get("conteos", {})
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Persistencia", _backend_label(payload.get("backend", repo.backend_name)), "Repositorio activo", tone="blue")
    with c2:
        metric_card("Bitácora", format_int(counts.get("audit_events", 0)), "Eventos registrados", tone="green")
    with c3:
        metric_card("Errores", format_int(counts.get("system_errors", 0)), "Diagnósticos persistidos", tone="red" if counts.get("system_errors", 0) else "slate")
    with c4:
        metric_card("Reportes", format_int(counts.get("reports", 0)), "Exportaciones", tone="amber")

    section_title("Diagnóstico Firestore", "Ping de conectividad si el backend o las credenciales aplican.")
    ping = firestore_ping_ok()
    if ping is None:
        st.info("Firestore no configurado o no aplica en este backend.")
    elif ping:
        st.success("Conexión Firestore respondió correctamente.")
    else:
        st.error("Firestore no respondió al ping. Revise credenciales o red.")
        try:
            repo.save_system_error("firestore_ping", "Fallo ping Firestore", {"backend": repo.backend_name})
        except Exception:
            pass

    with st.expander("Payload técnico"):
        st.json(payload)


def render_cloud(repo: "IDSMLRepository") -> None:
    page_header(
        "Nube y despliegue",
        "Opciones de ejecución local, Docker y cloud sin exponer secretos ni credenciales.",
        tag="Deployment",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        render_card(
            "Streamlit Cloud / Render",
            "Punto de entrada app.py, configuración por variables de entorno y secretos del proveedor.",
            tone="blue",
        )
    with c2:
        render_card(
            "Firestore + SQLite",
            "Repository Pattern con fallback automático a SQLite cuando Firestore no está disponible.",
            tone="green",
        )
    with c3:
        render_card(
            "Docker",
            "docker compose up conserva data y artifacts mediante volúmenes del proyecto.",
            tone="amber",
        )

    section_title("Variables esperadas", "No escriba secretos en el repositorio.")
    st.code(
        "\n".join(
            [
                "IDSML_PERSISTENCE_BACKEND=postgres|sqlite|firestore|auto",
                "FIREBASE_PROJECT_ID=<project-id>",
                "GOOGLE_APPLICATION_CREDENTIALS=<ruta-segura>",
                "streamlit run app.py",
                "docker compose up",
            ]
        ),
        language="bash",
    )
