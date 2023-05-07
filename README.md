# mtl15m

Une carte intéractive évaluant le potentiel piétonnier des différents quartiers de Montréal

## Instructions pour le développement

### Dépendances

   - Node.js 16.x+ (pour l'application elle même)
   - Python 3.10+ et PowerShell 7+ (pour les outils)

Si vous utilisez VS Code comme environnement de développement, installez les extensions recommandées.

### Premier départ

Après avoir clôné ce dépôt, installez les dépendances avec

    npm install

À partir de là, vous pouvez exécuter `npm run dev` pour lancer un serveur local de développement, ou `npm run test` pour exécuter les tests automatisés.

Ce projet utilise eslint pour de la validation additionnelle. Si vous utilisez VS Code avec l'extension ESLint officielle, ceci sera fait automatiquement pour vous. Sinon, vous pouvez exécuter `npm run lint` pour valider, ou `npm run lint-fix` pour corriger automatiquement les erreurs qui peuvent l'être.

### Données

Les données sont précalculées à partir de sources au moyen de scripts stockés dans le répertoire `tools`, et le résultat est versionné. Ces scripts dépendent de bibliothèques tierces que vous pouvez installer avec

    pip install -r tools/requirements.txt

Les données sources peuvent être grosses, donc elles ne sont pas versionnées directement dans ce dépôt. À la place, vous pouvez les récupérer avec 

    pwsh data/source/download_data.ps1

Ce script les télécharge déjà dans un répertoire où les scripts de `tools` s'attendent à les trouver.