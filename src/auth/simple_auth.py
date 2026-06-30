import streamlit as st

from src.domain.services.auth_service import authenticate


def login(repo=None):
    st.markdown(
        """
        <div class="ids-login-hero">
            <div class="ids-login-mark">+</div>
            <div class="ids-title">IDS-ML Hospital Carrión</div>
            <div class="ids-subtitle" style="max-width:none;">
                Sistema institucional de monitoreo y detección de amenazas
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1.25, 1])
    with center:
        st.markdown(
            """
            <div class="ids-login-card ids-card">
                <div class="ids-card-title">Acceso institucional</div>
                <div class="ids-card-subtitle">
                    Acceso autorizado para personal responsable de seguridad, redes y soporte TI.
                    Las operaciones relevantes quedan registradas para auditoría.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("idsml_login_form", clear_on_submit=False):
            username = st.text_input("Usuario", placeholder="Usuario institucional")
            password = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña")
            submitted = st.form_submit_button("Iniciar sesión", type="primary")

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
                st.error("Credenciales no válidas.")

        st.caption("Uso restringido. Solicite credenciales al administrador del sistema IDS-ML.")
    return st.session_state.get("authenticated", False)


def require_auth():
    if not st.session_state.get("authenticated", False):
        return False
    return True
