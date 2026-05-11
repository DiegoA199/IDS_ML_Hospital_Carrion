import streamlit as st

USERS = {
    "admin": {"password": "admin123", "role": "Administrador TI"},
    "analista": {"password": "analista123", "role": "Analista TI"},
    "invitado": {"password": "invitado123", "role": "Invitado/demo"},
}

ROLE_ADMIN = "Administrador TI"


def login(repo=None):
    st.sidebar.subheader("Acceso IDS-ML")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user["role"]
            st.sidebar.success(f"Bienvenido: {user['role']}")
            if repo is not None:
                try:
                    repo.save_audit_event(
                        username=username,
                        role=user["role"],
                        action="inicio_sesion",
                        module="auth",
                        result="ok",
                        observation="",
                    )
                except Exception:
                    pass
        else:
            st.sidebar.error("Credenciales no válidas")
    return st.session_state.get("authenticated", False)


def require_auth():
    if not st.session_state.get("authenticated", False):
        st.info("Ingrese con un usuario demo para continuar.")
        return False
    return True
