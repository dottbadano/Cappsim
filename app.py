import streamlit as st
import os
import json
import re

st.set_page_config(page_title="CAPPSIM - Debug Mode", layout="wide")

st.title("🩺 CAPPSIM — Diagnostica di Avvio")

try:
    st.write("### 1. Controllo Ambiente")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    st.write(f"- Cartella dello script (`base_dir`): `{base_dir}`")
    st.write(f"- Directory di lavoro corrente: `{os.getcwd()}`")
    
    casi_dir = os.path.join(base_dir, "casi")
    st.write(f"- Percorso cartella 'casi': `{casi_dir}`")
    st.write(f"- La cartella 'casi' esiste?: **{os.path.exists(casi_dir)}**")

    if os.path.exists(casi_dir):
        contents = os.listdir(casi_dir)
        st.write(f"- Contenuto della cartella 'casi': `{contents}`")
        
        for item in contents:
            item_path = os.path.join(casi_dir, item)
            if os.path.isdir(item_path):
                st.write(f"  - Sottocartella trovata: `{item}`")
                json_path = os.path.join(item_path, "scenario.json")
                st.write(f"    - 'scenario.json' presente?: `{os.path.exists(json_path)}`")
                if os.path.exists(json_path):
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        st.success(f"    - 'scenario.json' letto con successo! Titolo: *{data.get('titolo', 'Senza titolo')}*")
                    except Exception as e:
                        st.error(f"    - ❌ Errore nel parsing del JSON in `{json_path}`: {e}")

    st.write("---")
    st.success("✅ Il motore di diagnostica ha eseguito tutti i controlli senza crashare.")

except Exception as e:
    st.error(f"❌ SI È VERIFICATO UN CRASH CRITICO NELLO SCRIPT:")
    st.exception(e)
