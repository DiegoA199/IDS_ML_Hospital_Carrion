"""Páginas Streamlit del IDS-ML (orquestación de UI, sin lógica ML pesada)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import pandas as pd
import plotly.express as px
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
from src.models.trainer import select_best_model, train_and_evaluate
from src.preprocessing.pipeline import prepare_dataset
from src.reports import generator as report_gen
from src.security import rbac
from src.services.dashboard_service import build_dashboard_context
from src.services.system_status_service import build_status_payload, firestore_ping_ok

if TYPE_CHECKING:
    from src.storage.base_repository import IDSMLRepository


def _init_session():
    if "df" not in st.session_state:
        st.session_state["df"] = None
    if "results" not in st.session_state:
        st.session_state["results"] = None
    if "best_model" not in st.session_state:
        st.session_state["best_model"] = None
    if "last_pred_df" not in st.session_state:
        st.session_state["last_pred_df"] = None


def render_dashboard(repo: IDSMLRepository) -> None:
    _init_session()
    st.subheader("Dashboard operativo")
    ctx = build_dashboard_context(repo)
    counts = ctx["counts"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Backend", repo.backend_name)
    act = ctx.get("active_model") or {}
    c2.metric("Modelo activo (registro)", act.get("model_name", "—")[:24] or "—")
    c3.metric("Registros predichos (filas)", counts.get("prediction_rows", 0))
    c4.metric("Amenazas detectadas (pred.)", counts.get("amenazas_detectadas", 0))
    c5, c6, c7 = st.columns(3)
    c5.metric("Experimentos", counts.get("experiments", 0))
    c6.metric("Alertas almacenadas", counts.get("alerts", 0))
    c7.metric("Ejecuciones inferencia", counts.get("prediction_runs", 0))

    if ctx.get("best_f1_session") is not None:
        st.caption(f"Mejor F1 en historial reciente de experimentos: **{ctx['best_name_session']}** ({ctx['best_f1_session']:.4f})")

    if st.session_state.get("results"):
        metrics_df = pd.DataFrame([{"modelo": r.name, **r.metrics} for r in st.session_state["results"]])
        st.subheader("Comparación sesión actual")
        st.dataframe(metrics_df, use_container_width=True)
        fig = px.bar(metrics_df, x="modelo", y="f1_score", title="F1-score (sesión actual)")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Alertas por severidad (muestra reciente)")
    sev = ctx.get("severity_distribution") or {}
    if sev:
        st.bar_chart(pd.Series(sev))
    else:
        st.info("Sin alertas en la muestra.")

    st.subheader("Últimas alertas")
    ra = ctx.get("recent_alerts") or []
    st.dataframe(pd.DataFrame(ra) if ra else pd.DataFrame(), use_container_width=True)

    st.subheader("Últimos eventos de bitácora")
    ev = ctx.get("recent_audit") or []
    st.dataframe(pd.DataFrame(ev) if ev else pd.DataFrame(), use_container_width=True)


def render_dataset(repo: IDSMLRepository) -> None:
    _init_session()
    if not rbac.can_access_dataset(st.session_state.get("role", "")):
        st.warning("Sin permisos para este módulo.")
        return
    st.subheader("Carga y perfilado del dataset")
    uploaded = st.file_uploader("Cargar CSV de tráfico de red o dataset IDS", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.session_state["df"] = df
        st.success("Dataset cargado correctamente")
        st.dataframe(df.head(20), use_container_width=True)
        profile = profile_dataframe(df)
        st.json(profile)
        if df.shape[1] > 0:
            st.write("Distribución preliminar de columnas")
            st.write(df.dtypes.astype(str))
        log_action(
            repo,
            action="carga_dataset",
            module="dataset",
            result="ok",
            observation=f"filas={len(df)}, columnas={df.shape[1]}",
        )


def render_training(repo: IDSMLRepository) -> None:
    _init_session()
    if not rbac.can_train(st.session_state.get("role", "")):
        st.warning("Solo personal TI (Administrador o Analista) puede entrenar modelos.")
        return
    st.subheader("Entrenamiento y evaluación de modelos")
    df = st.session_state.get("df")
    if df is None:
        st.warning("Primero cargue un dataset en el módulo Dataset.")
        return
    target_col = st.selectbox("Seleccione columna objetivo/clase", list(df.columns))
    if st.button("Entrenar y comparar modelos"):
        with st.spinner("Preparando datos y entrenando modelos..."):
            prepared = prepare_dataset(df, target_col)
            results = train_and_evaluate(
                prepared.X_train,
                prepared.X_test,
                prepared.y_train,
                prepared.y_test,
            )
            best = select_best_model(results)
            st.session_state["results"] = results
            st.session_state["best_model"] = best
            for r in results:
                repo.save_experiment(r.name, r.metrics)
            bundle_path = save_model_bundle(
                best.model,
                prepared,
                model_name=best.name,
                f1_score=best.metrics.get("f1_score", 0.0),
            )
            vlabel = f"v-{datetime.now().strftime('%Y%m%dT%H%M%S')}"
            repo.register_model_version(
                model_name=best.name,
                f1_score=float(best.metrics.get("f1_score", 0.0)),
                bundle_path=str(bundle_path),
                version_label=vlabel,
            )
        log_action(
            repo,
            action="entrenamiento_completo",
            module="entrenamiento",
            result="ok",
            observation=f"mejor={best.name}, f1={best.metrics.get('f1_score')}, bundle={bundle_path}, version={vlabel}",
        )
        st.success(f"Mejor modelo: **{best.name}**. Artefacto: `{bundle_path}` (versión **{vlabel}**).")
    if st.session_state.get("results"):
        results = st.session_state["results"]
        metrics_df = pd.DataFrame([{"modelo": r.name, **r.metrics} for r in results])
        st.dataframe(metrics_df, use_container_width=True)
        best = st.session_state["best_model"]
        st.subheader("Matriz de confusión del mejor modelo")
        st.write(best.confusion_matrix)


def render_inference(repo: IDSMLRepository) -> None:
    _init_session()
    if not rbac.can_infer(st.session_state.get("role", "")):
        st.warning("Solo personal TI autorizado puede ejecutar inferencia.")
        return
    st.subheader("Inferencia sobre tráfico nuevo")
    st.markdown(
        "CSV **sin** columna objetivo, con las mismas características que el entrenamiento. "
        "Flujo: preprocesamiento → modelo activo → predicción → alertas → persistencia."
    )
    bundle_upload = st.file_uploader("Bundle .joblib (opcional)", type=["joblib"])
    bundle_path = default_bundle_path()
    if bundle_upload is not None:
        bundle_path.parent.mkdir(parents=True, exist_ok=True)
        bundle_path = bundle_path.parent / "uploaded_infer_bundle.joblib"
        bundle_path.write_bytes(bundle_upload.getbuffer())
    try:
        bundle = load_model_bundle(bundle_path)
    except FileNotFoundError:
        st.warning(f"No hay modelo en `{default_bundle_path()}`. Entrene primero.")
        return
    st.caption(
        f"Modelo: **{bundle.model_name}** | F1 al guardar: **{bundle.f1_score:.4f}** | "
        f"Entrenado: `{bundle.trained_at}` | Features: {len(bundle.feature_columns)}"
    )
    uploaded_infer = st.file_uploader("CSV de registros nuevos", type=["csv"], key="infer_csv")
    if uploaded_infer is not None:
        df_new = pd.read_csv(uploaded_infer)
        if st.button("Generar predicciones", key="btn_predict"):
            with st.spinner("Pipeline + modelo…"):
                pred_df = predict_dataframe(bundle, df_new)
                st.session_state["last_pred_df"] = pred_df
            log_action(repo, action="prediccion_lote", module="inferencia", result="ok", observation=f"filas={len(pred_df)}")
            st.success(f"Predicciones listas ({len(pred_df)} filas).")
    pred_df = st.session_state.get("last_pred_df")
    if pred_df is not None:
        st.dataframe(pred_df, use_container_width=True)
        max_alerts = 100
        if st.button("Persistir predicciones, filas y alertas", key="btn_register_infer"):
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
            n_alert = min(len(pred_df), max_alerts)
            for _, row in pred_df.head(max_alerts).iterrows():
                prob = None
                if "confianza" in pred_df.columns and pd.notna(row["confianza"]):
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
            st.success(f"Run **{run_id}**: filas detalle, {n_alert} alertas y bitácora registradas.")


def render_alerts(repo: IDSMLRepository) -> None:
    if not rbac.can_manage_alerts(st.session_state.get("role", "")):
        st.warning("Sin permisos para gestión de alertas.")
        return
    st.subheader("Centro de alertas TI")
    st.caption("Las alertas automáticas provienen del módulo **Inferencia**.")
    if rbac.can_manual_alert_demo(st.session_state.get("role", "")):
        prediction = st.text_input("Alerta manual (prueba)", value="ataque")
        if st.button("Registrar alerta manual"):
            alert = build_alert(prediction, backend=repo.backend_name)
            repo.save_alert(alert)
            log_action(repo, action="alerta_manual", module="alertas", result="ok", observation=prediction)
            st.success("Alerta registrada")
    alerts = repo.list_alerts(limit=200)
    st.subheader("Historial de alertas")
    st.dataframe(pd.DataFrame(alerts) if alerts else pd.DataFrame(), use_container_width=True)

    if rbac.can_change_alert_status(st.session_state.get("role", "")):
        st.subheader("Cambiar estado (Administrador TI)")
        aid = st.text_input("ID alerta (UUID o id numérico SQLite)", "")
        status = st.selectbox("Nuevo estado", ["nueva", "revisada", "cerrada"])
        if st.button("Actualizar estado") and aid:
            ok = repo.update_alert_status(aid, status, st.session_state.get("role", ""))
            st.success("Actualizado.") if ok else st.error("No se encontró la alerta.")

    st.subheader("Historial de inferencias")
    runs = repo.list_prediction_runs(limit=30)
    st.dataframe(pd.DataFrame(runs) if runs else pd.DataFrame(), use_container_width=True)

    st.subheader("Bitácora estructurada")
    logs = repo.list_audit_events(limit=60)
    st.dataframe(pd.DataFrame(logs) if logs else pd.DataFrame(), use_container_width=True)

    errs = repo.list_system_errors(limit=20)
    if errs:
        st.subheader("Errores recientes")
        st.dataframe(pd.DataFrame(errs), use_container_width=True)


def render_reports(repo: IDSMLRepository) -> None:
    if not rbac.can_reports(st.session_state.get("role", "")):
        st.warning("Sin permisos para reportes.")
        return
    st.subheader("Reportes exportables")
    user = str(st.session_state.get("username", "usuario"))
    if st.button("Generar CSV de experimentos"):
        path = report_gen.export_summary_csv(repo, user)
        log_action(repo, action="export_csv", module="reportes", result="ok", observation=str(path))
        st.success(f"CSV generado: `{path}`")
    if st.button("Generar PDF resumen (Matplotlib)"):
        p = report_gen.export_summary_pdf(repo, user)
        if p:
            log_action(repo, action="export_pdf", module="reportes", result="ok", observation=str(p))
            st.success(f"PDF: `{p}`")
        else:
            st.warning("No se pudo generar PDF (dependencia o error).")
    reps = repo.list_reports(limit=20)
    st.dataframe(pd.DataFrame(reps) if reps else pd.DataFrame(), use_container_width=True)


def render_system_status(repo: IDSMLRepository) -> None:
    if not rbac.can_system_status(st.session_state.get("role", "")):
        st.warning("Sin permisos para Estado del sistema.")
        return
    st.subheader("Estado del sistema")
    payload = build_status_payload(repo)
    st.json(payload)
    st.write("**Firestore (diagnóstico)**")
    ping = firestore_ping_ok()
    if ping is None:
        st.info("Firestore no configurado o no aplica en este backend.")
    elif ping:
        st.success("Conexión Firestore respondió correctamente (ping).")
    else:
        st.error("Firestore no respondió al ping (revisar credenciales / red).")
        try:
            repo.save_system_error("firestore_ping", "Fallo ping Firestore", {"backend": repo.backend_name})
        except Exception:
            pass


def render_cloud(repo: IDSMLRepository) -> None:
    st.subheader("Nube y despliegue")
    st.markdown(
        """
    - **Streamlit Cloud** o **Render** para la interfaz.  
    - **Firestore** + **SQLite** (fallback automático).  
    - Variables: `IDSML_PERSISTENCE_BACKEND`, `FIREBASE_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS`.  
    - Ver `.streamlit/secrets.toml.example`. No versionar secretos ni `.db` con datos sensibles.  
    - **Docker**: `docker compose up` desde la raíz del proyecto.
    """
    )
