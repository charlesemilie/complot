# Complot en ligne

Jeu de stratégie en ligne inspiré de **Coup**, implémenté avec **FastAPI** (backend) et **React** (frontend).

## Structure
Voir l'arborescence complète dans ce document.

## Setup local

1. Cloner le repo
2. Lancer `docker-compose up --build`
3. Ouvrir http://localhost:3000

## Déploiement sur Render

Le déploiement monorepo est configuré dans `render.yaml`. Il suffit de connecter le dépôt à Render et de définir les variables d'environnement :

- DATABASE_URL
- SECRET_KEY
- REACT_APP_API_URL

Render se chargera de builder et déployer les deux services automatiquement.