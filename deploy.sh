#!/bin/bash
echo "Déploiement vers Google App Engine..."
gcloud app deploy --quiet  # Le flag --quiet évite d'avoir à taper Y
echo "Déploiement terminé !"
