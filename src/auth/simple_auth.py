import streamlit as st

from src.domain.services.auth_service import authenticate
from src.ui.theme import institution_logo


def login(repo=None):
    with st.container(key="login_brand"):
        institution_logo()

    st.markdown(
        """
        <div class="ids-login-hero">
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
        with st.form("idsml_login_form", clear_on_submit=False):
            st.markdown(
                """
                <div class="ids-login-form-head">
                    <div class="ids-card-title">Acceso institucional</div>
                    <div class="ids-card-subtitle">Ingrese con sus credenciales autorizadas.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            username = st.text_input("Usuario", placeholder="Ingrese su usuario")
            password = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña")
            st.caption("Acceso demostrativo: la sesión permanece activa en esta pestaña hasta que la cierre.")
            submitted = st.form_submit_button("Iniciar sesión  →", type="primary", use_container_width=True)
            st.markdown(
                '<div class="ids-login-secure">♢ &nbsp; ACCESO RESTRINGIDO Y MONITOREADO</div>',
                unsafe_allow_html=True,
            )

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

        st.markdown(
            """
            <div class="ids-login-footer">
                © 2026 IDS-ML Hospital Carrión · Política de privacidad · Soporte técnico
            </div>
            """,
            unsafe_allow_html=True,
        )
    return st.session_state.get("authenticated", False)


def require_auth():
    if not st.session_state.get("authenticated", False):
        return False
    return True
