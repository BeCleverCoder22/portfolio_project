# 🎨 Portfolio Personnel - Django

Un portfolio personnel moderne et professionnel développé avec Django, conçu pour présenter efficacement vos projets, compétences et expériences professionnelles.

## 📸 Aperçu

Ce portfolio offre une interface élégante et responsive pour :
- Présenter vos projets avec des descriptions détaillées
- Afficher vos compétences techniques avec des niveaux de maîtrise
- Partager votre parcours professionnel
- Recevoir et gérer les messages de contact
- Suivre les statistiques de visite
- Administrer le contenu via une interface d'administration personnalisée

## ✨ Fonctionnalités

### 🏠 Page d'accueil
- Présentation personnelle avec photo de profil
- Projets mis en avant
- Visualisation des compétences par catégorie
- Call-to-action pour téléchargement du CV

### 📁 Gestion des projets
- Affichage détaillé des projets avec images
- Filtrage par technologie, statut et recherche textuelle
- Gestion des vues et statistiques
- Liens vers GitHub et démos en ligne
- Support des descriptions riches avec éditeur WYSIWYG

### 💼 Expériences professionnelles
- Timeline des expériences
- Descriptions détaillées des postes
- Gestion des postes actuels/passés

### 📞 Système de contact
- Formulaire de contact avec validation
- Système de priorités des messages
- Notifications email automatiques
- Interface d'administration pour la gestion des messages
- Suivi des réponses

### 📊 Dashboard administrateur
- Statistiques de visite en temps réel
- Graphiques de performance
- Gestion des messages reçus
- Suivi des projets les plus consultés

### 🔒 Sécurité et performance
- Middleware de suivi des visiteurs
- Protection CSRF
- Mise en cache des pages
- Compression des assets statiques
- Variables d'environnement pour la configuration

## 🛠️ Technologies utilisées

### Backend
- **Django 5.x** - Framework web Python
- **MySQL** - Base de données
- **Pillow** - Traitement d'images
- **python-dotenv** - Gestion des variables d'environnement

### Frontend
- **Bootstrap 5** - Framework CSS responsive
- **Font Awesome** - Icônes
- **Google Fonts (Poppins)** - Typographie
- **JavaScript vanilla** - Interactions côté client

### Outils et extensions
- **django-crispy-forms** - Rendu des formulaires
- **crispy-bootstrap5** - Intégration Bootstrap
- **django-ckeditor** - Éditeur WYSIWYG
- **WhiteNoise** - Serveur de fichiers statiques
- **Gunicorn** - Serveur WSGI pour production

## 📋 Prérequis

- Python 3.8+
- MySQL 5.7+ ou MariaDB 10.2+
- pip (gestionnaire de paquets Python)
- Virtualenv (recommandé)

## 🚀 Installation

### 1. Cloner le repository
```bash
git clone https://github.com/BeCleverCoder22/portfolio_project.git
cd portfolio_project
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de la base de données
Créez une base de données MySQL :
```sql
CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Variables d'environnement
Créez un fichier `.env` à la racine du projet :
```env
SECRET_KEY=votre-clé-secrète-django-très-longue-et-aléatoire
DEBUG=True
DB_NAME=portfolio_db
DB_USER=votre_user_mysql
DB_PASSWORD=votre_mot_de_passe_mysql
DB_HOST=localhost
DB_PORT=3306
ADMIN_EMAIL=votre.email@example.com
DEFAULT_FROM_EMAIL=noreply@votredomaine.com
```

### 6. Migrations et données initiales
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### 7. Lancer le serveur de développement
```bash
python manage.py runserver
```

Le site sera accessible sur : `http://127.0.0.1:8000`

## 📁 Structure du projet

```
portfolio_project/
├── manage.py                    # Script de gestion Django
├── requirements.txt             # Dépendances Python
├── .env                        # Variables d'environnement (à créer)
├── portfolio_project/          # Configuration principale
│   ├── settings.py             # Paramètres Django
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                 # Configuration WSGI
├── portfolio/                  # Application portfolio
│   ├── models.py               # Modèles de données
│   ├── views.py                # Vues et logique métier
│   ├── urls.py                 # URLs de l'application
│   ├── forms.py                # Formulaires
│   ├── admin.py                # Configuration admin
│   ├── middleware.py           # Middleware personnalisé
│   └── migrations/             # Migrations de base de données
├── templates/                  # Templates HTML
│   ├── base.html               # Template de base
│   └── portfolio/              # Templates spécifiques
├── static/                     # Fichiers statiques sources
├── staticfiles/                # Fichiers statiques collectés
└── media/                      # Fichiers uploadés
    ├── projects/               # Images des projets
    ├── profile/                # Photos de profil
    └── resumes/                # CVs téléchargeables
```

## 🎨 Personnalisation

### Modifier l'apparence
Les styles CSS sont définis dans `templates/base.html`. Vous pouvez :
- Modifier les couleurs dans les variables CSS (`:root`)
- Ajuster la typographie
- Personnaliser les animations et transitions

### Ajouter du contenu
1. Connectez-vous à l'admin : `/admin/`
2. Configurez vos informations dans "Paramètres du site"
3. Ajoutez vos compétences, projets et expériences
4. Téléchargez votre photo de profil et CV

### Configuration email
Pour les notifications de contact, configurez dans `settings.py` :
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.votredomaine.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre.email@example.com'
EMAIL_HOST_PASSWORD = 'votre_mot_de_passe'
```

## 🚀 Déploiement

### Variables d'environnement de production
```env
DEBUG=False
ALLOWED_HOSTS=votredomaine.com,www.votredomaine.com
SECRET_KEY=votre-clé-très-sécurisée-pour-production
```

### Serveur de production
```bash
# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Lancer avec Gunicorn
gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:8000
```

### Nginx (optionnel)
Configuration nginx recommandée pour servir les fichiers statiques et média.

## 📊 Fonctionnalités avancées

### Dashboard administrateur
- Graphiques de visites par jour/mois
- Statistiques des projets les plus vus
- Gestion des messages par priorité
- Export des données de contact

### SEO et performance
- URLs conviviales avec slugs
- Meta tags optimisés
- Compression des images
- Mise en cache des pages fréquemment visitées

### Sécurité
- Protection CSRF activée
- Validation des formulaires
- Sanitisation des entrées utilisateur
- Logs des tentatives de connexion

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajouter nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Créez une issue sur GitHub
- Contactez-moi via le formulaire de contact du portfolio

## 🎯 Roadmap

### Version 2.0 (à venir)
- [ ] Mode sombre/clair
- [ ] Système de blog intégré
- [ ] API REST pour les données
- [ ] PWA (Progressive Web App)
- [ ] Multilingue (FR/EN)
- [ ] Optimisation SEO avancée
- [ ] Intégration réseaux sociaux
- [ ] Système de commentaires

---

**Développé avec ❤️ par BeCleverCoder22**

*Un portfolio moderne pour développeurs ambitieux*