import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- Audio setup with edge-tts -----
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

def run_async_with_timeout(coro, timeout=30):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(asyncio.wait_for(coro, timeout=timeout))
    finally:
        loop.close()

async def save_speech(text, file_path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)

def generate_audio(text, output_path, voice):
    if not EDGE_TTS_AVAILABLE:
        raise Exception("edge-tts not installed")
    run_async_with_timeout(save_speech(text, output_path, voice))

VOICE = "fr-FR-DeniseNeural"

st.set_page_config(page_title="Let's Learn French with Gesner", layout="wide")

# ========== STYLING ==========
def set_french_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0a0f2a, #1a1f3a, #0a0f2a); }
        .main-header { background: linear-gradient(135deg, #005f73, #0a9396, #94d2bd); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: white !important; }
        .stTabs [role="tab"] { color: white !important; background: rgba(0,95,115,0.2); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: #005f73; color: black !important; }
        .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: white !important; }
        .stButton button { background-color: #005f73; color: white; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #0a9396; color: black; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #0a0f2a, #1a1f3a); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #1a1f3a; border: 1px solid #0a9396; border-radius: 10px; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox svg { fill: white; }
        div[data-baseweb="popover"] ul { background-color: #1a1f3a; border: 1px solid #0a9396; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #1a1f3a; }
        div[data-baseweb="popover"] li:hover { background-color: #0a9396; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#94d2bd" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#005f73"/>
                    <stop offset="50%" stop-color="#0a9396"/>
                    <stop offset="100%" stop-color="#94d2bd"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">🇫🇷</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ========== AUTHENTICATION ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_french_style()
    st.title("🔐 Accès requis")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Apprenons le français avec Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94d2bd;'>20 leçons – Conversations, vocabulaire, expressions, grammaire, rédaction</p>", unsafe_allow_html=True)
        password_input = st.text_input("Entrez le mot de passe pour accéder", type="password")
        if st.button("Se connecter"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect. Accès refusé.")
    st.stop()

set_french_style()
st.markdown("""
<div class="main-header">
    <h1>🇫🇷 Apprenons le français avec Gesner</h1>
    <p>20 leçons interactives | Conversations | Vocabulaire | Expressions | Grammaire | Rédaction | Audio</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Choisissez une leçon")
    lesson_number = st.selectbox("Leçon", list(range(1, 21)), index=0)
    st.markdown("---")
    st.markdown("### 📚 Votre progression")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ Leçon {lesson_number} sur 20 complétée")
    st.markdown("---")
    st.markdown("**Fondateur et développeur :**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp : (509) 4738-5663")
    st.markdown("📧 Email : deslandes78@gmail.com")
    st.markdown("🌐 [Site principal](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Prix")
    st.markdown("**299 USD** (livre complet – 20 leçons, code source, certificat)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("Tous droits réservés")
    st.markdown("---")
    if st.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ========== CONVERSATIONS NATURELLES (sans astérisques) ==========
def generer_conversation(lesson_num):
    """
    Retourne une liste de 3 conversations en français entre Ita et Kettely.
    Format propre, sans **, avec alternance naturelle.
    """
    themes = [
        (1, "l'enfance de Tiboul – sa curiosité", "Il démontait tout pour comprendre comment ça marche."),
        (2, "trouver un vieil ordinateur à la poubelle", "C'est là qu'il est tombé amoureux de la technologie."),
        (3, "apprendre l'anglais sur YouTube", "Il regardait des tutoriels toute la nuit, même avec une connexion lente."),
        (4, "son premier programme : une calculatrice", "Pour nous, c'était un miracle."),
        (5, "créer un logiciel de facturation pour un petit magasin", "Le propriétaire l'a payé avec un sac de riz."),
        (6, "le bouche‑à‑oreille et ses premiers contrats", "Il n'avait que 17 ans, mais sa réputation grandissait."),
        (7, "fonder GlobalInternet.py", "Il a dit : 'Maman, je vais construire des logiciels pour le monde entier.'"),
        (8, "engager ses propres enfants", "Aujourd'hui, Gesner Junior, Roosevelt, Sebastien et Zendaya travaillent avec lui."),
        (9, "comment il enseigne le code à ses enfants", "Il leur fait construire de vrais projets, pas seulement des exercices."),
        (10, "les enfants créent leur première application ensemble", "Un jeu pour attraper de l'argent – très mignon."),
        (11, "premier client international (Canada)", "Il était nerveux, mais l'affaire s'est parfaitement déroulée."),
        (12, "utiliser son succès pour aider les jeunes Haïtiens", "Il donne des ateliers gratuits à Port‑au‑Prince."),
        (13, "son approche de résolution de problèmes", "Il lit des articles de recherche puis construit des prototypes."),
        (14, "les outils IA qu'il a créés pour les médecins et étudiants", "Aujourd'hui, les hôpitaux utilisent son livre de terminologie médicale."),
        (15, "voir ses petits‑enfants apprendre le code", "Kettely a dit : 'Ita, notre sang coule dans leurs doigts.'"),
        (16, "quatre générations d'apprenants dans la famille Deslandes", "De Tiboul au petit bébé Gesner."),
        (17, "conseils pour les parents", "N'abandonnez jamais les idées folles de votre enfant."),
        (18, "conseils pour les enfants", "Vous n'avez pas besoin d'une école chic – juste de curiosité et de persévérance."),
        (19, "le message de Gesner au monde", "Le savoir est la seule chose qu'on ne peut pas vous enlever."),
        (20, "que nos âmes reposent en paix", "Car ce qu'il a bâti continuera d'enseigner longtemps après nous.")
    ]
    idx = (lesson_num - 1) // 2
    if idx >= len(themes):
        idx = len(themes) - 1
    theme, phrase1, phrase2 = themes[idx]
    
    # Conversation 1
    conv1 = f"""Ita : Kettely, tu te souviens de {theme} ?
Kettely : Oh oui, Ita. {phrase1}
Ita : Et puis {phrase2}
Kettely : Ce garçon ne nous a jamais cessé d'émerveiller.
Ita : Il était toujours si concentré. Même quand nous n'avions pas d'argent, il trouvait une solution.
Kettely : Regarde‑le maintenant. Un véritable scientifique et entrepreneur.
Ita : Et il enseigne la même chose à ses propres enfants.
Kettely : Gesner Junior, Roosevelt, Sebastien, Zendaya – ils suivent tous ses traces.
Ita : C'est notre plus grande récompense, Kettely.
Kettely : En effet. Que nos âmes reposent en paix, sachant que le savoir est désormais leur guide."""
    
    # Conversation 2
    conv2 = f"""Kettely : Ita, je pensais à comment Gesner a lutté pour apprendre la programmation.
Ita : Il n'avait même pas un vrai ordinateur au début. Il utilisait la vieille machine de la bibliothèque.
Kettely : Et quand elle est tombée en panne, il l'a réparée lui‑même !
Ita : C'est là que j'ai su qu'il deviendrait ingénieur.
Kettely : Aujourd'hui, il construit des entreprises entières depuis son ordinateur portable.
Ita : Et il vend ses produits à des clients du monde entier.
Kettely : Tu te souviens de son premier logiciel vendu 20 dollars ? Il était si heureux.
Ita : Maintenant ses formations coûtent 299 dollars, et les gens sont ravis de payer.
Kettely : Parce qu'ils savent qu'ils reçoivent une vraie valeur.
Ita : C'est la différence – il donne du savoir, pas seulement du code.
Kettely : Et il apprend à ses enfants à faire de même.
Ita : Ils deviendront autonomes, tout comme lui.
Kettely : Et puis ils enseigneront à leurs propres enfants.
Ita : Voilà l'héritage d'un véritable éducateur."""
    
    # Conversation 3
    conv3 = f"""Ita : Kettely, quel conseil donnerais‑tu aux autres parents ?
Kettely : Croyez aux rêves de votre enfant, même s'ils semblent impossibles.
Ita : Et pour les enfants ?
Kettely : N'arrêtez jamais d'apprendre. Utilisez Internet. Construisez des choses. Échouez, puis réessayez.
Ita : Gesner a échoué maintes fois, mais il n'a jamais abandonné.
Kettely : Voilà pourquoi il en est là aujourd'hui.
Ita : Il enseigne maintenant cette leçon à ses propres enfants.
Kettely : Et ils construisent déjà leurs propres logiciels.
Ita : Gesner Junior apprend Python, Roosevelt conçoit des sites web.
Kettely : Sebastien maîtrise l'IA, et Zendaya organise toute l'entreprise familiale.
Ita : Ensemble, ils changeront Haïti et le monde.
Kettely : Puissions‑nous reposer en paix, sachant que notre sang porte la graine de l'innovation.
Ita : Et que Dieu les guide toujours.
Kettely : Amen."""
    
    return [conv1, conv2, conv3]

# ========== LISTES DE BASE (vocabulaire, expressions, grammaire, sujets de rédaction) ==========
vocabulaire_fr = [
    "abandonner", "absorber", "abondant", "accélérer", "accessible", "accommoder", "accompagner", "accomplir",
    "accusé", "atteindre", "reconnaître", "acquérir", "adapter", "adéquat", "ajuster", "admirer", "admettre",
    "adopter", "avancer", "défenseur", "affecter", "agréger", "allouer", "anticiper", "apparent", "appel",
    "appliquer", "approcher", "approprié", "approximatif", "arbitraire", "évaluer", "assigner", "assister",
    "supposer", "assurer", "atteindre", "tenter", "attribut", "authentique", "autoriser", "automatiser",
    "disponible", "moyen", "éviter", "conscient", "bénéfique", "bref", "large", "capable", "cause", "défi",
    "caractéristique", "clarifier", "cohérent", "coïncider", "s'effondrer", "combiner", "commencer", "commentaire",
    "commission", "engager", "marchandise", "communiquer", "comparer", "compenser", "concourir", "compiler",
    "compléter", "compliquer", "se conformer", "composer", "comprendre", "compréhensif", "comprimer", "comprendre",
    "compromis", "cacher", "concéder", "se concentrer", "concept", "concerner", "conclure", "simultané", "condenser",
    "condition", "conduire", "conférer", "avouer", "confiner", "confirmer", "conflit", "se conformer", "affronter",
    "confondre", "se rassembler", "conjecture", "connecter", "consentir", "conserver", "considérer", "consister",
    "consolider", "visible", "constant", "constituer", "contraindre", "construire", "consulter", "consommer",
    "contacter", "contenir", "contempler", "contemporain", "contester", "contexte", "contrat", "contredire",
    "contraire", "contribuer", "contrôler", "controversé", "convoquer", "pratique", "converger", "converser",
    "convertir", "transmettre", "convaincre", "coopérer", "coordonner", "faire face", "noyau", "corporatif",
    "correspondre", "corrompu", "conseiller", "comptoir", "contrepartie", "cours", "couvrir", "couverture", "artisanat",
    "créer", "crédible", "crédit", "crise", "critères", "critique", "crucial", "brut", "réduire", "curieux",
    "actuel", "réduire", "coutume", "cycle", "dommage", "débat", "décennie", "décent", "décider", "déclarer",
    "déclin", "diminuer", "consacrer", "juger", "défaut", "défendre", "différer", "définir", "précis", "déléguer",
    "supprimer", "délibéré", "délicat", "livrer", "exiger", "démontrer", "dénoter", "nier", "partir", "dépendre",
    "dépeindre", "déployer", "déposer", "déprimer", "dériver", "descendre", "décrire", "mériter", "concevoir",
    "malgré", "destiner", "détruire", "détail", "détecter", "dissuader", "déterminer", "développer", "dévier",
    "dispositif", "concevoir", "consacrer", "diagramme", "différencier", "difficile", "diffuser", "diluer",
    "diminuer", "direct", "désactiver", "être en désaccord", "disparaître", "catastrophe", "jeter", "discerner",
    "décharger", "discipline", "divulguer", "réduction", "découvrir", "discriminer", "discuter", "maladie", "disgrâce",
    "déguiser", "ne pas aimer", "rejeter", "désordre", "déplacer", "afficher", "disposer", "dispute", "ignorer",
    "dissoudre", "distinct", "distinguer", "déformer", "distraire", "détresse", "distribuer", "district", "déranger",
    "diverger", "divers", "détourner", "diviser", "divin", "divorce", "documenter", "domaine", "domestique",
    "dominer", "donner", "brouillon", "drame", "drastique", "inconvénient", "crainte", "dérive", "sécheresse",
    "double", "stupide", "dupliquer", "durée", "dynamique", "sincère", "facilité", "excentrique", "écho", "économique",
    "bord", "éditer", "éduquer", "effet", "efficace", "efficient", "effort", "élaborer", "élire", "élégant", "élément",
    "élever", "susciter", "éligible", "éliminer", "élite", "éloquent", "ailleurs", "émerger", "éminent", "émettre",
    "émotion", "emphase", "autonomiser", "permettre", "promulguer", "rencontrer", "encourager", "mettre en danger",
    "effort", "approuver", "endurer", "faire respecter", "engager", "améliorer", "apprécier", "agrandir", "éclairer",
    "enrôler", "énorme", "enrichir", "inscrire", "assurer", "entrer", "divertir", "enthousiasme", "entier", "intituler",
    "entité", "entrée", "entrepreneur", "énumérer", "envisager", "épisode", "égal", "équiper", "équivalent", "ériger",
    "éroder", "erratique", "erreur", "éruption", "essai", "essence", "essentiel", "établir", "domaine", "estime",
    "estimer", "éternel", "éthique", "évaluer", "s'évaporer", "éventuel", "preuve", "évident", "évoluer", "exact",
    "exagérer", "dépasser", "exceller", "sauf", "excès", "échanger", "exciter", "exclure", "excuse", "exécuter",
    "exempter", "exercice", "exercer", "épuiser", "exposer", "exil", "exister", "sortie", "élargir", "attendre",
    "expédier", "expulser", "dépenser", "dépense", "expérience", "expert", "expliquer", "explicite", "exploser",
    "exploiter", "explorer", "exposer", "exprimer", "étendre", "étendue", "extérieur", "externe", "éteint", "extraire",
    "extra", "extraordinaire", "extrême", "fabriquer", "faciliter", "facteur", "faculté", "faible", "juste", "foi",
    "faux", "tromperie", "familier", "fantaisie", "fantasme", "tarif", "fasciner", "mode", "fatal", "fatigue",
    "défaut", "faisable", "caractéristique", "fédéral", "faible", "retour", "fertile", "féroce", "final", "finances",
    "fini", "ferme", "réparer", "défaut", "flexible", "prospérer", "fluctuer", "concentrer", "interdire", "force",
    "prévoir", "premier", "forger", "formel", "format", "ancien", "formule", "à venir", "fortune", "fondation",
    "fraction", "fragile", "fragment", "cadre", "fréquent", "frais", "frontière", "frustrer", "accomplir", "fonction",
    "fondamental", "fuser", "futur", "gagner", "rassembler", "genre", "générer", "généreux", "authentique", "gigantesque",
    "global", "objectif", "gouverner", "progressif", "grain", "accorder", "graphique", "saisir", "reconnaissant",
    "gratitude", "grave", "gravité", "avide", "pleurer", "garantie", "garder", "guidance", "coupable", "habitude",
    "arrêter", "manier", "port", "mal", "harmonie", "dur", "récolte", "hâte", "danger", "hésiter", "hiérarchie",
    "surligner", "entraver", "indice", "historique", "creux", "honnête", "horizon", "hostile", "énorme", "humanité",
    "humble", "hypothèse", "idéal", "identique", "identifier", "oisif", "ignorer", "illuminer", "illustrer", "image",
    "imiter", "immense", "immerger", "impact", "affaiblir", "transmettre", "entraver", "impératif", "mettre en œuvre",
    "impliquer", "sous‑entendre", "importer", "imposer", "impressionner", "améliorer", "impulsion", "incitation",
    "incident", "inclure", "revenu", "incorporer", "augmenter", "encourir", "en effet", "indiquer", "indifférent",
    "indigène", "indirect", "induire", "se livrer", "industriel", "inévitable", "déduire", "infini", "gonfler",
    "influencer", "informer", "infrastructure", "inhérent", "initial", "injecter", "blesser", "innocent", "innover",
    "entrée", "demander", "perspicacité", "insister", "inspecter", "inspirer", "installer", "exemple", "instant",
    "au lieu de", "instituer", "instruire", "isoler", "intact", "intégral", "intégrer", "intégrité", "intellect",
    "avoir l'intention", "intense", "interagir", "interférer", "intérimaire", "intérieur", "intermédiaire", "interne",
    "interpréter", "interrompre", "intervalle", "intervenir", "intime", "complexe", "intrigue", "intrinsèque", "s'introduire",
    "intuition", "envahir", "inventer", "investir", "enquêter", "inviter", "impliquer", "ironique", "isoler", "problème",
    "article", "juger", "justifier", "vif", "étiquette", "travail", "retard", "point de repère", "langue", "lancer",
    "couche", "leadership", "conférence", "légal", "héritage", "législation", "légitime", "loisir", "longueur",
    "leçon", "responsable", "libéral", "licence", "de même", "limite", "linéaire", "persistant", "lien", "liste",
    "alphabétisation", "littéral", "littérature", "contentieux", "vivre", "prêt", "local", "localiser", "logique",
    "apparaître", "lâche", "loyal", "lucide", "lucratif", "lumineux", "attrait", "luxe", "maintenir", "majeur",
    "majorité", "mandat", "manifester", "manipuler", "manière", "fabrication", "marge", "massif", "mûr", "maximiser",
    "signifier", "mesurer", "médias", "médiation", "médical", "médium", "mental", "mentionner", "marchand", "fusionner",
    "mérite", "méthode", "métrique", "migrer", "doux", "militaire", "minimiser", "minimum", "mineur", "minute",
    "miracle", "égarer", "mission", "modéré", "modifier", "surveiller", "monopole", "moral", "motion", "motiver",
    "motif", "mutuel", "mystère", "récit", "étroit", "nation", "natif", "naturel", "naviguer", "nécessaire",
    "négatif", "négliger", "négocier", "ni", "neutre", "néanmoins", "notable", "remarquer", "notion", "notoire",
    "nourrir", "roman", "objectif", "obliger", "obscur", "observer", "obstacle", "obtenir", "évident", "occasion",
    "occuper", "se produire", "offenser", "compenser", "omettre", "en cours", "opérer", "opinion", "adversaire",
    "opportunité", "s'opposer", "opposé", "opprimer", "optimal", "optimiser", "option", "orbite", "ordre", "ordinaire",
    "organiser", "orienter", "original", "résultat", "contour", "production", "extérieur", "global", "surmonter",
    "chevaucher", "négliger", "submerger", "devoir", "propre", "rythme", "paquet", "douleur", "panel", "paradigme",
    "parallèle", "paramètre", "participer", "particulier", "passion", "passif", "brevet", "chemin", "patient", "motif",
    "pause", "paix", "percevoir", "pour cent", "parfait", "effectuer", "permanent", "permettre", "persister", "personnel",
    "perspective", "persuader", "pertinent", "omniprésent", "phase", "phénomène", "philosophie", "physique", "pionnier",
    "endroit", "simple", "plan", "plateforme", "plausible", "jeu", "plaidoyer", "agréable", "s'il vous plaît", "engagement",
    "beaucoup", "intrigue", "pluriel", "politique", "polir", "poli", "polluer", "populaire", "portion", "peindre", "poser",
    "position", "positif", "posséder", "possible", "reporter", "potentiel", "verser", "pauvreté", "pouvoir", "pratique",
    "prêcher", "précéder", "précis", "prédire", "préférer", "préjugé", "préliminaire", "prime", "préparer", "prescrire",
    "présence", "présenter", "préserver", "présider", "presse", "pression", "présumer", "prévenir", "précédent", "primaire",
    "principal", "principe", "priorité", "prison", "confidentialité", "privé", "privilège", "probable", "procéder", "processus",
    "proclamer", "produire", "profession", "profit", "profond", "programme", "progrès", "interdire", "projet", "prolonger",
    "éminent", "promesse", "promouvoir", "rapide", "preuve", "approprié", "propriété", "proportion", "proposer", "perspective",
    "prospérer", "protéger", "protestation", "prouver", "fournir", "provoquer", "public", "publier", "acheter", "but", "poursuivre",
    "puzzle", "qualifier", "qualité", "quantité", "quart", "requête", "quête", "question", "file d'attente", "rapide", "calme",
    "quitter", "citation", "course", "radical", "augmenter", "gamme", "rang", "rare", "taux", "plutôt", "atteindre", "réagir",
    "lire", "prêt", "réel", "réaliser", "raison", "rappeler", "récent", "recevoir", "récréation", "reconnaître", "recommander",
    "enregistrer", "récupérer", "rectifier", "recycler", "réduire", "référer", "réfléchir", "réformer", "s'abstenir", "rafraîchir",
    "refuser", "considérer", "région", "enregistrer", "regretter", "réguler", "renforcer", "rejeter", "relier", "libérer", "pertinent",
    "soulager", "compter sur", "rester", "remarquer", "rappeler", "enlever", "rendre", "renouveler", "louer", "réparer", "répéter",
    "remplacer", "répondre", "rapporter", "représenter", "reproduire", "réputation", "demander", "exiger", "sauver", "recherche",
    "ressembler", "réserver", "résident", "résister", "résoudre", "recours", "respecter", "répondre", "restaurer", "restreindre",
    "résultat", "reprendre", "retenir", "prendre sa retraite", "retourner", "révéler", "revenu", "inverser", "réviser", "réviser",
    "revivre", "récompense", "rythme", "riche", "débarrasser", "risque", "rival", "robuste", "rôle", "routine", "règle", "rural",
    "sacrifice", "sûr", "but", "échantillon", "échelle", "balayer", "disperser", "calendrier", "schéma", "portée", "score", "écran",
    "recherche", "saison", "section", "secteur", "sécuriser", "chercher", "sélectionner", "sens", "sensible", "séquence", "série",
    "servir", "service", "régler", "sévère", "forme", "partager", "changement", "court", "montrer", "signal", "signification", "similaire",
    "simple", "simuler", "simultané", "seul", "site", "situer", "taille", "compétence", "léger", "intelligent", "lisse", "monter en flèche",
    "social", "doux", "sol", "unique", "solide", "solution", "résoudre", "son", "source", "espace", "durée", "épargner", "parler", "spécial",
    "spécifique", "spécifier", "spéculer", "vitesse", "dépenser", "diviser", "gâter", "repérer", "diffuser", "stable", "personnel", "étape",
    "se tenir", "standard", "point de vue", "étoile", "état", "statique", "statistiques", "statut", "stable", "raide", "pas", "coller",
    "encore", "stimuler", "stock", "arrêter", "magasin", "droit", "tension", "étirer", "strict", "frapper", "fort", "structure", "lutter",
    "étude", "style", "sujet", "soumettre", "ultérieur", "substance", "substantiel", "substitut", "subtil", "réussir", "succès", "suffisant",
    "suggérer", "adapté", "somme", "résumé", "supérieur", "fournir", "soutenir", "supposer", "sûr", "surface", "surplus", "surprise",
    "entourer", "enquêter", "survivre", "soupçonner", "suspendre", "soutenir", "symbole", "symptôme", "système", "table", "tact", "prendre",
    "talent", "parler", "cible", "tâche", "enseigner", "équipe", "technique", "technologie", "temporaire", "avoir tendance", "terme", "test",
    "texte", "thème", "théorie", "donc", "épais", "mince", "penser", "approfondi", "bien que", "menace", "à travers", "lancer", "serré",
    "temps", "minuscule", "tissu", "titre", "ensemble", "tolérer", "sujet", "total", "toucher", "difficile", "tournée", "vers", "piste",
    "commerce", "tradition", "trafic", "tragique", "former", "transférer", "transformer", "transit", "traduire", "transporter", "piège",
    "voyage", "traiter", "traité", "arbre", "tendance", "procès", "tribu", "voyage", "problème", "vrai", "confiance", "vérité", "essayer",
    "tourner", "type", "typique", "ultime", "incapable", "inconscient", "découvrir", "sous", "subir", "comprendre", "entreprendre", "annuler",
    "mal à l'aise", "inattendu", "injuste", "se dérouler", "unifier", "unique", "unité", "unir", "universel", "inconnu", "contrairement",
    "improbable", "décharger", "déverrouiller", "malchanceux", "non rémunéré", "désagréable", "impopulaire", "irréel", "agitation", "dangereux",
    "incertain", "inhabituel", "réticent", "mettre à jour", "améliorer", "soutenir", "sur", "supérieur", "bouleversé", "urbain", "exhorter",
    "utiliser", "habituel", "vacant", "vacances", "vaccin", "valide", "précieux", "valeur", "variable", "variation", "variété", "divers",
    "varier", "vaste", "véhicule", "entreprise", "vérifier", "version", "contre", "vaisseau", "viable", "victime", "victoire", "vidéo",
    "vue", "village", "violer", "violence", "virtuel", "vertu", "virus", "visible", "vision", "visiter", "visuel", "vital", "vif", "voix",
    "volume", "bénévole", "vote", "salaire", "attendre", "marcher", "mur", "vouloir", "guerre", "avertir", "gaspiller", "regarder", "eau",
    "vague", "façon", "faible", "richesse", "arme", "porter", "hebdomadaire", "peser", "poids", "bienvenue", "bien-être", "bien", "ouest",
    "humide", "entier", "large", "largeur", "sauvage", "volontaire", "gagner", "vent", "fenêtre", "sage", "souhait", "retirer", "dans",
    "sans", "témoin", "émerveillement", "mot", "travail", "monde", "inquiétude", "valeur", "voudrais", "écrire", "faux", "cour", "année",
    "jeunesse", "zéro", "zone"
]
vocabulaire_fr = vocabulaire_fr * 3

expressions_fr = [
    "C'est la goutte d'eau qui fait déborder le vase", "Mettre la charrue avant les bœufs", "Appeler un chat un chat",
    "Avoir le cœur sur la main", "Être sur son trente et un", "Ça me prend la tête", "Avoir la frite", "C'est simple comme bonjour",
    "Être dans les nuages", "Avoir un poil dans la main", "Faire d'une pierre deux coups", "Voir la vie en rose",
    "Mettre son grain de sel", "C'est du gâteau", "Avoir la pêche", "Poser un lapin", "Tomber dans les pommes",
    "Avoir la chair de poule", "Sauter du coq à l'âne", "Tourner autour du pot", "Être au bout du rouleau",
    "Casser les pieds", "Faire la grasse matinée", "Avoir le cafard", "Être à l'ouest", "Mettre les voiles",
    "Avoir le beurre et l'argent du beurre", "Être dans la panade", "Ne pas y aller par quatre chemins",
    "Avoir un chat dans la gorge", "Manger sur le pouce", "Être tiré à quatre épingles", "Avoir une mémoire d'éléphant",
    "C'est l'hôpital qui se fout de la charité", "Avoir la main verte", "Être comme un coq en pâte", "Faire le pont",
    "Avoir un coup de foudre", "C'est la fin des haricots", "Avoir le vent en poupe", "Être à côté de la plaque",
    "Couper la poire en deux", "Avoir le cul entre deux chaises", "Mettre la main à la pâte", "Être au pied du mur",
    "Avoir les dents longues", "C'est une autre paire de manches", "Avoir un ticket avec quelqu'un", "Casser du sucre sur le dos",
    "Être à la bourre", "Mettre du beurre dans les épinards", "Avoir une case en moins", "C'est bête comme chou",
    "Avoir le compas dans l'œil", "Être né coiffé", "Faire une croix dessus", "Avoir la conscience tranquille",
    "C'est un vrai fromage", "Avoir un poil dans la main", "Être sur la même longueur d'onde", "Faire un froid de canard",
    "Avoir un bon fond", "C'est le jour et la nuit", "Avoir la tête dans le guidon", "Être comme un poisson dans l'eau",
    "Faire la part des choses", "Avoir les yeux plus gros que le ventre", "C'est de la dynamite", "Avoir un cœur d'artichaut",
    "Être dans la lune", "Faire le mur", "Avoir le sens du commerce", "C'est le grand bazar", "Avoir la grosse tête",
    "Être sur un nuage", "Faire chou blanc", "Avoir une oreille attentive", "C'est le monde à l'envers", "Avoir la bougeotte",
    "Être au septième ciel", "Faire des ronds dans l'eau", "Avoir le bras long", "C'est un coup d'épée dans l'eau",
    "Avoir le mot pour rire", "Être comme un lion en cage", "Faire du lèche-vitrine", "Avoir un blanc",
    "C'est une tempête dans un verre d'eau", "Avoir la langue bien pendue", "Être en pleine forme", "Faire la sourde oreille",
    "Avoir les doigts de fée", "C'est une mine d'or", "Avoir le trac", "Être au bout du tunnel", "Faire une bouchée",
    "Avoir un œil critique", "C'est un sacré numéro", "Avoir la foi", "Être sur le qui-vive", "Faire le grand huit"
]
expressions_fr = expressions_fr * 2

grammaire_fr = [
    "Utilisez le présent simple pour les faits et les routines.",
    "Utilisez le passé composé pour les actions terminées dans le passé.",
    "Utilisez l'imparfait pour décrire des actions passées habituelles ou en cours.",
    "Utilisez le futur simple pour les actions futures.",
    "Le conditionnel présent exprime une action soumise à une condition.",
    "Le subjonctif est utilisé après certaines conjonctions et verbes exprimant le doute, le souhait ou l'émotion.",
    "Les pronoms compléments directs (le, la, les) remplacent un nom complément d'objet direct.",
    "Les pronoms compléments indirects (lui, leur) remplacent un nom complément d'objet indirect.",
    "Les pronoms y et en remplacent respectivement un lieu ou une chose introduite par 'à' et une quantité ou une chose introduite par 'de'.",
    "La négation se forme avec 'ne...pas' (ou 'ne...jamais', 'ne...rien', etc.) autour du verbe.",
    "Les adjectifs s'accordent en genre et en nombre avec le nom qu'ils qualifient.",
    "Les verbes pronominaux (se laver, se souvenir) s'utilisent avec un pronom réfléchi.",
    "Le passé récent se forme avec 'venir de + infinitif'.",
    "Le futur proche se forme avec 'aller + infinitif'.",
    "L'impératif sert à donner un ordre ou un conseil.",
    "Les prépositions de lieu (à, dans, sur, sous, devant, derrière, entre, etc.) indiquent la position.",
    "Les conjonctions de coordination (mais, ou, et, donc, or, ni, car) relient des propositions indépendantes.",
    "Les conjonctions de subordination (que, quand, si, comme, parce que, etc.) introduisent une proposition dépendante.",
    "Le gérondif (en + participe présent) exprime la simultanéité ou la manière.",
    "Le participe présent (ant, end, issant) peut servir d'adjectif verbal ou de gérondif.",
    "L'accord du participe passé avec l'auxiliaire 'avoir' se fait si le complément d'objet direct est placé avant.",
    "L'accord du participe passé avec l'auxiliaire 'être' se fait avec le sujet.",
    "Les verbes du premier groupe (-er) ont une conjugaison régulière.",
    "Les verbes du deuxième groupe (-ir) ont un participe présent en -issant.",
    "Les verbes du troisième groupe (-ir, -oir, -re) sont irréguliers et doivent être mémorisés."
]

sujets_redaction = [
    "Êtes-vous d'accord ou non avec l'affirmation suivante ? La technologie a rendu nos vies plus compliquées. Utilisez des raisons et des exemples spécifiques.",
    "Certaines personnes préfèrent vivre dans une petite ville. D'autres préfèrent une grande ville. Que préférez-vous et pourquoi ?",
    "Pensez-vous que les universités devraient obliger les étudiants à suivre des cours variés en dehors de leur spécialité ? Pourquoi ou pourquoi pas ?",
    "Selon vous, quelle est la qualité la plus importante pour un bon leader ? Utilisez des exemples précis.",
    "Certains pensent que la meilleure façon d'apprendre est par l'expérience. D'autres disent que l'apprentissage par les livres est plus efficace. Êtes-vous d'accord avec l'une ou l'autre ?",
    "Êtes-vous d'accord ou non que la chose la plus importante que les parents puissent enseigner à leurs enfants est l'indépendance ?",
    "Certains pensent que le gouvernement devrait dépenser plus pour protéger l'environnement. D'autres disent pour la santé publique. Lequel est le plus important ?",
    "Êtes-vous d'accord qu'il est préférable de travailler en équipe que seul ? Expliquez.",
    "Préférez-vous planifier soigneusement votre temps libre ou être spontané ? Expliquez.",
    "Pensez-vous que les médias sociaux ont un effet positif ou négatif sur la société ? Donnez des exemples.",
    "Certains croient que le succès vient du travail acharné, d'autres de la chance. Avec qui êtes-vous d'accord ?",
    "L'objectif le plus important de l'éducation est de préparer les gens à une carrière. Êtes-vous d'accord ?",
    "La publicité influence‑t‑elle trop nos habitudes d'achat ? Expliquez.",
    "Le voyage est‑il nécessaire pour une bonne éducation ? Pourquoi ou pourquoi pas ?",
    "Préférez‑vous lire des romans ou des essais ? Pourquoi ?",
    "La meilleure façon de réduire le stress est de passer du temps seul. Êtes-vous d'accord ?",
    "L'argent est‑il la meilleure mesure du succès ? Expliquez.",
    "Les écoles devraient‑elles enseigner la littératie financière ? Pourquoi ?",
    "Certains disent qu'il vaut mieux être généraliste, d'autres spécialiste. Avec qui êtes‑vous d'accord ?",
    "La chose la plus importante dans la vie est le bonheur. Utilisez des exemples pour soutenir votre réponse."
]

conseils_redaction = """
Conseils pour la rédaction en français

1. Comprenez le sujet – Répondez exactement à la question posée.
2. Planifiez avant d'écrire – Prenez 2–3 minutes pour structurer vos idées.
3. Une thèse claire – La première phrase de l'introduction doit énoncer votre position.
4. Phrases de sujet – Chaque paragraphe doit commencer par une phrase qui introduit l'idée principale.
5. Exemples concrets – Évitez les généralités ; utilisez des exemples réels ou hypothétiques.
6. Mots de liaison – Cependant, par conséquent, de plus, par exemple.
7. Variez la longueur des phrases – Mélangez phrases courtes et longues.
8. Relisez-vous – Laissez 2–3 minutes pour corriger la grammaire et l'orthographe.
9. Restez dans le sujet – N'ajoutez pas d'informations hors de propos.
10. Écrivez au moins 250 mots – Les essais plus longs ont tendance à mieux réussir s'ils sont bien organisés.
"""

def get_items(base_list, lesson_num, count):
    start = (lesson_num - 1) * count
    end = start + count
    if end <= len(base_list):
        return base_list[start:end]
    else:
        first_part = base_list[start:]
        remaining = count - len(first_part)
        second_part = base_list[:remaining]
        return first_part + second_part

def get_sujet_redaction(lesson_num):
    return sujets_redaction[(lesson_num - 1) % len(sujets_redaction)]

# ========== AUDIO ==========
def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Audio désactivé. Installez edge-tts.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                generate_audio(text, tmp.name, VOICE)
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur audio : {e}")
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ========== AFFICHAGE DE LA LEÇON ==========
st.markdown(f"## 📖 Leçon {lesson_number}")

conversations = generer_conversation(lesson_number)
vocab = get_items(vocabulaire_fr, lesson_number, 50)
expressions = get_items(expressions_fr, lesson_number, 25)
grammaire = get_items(grammaire_fr, lesson_number, 25)
sujet = get_sujet_redaction(lesson_number)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Conversations", "📚 Vocabulaire", "💡 Expressions", "📖 Grammaire", "✍️ Rédaction"])

with tab1:
    st.subheader("Conversations interactives – Ita & Kettely")
    for idx, conv in enumerate(conversations):
        st.markdown(conv)
        play_audio(conv, f"conv_{lesson_number}_{idx}")
        st.markdown("---")

with tab2:
    st.subheader("Vocabulaire (50 mots)")
    cols = st.columns(5)
    for idx, mot in enumerate(vocab):
        with cols[idx % 5]:
            st.markdown(f"**{mot}**")
            play_audio(mot, f"vocab_{lesson_number}_{idx}")

with tab3:
    st.subheader("Expressions idiomatiques (25)")
    cols = st.columns(5)
    for idx, expr in enumerate(expressions):
        with cols[idx % 5]:
            st.markdown(f"**{expr}**")
            play_audio(expr, f"expr_{lesson_number}_{idx}")

with tab4:
    st.subheader("Règles de grammaire (25)")
    for idx, regle in enumerate(grammaire):
        st.markdown(f"**{idx+1}. {regle}**")
        play_audio(regle, f"grammaire_{lesson_number}_{idx}")
        st.markdown("---")

with tab5:
    st.subheader("Rédaction")
    st.markdown("### Sujet de rédaction")
    st.markdown(sujet)
    play_audio(sujet, f"sujet_{lesson_number}")
    st.markdown("---")
    st.markdown("### Conseils pour la rédaction")
    st.markdown(conseils_redaction)
    play_audio(conseils_redaction, f"conseils_{lesson_number}")
    st.markdown("---")
    st.markdown("### Votre essai")
    st.text_area("Écrivez votre essai ici :", height=300, key=f"essai_{lesson_number}")
    st.info("Après avoir écrit, relisez votre essai pour la grammaire, la cohérence et les exemples. Entraînez‑vous avec un chronomètre.")

if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 Félicitations ! Vous avez terminé le cours de français.")
    st.markdown("""
    ### 📞 Pour continuer avec des projets avancés ou obtenir du soutien :
    - **Gesner Deslandes** – Fondateur
    - 📱 WhatsApp : (509) 4738-5663
    - 📧 Email : deslandes78@gmail.com
    - 🌐 [Site principal](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Continuez à pratiquer et à parler français !
    """)
