# Les Toqués du Biz - Documentation

## Informations du Projet
- **Nom du projet Google Cloud** : les-toques-du-biz
- **URL du site** : https://zenalacarte.com
- **Région App Engine** : europe-west1

## Configuration du Projet

### Domaine et DNS
- **Domaine principal** : zenalacarte.com
- **Sous-domaine** : www.zenalacarte.com
- **Gestion DNS** : Automatique via Google Cloud
- **SSL** : Géré par Google, renouvellement automatique

### Intégrations
- **Formulaire Newsletter** : ConvertKit
  - ID du formulaire : 7556250
  - Data UID : 306a5b25be
  - URL d'action : https://app.kit.com/forms/7556250/subscriptions

## Déploiement

### Prérequis
```bash
# Installation des dépendances
pip install -r requirements.txt
```

### Commandes Importantes
1. **Test en local**
   ```bash
   python3 -m flask run --port 9000
   ```

2. **Déploiement rapide**
   ```bash
   ./deploy.sh
   ```
   ou
   ```bash
   gcloud app deploy
   ```

### Structure des Fichiers
- `app.py` : Application Flask principale
- `templates/index.html` : Page d'accueil
- `static/` : Fichiers statiques (CSS, JS, images)
- `deploy.sh` : Script de déploiement rapide
- `app.yaml` : Configuration App Engine
- `requirements.txt` : Dépendances Python

## Maintenance

### Mise à jour du Site
1. Modifier les fichiers nécessaires
2. Tester en local (port 9000)
3. Déployer avec `./deploy.sh`

### Commandes Google Cloud Utiles
```bash
# Voir les logs
gcloud app logs tail

# Ouvrir la console
gcloud app browse

# Vérifier le projet actif
gcloud config get-value project
```

## Sécurité
- SSL/HTTPS activé et géré automatiquement
- Certificats auto-renouvelés par Google
- Sécurité gérée par App Engine

## Contact et Support
- Propriétaire : mehdi@zenalacarte.com
- Projet Google Cloud : [Console](https://console.cloud.google.com/appengine?project=les-toques-du-biz)

## Dépendances Principales
- Flask 3.0.0
- Python-dotenv 1.0.0
- Flask-WTF 1.2.1
- Pillow 10.1.0
