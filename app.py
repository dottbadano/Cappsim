import importlib
import os
import streamlit as st

# Configurazione pagina
st.set_page_config(
    page_title="2getSIM - Uro-Oncologia Clinica", page_icon="⚡", layout="wide"
)

# ---------------------------------------------------------------------------
# SISTEMA DI AUTENTICAZIONE (MASTER vs DISCENTI)
# ---------------------------------------------------------------------------
MASTER_CREDENTIALS = {
    "gbadano": "211280",
    "acavo": "211186",
    "smigone": "090286",  # o smigone a seconda di come preferisci digitare
}

# Inizializzazione dello stato di autenticazione
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None  # "master" o "discente"
if "username" not in st.session_state:
    st.session_state.username = None


def login_screen():
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0;">
            <h1>⚡ 2getSIM — Accesso Riservato</h1>
            <p style="color: #666; font-size: 1.1rem;">Corso Residenziale Uro-Oncologico Multidisciplinare</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username_input = st.text_input(
                "Username", placeholder="Inserisci username o ID (es. 001 o gbadano)"
            )
            password_input = st.text_input(
                "Password", type="password", placeholder="Password di accesso"
            )
            submit = st.form_submit_button(
                "Accedi alla Sessione", use_container_width=True
            )

            if submit:
                # Controllo Master (Docenti)
                if username_input in MASTER_CREDENTIALS:
                    if MASTER_CREDENTIALS[username_input] == password_input:
                        st.session_state.authenticated = True
                        st.session_state.user_role = "master"
                        st.session_state.username = username_input
                        st.rerun()
                    else:
                        st.error("Password Master errata.")

                # Controllo Discenti (001 a 016, password unica: 12345678)
                elif username_input.isdigit() and 1 <= int(username_input) <= 16:
                    if password_input == "12345678":
                        st.session_state.authenticated = True
                        st.session_state.user_role = "discente"
                        st.session_state.username = (
                            f"Discente {username_input}"
                        )
                        st.rerun()
                    else:
                        st.error(
                            "Password errata per i discenti (Default: 12345678)."
                        )
                else:
                    st.error(
                        "Credenziali non riconosciute. Verifica username e password."
                    )


if not st.session_state.authenticated:
    login_screen()
    st.stop()

# ---------------------------------------------------------------------------
# MOTORE PRINCIPALE DELL'APPLICAZIONE (DOPO IL LOGIN)
# ---------------------------------------------------------------------------

# Barra laterale di controllo ruolo
with st.sidebar:
    st.markdown(f"### 👤 Utente: **{st.session_state.username}**")
    st.markdown(
        f"**Ruolo:** `{'Docente Master (Control Room)' if st.session_state.user_role == 'master' else 'Discente in Aula'}`"
    )
    if st.button("Disconnetti", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.username = None
        st.rerun()
    st.divider()

# Caricamento dinamico dei casi clinici dalla cartella 'casi_clinici'
CASE_DIR = "casi_clinici"
if not os.path.exists(CASE_DIR):
    os.makedirs(CASE_DIR)
    st.warning(
        f"La cartella '{CASE_DIR}' è stata creata. Inserisci almeno un file `.py` con il caso clinico."
    )
    st.stop()

case_files = [
    f[:-3] for f in os.listdir(CASE_DIR) if f.endswith(".py") and f != "__init__"
]

if not case_files:
    st.error(
        f"Nessun caso clinico trovato nella cartella '{CASE_DIR}/'. Aggiungi un file python con la logica del caso."
    )
    st.stop()

# Selezione del caso clinico
selected_case_name = st.sidebar.selectbox(
    "Seleziona Caso Clinico", case_files, format_func=lambda x: x.replace("_", " ").title()
)

# Import dinamico del modulo del caso clinico
try:
    module = importlib.import_module(f"{CASE_DIR}.{selected_case_name}")
    # Ogni modulo di caso clinico deve esporre una funzione principale 'render_case(user_role, username)'
    if hasattr(module, "render_case"):
        module.render_case(
            st.session_state.user_role, st.session_state.username
        )
    else:
        st.error(
            f"Il modulo '{selected_case_name}.py' non contiene la funzione 'render_case(user_role, username)' richiesta."
        )
except Exception as e:
    st.error(f"Errore nel caricamento del caso clinico: {e}")
