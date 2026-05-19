import streamlit as st

from src.domain.services.auth_service import authenticate
from src.ui.theme import page_header


def login(repo=None):
    page_header(
        "Acceso institucional",
        "Plataforma IDS-ML para monitoreo de trafico, evaluacion de amenazas y trazabilidad de alertas.",
        kicker="IDS-ML Core",
        tag="Acceso seguro",
    )

    left, center, right = st.columns([1, 1.25, 1])
    with center:
        st.markdown(
            """
            <div class="ids-login-card ids-card">
                <div class="ids-card-title">Ingreso al sistema</div>
                <div class="ids-card-subtitle">
                    Acceso autorizado para personal responsable de seguridad, redes y soporte TI.
                    Las operaciones relevantes quedan registradas para auditoria.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("idsml_login_form", clear_on_submit=False):
            username = st.text_input("Usuario", placeholder="Usuario institucional")
            password = st.text_input("Contrasena", type="password", placeholder="Ingrese su contrasena")
            submitted = st.form_submit_button("Ingresar al sistema")

        if submitted:
            user = authenticate(username, password)
            if user is not None:
                st.session_state["authenticated"] = True
                st.session_state["username"] = user.username
                st.session_state["role"] = user.role
                if repo is not None:
                    try:
                        repo.save_audit_event(
                            username=user.username,
                            role=user.role,
                            action="inicio_sesion",
                            module="auth",
                            result="ok",
                            observation="",
                        )
                    except Exception:
                        pass
                st.rerun()
            else:
                st.error("Credenciales no validas.")

        st.caption("Uso restringido. Solicite credenciales al administrador del sistema IDS-ML.")
    return st.session_state.get("authenticated", False)


def require_auth():
    if not st.session_state.get("authenticated", False):
        return False
    return True
