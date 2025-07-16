# 📬 Candidabot – Email Tracker 🤖
Bienvenue dans la nouvelle version de Candidabot, mon robot personnel qui m’aide à suivre automatiquement mes candidatures en lisant les réponses que je reçois par email.

J’ai souvent du mal à savoir où j’en suis dans mes candidatures : qui m’a répondu ? Est-ce positif, négatif ? Faut-il relancer ?
C’est pour ça que j’ai créé ce robot qui lit ma boîte mail, analyse les réponses et met à jour un fichier Excel clair et pratique.

## ⚙️ Fonctionnalités
- 📥 Lecture automatique des mails via IMAP

- 🧠 Détection intelligente du contenu des mails :

  Réponse positive (ex: "entretien", "sélectionné")

  Réponse négative (ex: "refus", "non retenu")

  Candidature envoyée

- ❌ Filtrage des mails non pertinents (alertes, newsletters…)

- 📊 Mise à jour d’un fichier Excel (suivi_mails_candidatures.xlsx)

- 🔔 Notification par mail des nouveaux messages pertinents

- 🔁 Relance automatique après 14 jours sans réponse (envoi de mail)

- 🕒 Marquage automatique en "Refusée ⚠️ (auto)" après 35 jours sans retour


## 📁 Structure du fichier Excel
Date	Expéditeur	Objet	Statut détecté	Aperçu	Type	Date de relance
2025-07-10	recruteur@…	Candidature Dev	Positif	Merci pour…	Réponse	-

## 🛠️ Technologies utilisées
Ce projet repose sur les technologies et bibliothèques suivantes :

### Python 3.x – Langage principal utilisé pour développer le script.

### imap-tools – Permet de se connecter à une boîte mail IMAP et de lire les messages.

### pandas – Utilisé pour manipuler les données et gérer le fichier Excel.

### openpyxl – Sert à lire et écrire des fichiers Excel (.xlsx).

### python-dotenv – Pour charger les variables d’environnement depuis un fichier .env.

### python-dateutil – Fournit des extensions puissantes pour manipuler des objets datetime.

## 📧 Relance automatique
Si aucun retour n’est détecté après 14 jours et qu'aucune réponse n’est trouvée en lien avec le même objet, un mail de relance est automatiquement envoyé à l’expéditeur.

text
Copier
Modifier
Objet : Relance – [Objet original]

Bonjour,

Je me permets de revenir vers vous concernant ma candidature envoyée il y a deux semaines.

Je reste très motivée par l’opportunité et disponible pour toute information complémentaire.

Cordialement,

## 🔐 Configuration
Crée un fichier .env avec les variables suivantes :

env
Copier
Modifier
EMAIL_ADDRESS=ton_email@example.com
EMAIL_PASSWORD=ton_mot_de_passe
IMAP_SERVER=imap.exemple.com
IMAP_PORT=993
SMTP_SERVER=smtp.exemple.com
SMTP_PORT=587
SMTP_EMAIL=ton_email@example.com
SMTP_PASSWORD=ton_mot_de_passe

▶️ Lancer le script
bash
Copier
Modifier
python suivi_mails.py

## 📌 Pourquoi ce projet ?
Je suis en pleine recherche d’emploi et je voulais un outil utile, fait pour moi, par moi.
Plutôt que d’entrer chaque candidature manuellement, je voulais un assistant automatique, intelligent et simple à utiliser.

Ce projet me permet aussi de pratiquer Python tout en créant une vraie solution à un vrai besoin.

## 🧑‍💻 Auteure
Mechri Maroua
Développeuse Full Stack passionnée par les projets utiles et les défis techniques 🚀

