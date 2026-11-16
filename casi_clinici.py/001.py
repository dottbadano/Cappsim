import streamlit as st


def render_case(user_role, username):
  # Inizializzazione dello stato di sessione per il caso 001
  if "c001_state" not in st.session_state:
    st.session_state.c001_state = {
        "current_node": "snodo1",
        "vitalita": 100,
        "oncologico": 100,
        "qol": 75,
        "storia": [],
        "binario": "principale",
    }

  state = st.session_state.c001_state

  # Intestazione del caso
  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <span style="background: #3b82f6; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: bold;">CASO 001 — ARENA URO-ONCOLOGICA</span>
            <h2 style="margin: 0.5rem 0 0 0; font-size: 1.5rem;">Il Paziente con RAU, Macroematuria e PSA 12</h2>
            <p style="margin: 0; color: #94a3b8; font-size: 0.95rem;">Gestione multidisciplinare integrata tra ostruzione meccanica, stadiazione radiologica e target molecolari.</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # Layout a due colonne: Sinistra (Cartella Paziente fissa), Destra (Azioni e Bivi)
  col_left, col_right = st.columns([1, 1.8], gap="large")

  with col_left:
    st.markdown("### 📋 Anamnesi & Profilo Paziente")
    st.info(
        """
        * **Paziente:** Uomo, 67 anni, ECOG PS 0.
        * **Anamnesi:** Ipertensione arteriosa in olmesartan 20 mg; dislipidemia in rosuvastatina 10 mg.
        * **Familiarità critica:** **Madre deceduta per carcinoma mammario a 58 anni; fratello operato per carcinoma prostatico a 62 anni.**
        * **Esordio:** Accesso in PS 10 giorni fa per **ritenzione acuta d'urina (RAU)** risolta con catetere Foley 18 Ch + tamsulosina. Giunge oggi in ambulatorio per comparsa da 3 giorni di **macroematuria intermittente con piccoli coaguli**.
        * **Esame obiettivo:** DRE negativa (prostata ~65 cc liscia, parenchimatosa, indolente, cT1c).
        * **Esami ematochimici:** **PSA 12,0 ng/ml**, Hb 13,2 g/dl, Creatinina 1,02 mg/dl, urinocoltura negativa.
        """
    )

    # Indicatori di stato attuali
    st.markdown("### 📊 Parametri Clinici")
    m1, m2, m3 = st.columns(3)
    m1.metric("Vitalità", f"{state['vitalita']}%")
    m2.metric("Controllo Oncologico", f"{state['oncologico']}%")
    m3.metric("Qualità di Vita", f"{state['qol']}%")

    if user_role == "master":
      with st.expander("🛠️ Pannello Control Room (Master Debug)"):
        st.write(f"Nodo attuale: `{state['current_node']}`")
        st.write(f"Binario: `{state['binario']}`")
        if st.button("Reset Caso 001"):
          st.session_state.c001_state = {
              "current_node": "snodo1",
              "vitalita": 100,
              "oncologico": 100,
              "qol": 75,
              "storia": [],
              "binario": "principale",
          }
          st.rerun()

  with col_right:
    # DEFINIZIONE NODI E RAMIFICAZIONI DEL CASO 001
    node = state["current_node"]

    if node == "snodo1":
      st.markdown("### 📍 Snodo 1 — La prima scelta dopo l'accesso in ambulatorio")
      st.write(
          "Il paziente si presenta con catetere a dimora, macroematuria"
          " intermittente, DRE negativa e PSA 12,0 ng/ml. Qual è la tua mossa"
          " diagnostica primaria?"
      )

      with st.form("form_snodo1"):
        scelta = st.radio(
            "Seleziona l'opzione clinica:",
            [
                (
                    "A) rM multiparametrica della prostata + Uretrocistoscopia"
                    " ambulatoriale"
                ),
                (
                    "B) Uro-TC torace-addome-pelvi con mdc per sospetta neoplasia"
                    " uroteliale"
                ),
                (
                    "C) TURP + TURB disostruttiva ed emostatica immediata in"
                    " sala operatoria"
                ),
                (
                    "D) Cistoclisi continua e rivalutazione del PSA a 2 mesi a"
                    " catetere rimosso"
                ),
            ],
        )
        submit = st.form_submit_button("Conferma Scelta", use_container_width=True)

        if submit:
          if scelta.startswith("A"):
            state["vitalita"] += 0
            state["oncologico"] += 10
            state["qol"] += 0
            state["current_node"] = "snodo3"
          elif scelta.startswith("B"):
            state["vitalita"] += 0
            state["oncologico"] -= 5
            state["binario"] = "urotc"
            state["current_node"] = "snodo2_urotc"
          elif scelta.startswith("C"):
            state["vitalita"] -= 5
            state["oncologico"] -= 25
            state["qol"] -= 10
            state["binario"] = "post_turp"
            state["current_node"] = "snodo3"
          else:
            state["vitalita"] -= 5
            state["oncologico"] -= 20
            state["qol"] -= 15
            state["current_node"] = "snodo3"
          st.rerun()

    elif node == "snodo2_urotc":
      st.markdown(
          "### 📍 Snodo 2 — La trappola della Uro-TC e della vescica da sforzo"
      )
      st.write(
          "La Uro-TC mostra una minima ectasia pielocaliceale destra di I"
          " grado e **pareti vescicali diffusamente ispessite, trabecolate e"
          " disomogenee (aspetto da vescica da sforzo)** attorno al Foley, senza"
          " difetti di riempimento ureterali. Come procedi?"
      )

      with st.form("form_snodo2"):
        scelta = st.radio(
            "Seleziona l'opzione clinica:",
            [
                (
                    "A) Ureterorenoscopia (URS) diagnostica destra + biopsie"
                    " vescicali random e citologia"
                ),
                (
                    "B) Uretrocistoscopia ambulatoriale + rM multiparametrica"
                    " della prostata"
                ),
                (
                    "C) Nefroureterectomia destra / posizionamento stent"
                    " ureterale permanente"
                ),
                ("D) Sola sorveglianza ecografica a 6 mesi"),
            ],
        )
        submit = st.form_submit_button("Conferma Scelta", use_container_width=True)

        if submit:
          if scelta.startswith("A"):
            state["vitalita"] -= 10
            state["oncologico"] -= 20
            state["qol"] -= 15
            state["current_node"] = "snodo3"
          elif scelta.startswith("B"):
            state["vitalita"] += 0
            state["oncologico"] += 5
            state["current_node"] = "snodo3"
          elif scelta.startswith("C"):
            state["vitalita"] -= 35
            state["oncologico"] -= 45
            state["qol"] -= 40
            state["current_node"] = "esito_sconfitta"
          else:
            state["vitalita"] -= 15
            state["oncologico"] -= 35
            state["qol"] -= 20
            state["current_node"] = "snodo3"
          st.rerun()

    elif node == "snodo3":
      st.markdown(
          "### 📍 Snodo 3 — rM Prostata Anteriore PI-RADS 5 e Scelta Terapeutica"
          " Primaria"
      )
      st.write(
          "La rM multiparametrica svela una voluminosa lesione anteriore di"
          " **23 mm PI-RADS 5 con estensione extracapsulare anteriore nello"
          " spazio di Retzius (cT3a)** (zona posteriore liscia, confermando la"
          " DRE negativa). Biopsia fusion: **Adenocarcinoma ISUP 5 (Gleason"
          " 4+5)**. PET-PSMA: `miN0 M0`. Tentativo di scateteramento fallito"
          " (catetere a permanenza). Qual è la strategia primaria?"
      )

      with st.form("form_snodo3"):
        scelta = st.radio(
            "Seleziona l'opzione clinica:",
            [
                (
                    "A) Prostatectomia radicale + linfadenectomia pelvica"
                    " estesa (approccio multimodale)"
                ),
                (
                    "B) Radioterapia radicale pelvica + LHRH + ARSI (Abiraterone)"
                    " per 24 mesi"
                ),
                ("C) TURP disostruttiva + Radioterapia immediata"),
                ("D) Sola ADT (LHRH) in attesa di riduzione volumetrica"),
            ],
        )
        submit = st.form_submit_button("Conferma Scelta", use_container_width=True)

        if submit:
          if scelta.startswith("A"):
            state["oncologico"] += 10
            state["qol"] += 20
            state["current_node"] = "snodo4a"
          elif scelta.startswith("B"):
            state["vitalita"] -= 5
            state["oncologico"] += 5
            state["qol"] -= 25
            state["current_node"] = "esito_sconfitta"
          elif scelta.startswith("C"):
            state["vitalita"] -= 10
            state["oncologico"] -= 15
            state["qol"] -= 20
            state["current_node"] = "esito_sconfitta"
          else:
            state["vitalita"] -= 10
            state["oncologico"] -= 30
            state["qol"] -= 20
            state["current_node"] = "esito_sconfitta"
          st.rerun()

    elif node == "snodo4a":
      st.markdown(
          "### 📍 Snodo 4 — Ripresa Biochimica Post-Prostatectomia (PSA 0,42"
          " ng/ml)"
      )
      st.write(
          "Il paziente ha rimosso il catetere in 10ª giornata, è continente e in"
          " ottima forma. A 6 mesi il PSA risale a **0,42 ng/ml** (PSA-DT 4"
          " mesi). Come procedi?"
      )

      with st.form("form_snodo4a"):
        scelta = st.radio(
            "Seleziona l'opzione clinica:",
            [
                (
                    "A) Eseguire PET-PSMA di ristadiazione prima di impostare il"
                    " trattamento"
                ),
                (
                    "B) Radioterapia di salvataggio cieca sulla sola loggia"
                    " prostatica senza PET"
                ),
                (
                    "C) Avviare direttamente ADT (LHRH) continuativa senza"
                    " imaging né RT"
                ),
                ("D) Sorveglianza del solo PSA fino a valori > 2,0 ng/ml"),
            ],
        )
        submit = st.form_submit_button("Conferma Scelta", use_container_width=True)

        if submit:
          if scelta.startswith("A"):
            state["oncologico"] += 10
            state["current_node"] = "snodo5a"
          elif scelta.startswith("B"):
            state["oncologico"] -= 15
            state["qol"] -= 5
            state["current_node"] = "snodo6"
          elif scelta.startswith("C"):
            state["vitalita"] -= 5
            state["oncologico"] -= 20
            state["qol"] -= 10
            state["current_node"] = "snodo6"
          else:
            state["vitalita"] -= 10
            state["oncologico"] -= 25
            state["current_node"] = "snodo6"
          st.rerun()

    elif node == "snodo5a":
      st.markdown(
          "### 📍 Snodo 5 — PET-PSMA di Ristadiazione: Linfonodo Iliaco Comune"
      )
      st.write(
          "La PET-PSMA mostra lieve iperaccumulo in loggia prostatica e un"
          " **linfonodo iliaco comune destro di 9 mm intensamente captante**."
          " Qual è la scelta terapeutica?"
      )

      with st.form("form_snodo5a"):
        scelta = st.radio(
            "Seleziona l'opzione clinica:",
            [
                (
                    "A) RT di salvataggio su loggia e pelvi con boost sul"
                    " linfonodo captante + ADT breve"
                ),
                (
                    "B) Radioterapia sulla sola loggia prostatica ignorando il"
                    " linfonodo iliaco"
                ),
                (
                    "C) Linfadenectomia di salvataggio isolata senza irradiare"
                    " la loggia"
                ),
                ("D) Chemioterapia sistemica con Docetaxel"),
            ],
        )
        submit = st.form_submit_button("Conferma Scelta", use_container_width=True)

        if submit:
          if scelta.startswith("A"):
            state["oncologico"] += 15
            state["current_node"] = "snodo6"
          elif scelta.startswith("B"):
            state["vitalita"] -= 5
            state["oncologico"] -= 20
            state["qol"] -= 5
            state["current_node"] = "snodo6"
          elif scelta.startswith("C"):
            state["vitalita"] -= 10
            state["oncologico"] -= 15
            state["qol"] -= 15
            state["current_node"] = "snodo6"
          else:
            state["vitalita"] -= 10
            state["oncologico"] -= 20
            state["qol"] -= 20
            state["current_node"] = "snodo6"
          st.rerun()

    elif node == "snodo6":
      st.markdown(
          "### 📍 Snodo 6 — Ripartenza Tardiva a 20 Mesi (3 Linfonodi"
          " Retroperitoneali)"
      )
      st.write(
          "Dopo 20 mesi di PSA indosabile, il PSA risale a 1,9 ng/ml. La nuova"
          " PET-PSMA evidenzia **3 linfonodi retroperitoneali para-aortici**"
          " (mHSPC basso volume, paziente naïve agli ARSI). Come procedi?"
      )

      with st.form("form_snodo6"):
        scelta = st.radio(
            "Seleziona l'opzione clinica:",
            [
                (
                    "A) Terapia sistemica con ADT (LHRH) + ARSI (Apalutamide /"
                    " Enzalutamide / Darolutamide)"
                ),
                ("B) Sola ADT (LHRH) in monoterapia"),
                ("C) Re-irradiazione pelvica e retroperitoneale estesa"),
                ("D) Sospensione terapie attive e sole cure palliative"),
            ],
        )
        submit = st.form_submit_button("Conferma Scelta", use_container_width=True)

        if submit:
          if scelta.startswith("A"):
            state["vitalita"] += 5
            state["oncologico"] += 10
            state["current_node"] = "snodo7"
          elif scelta.startswith("B"):
            state["vitalita"] -= 10
            state["oncologico"] -= 20
            state["current_node"] = "snodo7"
          elif scelta.startswith("C"):
            state["vitalita"] -= 20
            state["oncologico"] -= 25
            state["qol"] -= 30
            state["current_node"] = "snodo7"
          else:
            state["vitalita"] -= 40
            state["oncologico"] -= 45
            state["qol"] -= 25
            state["current_node"] = "esito_sconfitta"
          st.rerun()

    elif node == "snodo7":
      st.markdown(
          "### 📍 Snodo 7 — Il PSA Basso che Inganna (PSA 0,18 ng/ml + Dolenzia"
          " Ossea)"
      )
      st.write(
          "A 10 mesi dall'avvio di ADT + ARSI il paziente sta bene ed è senza"
          " catetere. Esami: **PSA 0,18 ng/ml** (stabile). Riferisce però da 3"
          " settimane **dolenzia sorda all'anca destra e al rachide lombare (VAS"
          " 3-4/10)**. Ematochimici: Hb 12,1 g/dl, **Fosfatasi Alcalina (ALP)"
          " 178 U/L** (basale 72 U/L). Come agisci?"
      )

      with st.form("form_snodo7"):
        scelta = st.radio(
            "Seleziona l'opzione clinica:",
            [
                (
                    "A) Ristadiazione strumentale immediata con TC"
                    " torace-addome + Scintigrafia ossea"
                ),
                (
                    "B) Rassicurare il paziente visto il PSA a 0,18 ng/ml,"
                    " prescrivere FANS + MOC/DEXA e controllo a 3 mesi"
                ),
                (
                    "C) Sospendere l'ARSI per sospetta mialgia/artralgia"
                    " iatrogena da farmaco"
                ),
                (
                    "D) Radioterapia antalgica cieca sull'anca destra senza"
                    " ristadiazione sistemica"
                ),
            ],
        )
        submit = st.form_submit_button("Conferma Scelta", use_container_width=True)

        if submit:
          if scelta.startswith("A"):
            state["vitalita"] += 5
            state["oncologico"] += 10
            state["current_node"] = "snodo8"
          elif scelta.startswith("B"):
            state["vitalita"] -= 40
            state["oncologico"] -= 45
            state["qol"] -= 45
            state["current_node"] = "esito_sconfitta"
          elif scelta.startswith("C"):
            state["vitalita"] -= 35
            state["oncologico"] -= 45
            state["qol"] -= 35
            state["current_node"] = "esito_sconfitta"
          else:
            state["vitalita"] -= 20
            state["oncologico"] -= 30
            state["qol"] -= 20
            state["current_node"] = "esito_sconfitta"
          st.rerun()

    elif node == "snodo8":
      st.markdown(
          "### 📍 Snodo 8 — Il Bivio Finale sulle Lesioni Ossee a PSA Soppresso"
