import os
from imap_tools import MailBox, AND
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Charger variables d'environnement
load_dotenv()

# Config IMAP (lecture mail)
EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))

# Config SMTP (envoi notification)
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Mots-clés
MOTS_POSITIFS = ["entretien", "félicitations", "sélectionné", "convocation"]
MOTS_NEGATIFS = ["rejet", "refus", "malheureusement", "non retenu", "issue défavorable"]
MOTS_A_EXCLURE = ["alert", "alerte", "notification", "tmechri", "newsletter", "invitation", "donotreply", "ebuyclub"]
OBJETS_A_EXCLURE = ["nouvelle offre", "nouvelles offres", "découvrez", "recommandée", "suggestion", "vous pourriez aimer"]

# Fichier Excel
EXCEL_FILE = "suivi_mails_candidatures.xlsx"

# Fonction pour envoyer une notification de nouveaux mails

def send_notification_email(nb_nouveaux):
    if nb_nouveaux == 0:
        return
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = f"{nb_nouveaux} nouveaux mails de candidature détectés"

    body = f"Ton robot a détecté {nb_nouveaux} nouveaux mails pertinents.\nConsulte le fichier Excel pour les détails."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print("📧 Notification envoyée.")
    except Exception as e:
        print(f"❌ Erreur d'envoi notification : {e}")

# Fonction pour envoyer une relance automatique

def send_follow_up_email(to_email, sujet_original):
    sujet = f"Relance – {sujet_original}"
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email
    msg['Subject'] = sujet

    corps = f"""
Bonjour,

Je me permets de revenir vers vous concernant ma candidature envoyée il y a deux semaines.

Je reste très motivée par l’opportunité et disponible pour toute information complémentaire.

Cordialement,

MECHRI Maroua
"""
    msg.attach(MIMEText(corps, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📧 Relance envoyée à {to_email}")
    except Exception as e:
        print(f"❌ Erreur lors de la relance : {e}")

# Charger historique
if os.path.exists(EXCEL_FILE):
    df_historique = pd.read_excel(EXCEL_FILE)
    anciens_sujets = set(df_historique["Objet"].fillna("").tolist())
else:
    df_historique = pd.DataFrame()
    anciens_sujets = set()

results = []

# Connexion à la boîte mail
with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD, initial_folder='INBOX') as mailbox:
    print("✅ Connexion réussie.")

    date_limite = datetime.now().date() - timedelta(days=15)
    messages = mailbox.fetch(criteria=AND(date_gte=date_limite), bulk=True)

    for msg in messages:
        texte_mail = msg.text or ""
        sujet = msg.subject or ""
        exp = msg.from_ or ""

        texte_mail_lower = texte_mail.lower()
        sujet_lower = sujet.lower()

        exclu = (
            any(mot in texte_mail_lower for mot in MOTS_A_EXCLURE)
            or any(mot in sujet_lower for mot in OBJETS_A_EXCLURE)
        )

        if "candidature" in sujet_lower and EMAIL in exp:
            statut = "Envoyée"
            mail_type = "Envoyée"
        elif not exclu and (
            any(kw in exp.lower() for kw in ["recrut", "hr", "jobs", "rh", "talent", "career", "candidature"])
            or any(mot in texte_mail_lower for mot in MOTS_POSITIFS + MOTS_NEGATIFS)
        ) and sujet not in anciens_sujets:
            if any(mot in texte_mail_lower for mot in MOTS_POSITIFS):
                statut = "Positif"
            elif any(mot in texte_mail_lower for mot in MOTS_NEGATIFS):
                statut = "Refusé"
            else:
                statut = "À traiter"
            mail_type = "Réponse"
        else:
            continue

        results.append({
            "Date": msg.date.strftime('%Y-%m-%d'),
            "Expéditeur": exp,
            "Objet": sujet,
            "Statut détecté": statut,
            "Aperçu": texte_mail[:150].replace('\n', ' '),
            "Type": mail_type,
            "Date de relance": None
        })

# Mettre à jour Excel

df_new = pd.DataFrame(results)
if not df_new.empty:
    df_final = pd.concat([df_historique, df_new], ignore_index=True).drop_duplicates(subset=["Objet"])
else:
    df_final = df_historique.copy()

# Traitement des relances et refus auto

today = datetime.now().date()
df_updated = df_final.copy()

for idx, row in df_updated.iterrows():
    if row.get("Type") == "Envoyée" and row["Statut détecté"] == "Envoyée":
        date_envoi = pd.to_datetime(row["Date"]).date()
        relance_envoyee = pd.notna(row.get("Date de relance", None))
        jours_depuis_envoi = (today - date_envoi).days

        sujet_envoye = row["Objet"].lower()
        reponse_existante = df_final[
            (df_final["Type"] == "Réponse") &
            (df_final["Objet"].str.lower().str.contains(sujet_envoye[:20]))
        ]

        if jours_depuis_envoi >= 14 and not relance_envoyee and reponse_existante.empty:
            send_follow_up_email(row["Expéditeur"], row["Objet"])
            df_updated.at[idx, "Date de relance"] = today.strftime('%Y-%m-%d')

        if jours_depuis_envoi >= 35 and reponse_existante.empty:
            df_updated.at[idx, "Statut détecté"] = "Refusée ⚠️ (auto)"

# Enregistrer Excel final

df_updated.to_excel(EXCEL_FILE, index=False)
print(f"📁 Mise à jour Excel terminée. {len(df_new)} nouveaux mails traités.")
send_notification_email(len(df_new))
