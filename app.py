import streamlit as st

st.set_page_config(page_title="Quiz à décalage", page_icon="❓")

st.title("❓ Quiz de culture générale à décalage")
st.write(
    "Le principe : tu lis la question affichée, "
    "mais tu dois répondre à la question posée il y a N tours."
)

# ----------------------
# QUESTIONS INTÉGRÉES
# ----------------------
# 👉 Tu peux ajouter/enlever des questions à cette liste.
# Format : ("question", "réponse")

QUESTIONS = [
    ("Quelle est la capitale de la France ?", "Paris"),
    ("Quel est le plus grand océan du monde ?", "Pacifique"),
    ("Qui a écrit Les Misérables ?", "Victor Hugo"),
    ("Quelle est la capitale de l’Espagne ?", "Madrid"),
    ("Quel est le plus long fleuve de France ?", "La Loire"),
    ("Qui a écrit Le Petit Prince ?", "Antoine de Saint-Exupéry"),
    ("Quel est l’astre autour duquel la Terre tourne ?", "Soleil"),
    ("Quel sport pratique Kylian Mbappé ?", "Football"),
    ("Quelle est la capitale du Portugal ?", "Lisbonne"),
    ("Qui a découvert l’Amérique en 1492 ?", "Christophe Colomb"),
    ("Qui a réalisé le film Titanic ?", "James Cameron"),
    ("Qui a écrit Germinal ?", "Émile Zola"),
    ("Quelle planète est surnommée la planète rouge ?", "Mars"),
    ("Quel est l’hymne national français ?", "La Marseillaise"),
    ("Quelle est la devise de la République française ?", "Liberté, Égalité, Fraternité"),
]

NB_QUESTIONS = len(QUESTIONS)

if NB_QUESTIONS == 0:
    st.error("Aucune question définie dans le programme.")
    st.stop()

# ----------------------
# PARAMÈTRE : DÉCALAGE
# ----------------------

st.sidebar.header("⚙️ Paramètres")
decalage = st.sidebar.number_input(
    "Décalage (nombre de questions à remonter)",
    min_value=1,
    max_value=min(10, NB_QUESTIONS - 1),
    value=2,
    step=1,
    help="Par exemple : 2 = tu réponds à la question posée 2 tours plus tôt."
)

melanger = st.sidebar.checkbox(
    "Mélanger l'ordre des questions",
    value=True
)

# ----------------------
# SESSION STATE
# ----------------------

if "ordre" not in st.session_state:
    # Liste d'indices [0, 1, 2, ..., NB_QUESTIONS-1]
    st.session_state.ordre = list(range(NB_QUESTIONS))
    if melanger:
        import random
        random.shuffle(st.session_state.ordre)

if "index_courant" not in st.session_state:
    st.session_state.index_courant = 0

if "decalage_actuel" not in st.session_state:
    st.session_state.decalage_actuel = decalage

# Si on change le décalage en cours de route, on le met à jour
st.session_state.decalage_actuel = decalage

# ----------------------
# LOGIQUE PRINCIPALE
# ----------------------

index_courant = st.session_state.index_courant

if index_courant >= NB_QUESTIONS:
    st.success("🎉 Fin du quiz ! Toutes les questions ont été posées.")
    st.write("Tu peux recharger la page (Ctrl+R) pour recommencer.")
    st.stop()

# Indice de la question actuelle dans la liste QUESTIONS
q_idx = st.session_state.ordre[index_courant]
question_actuelle, _ = QUESTIONS[q_idx]

st.markdown(f"### ❓ Question actuelle\n**{question_actuelle}**")

# On calcule l'indice de la question à laquelle il faut répondre
index_pour_reponse = index_courant - st.session_state.decalage_actuel

if index_pour_reponse >= 0:
    st.write("---")
    st.markdown("### 💬 Réponds maintenant à cette question précédente :")

    q_rep_idx = st.session_state.ordre[index_pour_reponse]
    question_a_repondre, bonne_reponse = QUESTIONS[q_rep_idx]

    st.markdown(f"**Question (il y a {st.session_state.decalage_actuel} tours) :** {question_a_repondre}")

    # Input spécifique à cet index pour ne pas réutiliser les anciennes réponses
    user_input = st.text_input(
        "Ta réponse :",
        key=f"rep_{index_courant}"
    )

    if user_input:
        if user_input.strip().lower() == bonne_reponse.strip().lower():
            st.success("✅ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. La bonne réponse était : **{bonne_reponse}**")

else:
    st.info(
        f"Le décalage est de {st.session_state.decalage_actuel} questions. "
        "Les premières questions servent à remplir la mémoire avant de commencer à répondre."
    )

# ----------------------
# BOUTON SUIVANT
# ----------------------

if st.button("➡️ Question suivante"):
    st.session_state.index_courant += 1
    st.experimental_rerun()
