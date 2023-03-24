# mtl15m

Une carte intéractive évaluant le potentiel piétonnier des différents quartiers de Montréal

## Instructions pour le développement

### Dépendances

   - Node.js 16.x+
   - Python 3.10+

### Premier départ

Après avoir clôné ce dépôt, installez les dépendances avec

    npm install

Puis, générez les données en exécutant `tools/run_all.bat` (Windows) ou `tools/run_all.sh` (Unix).

À partir de là, vous pouvez exécuter `npm run dev` pour lancer un serveur local de développement, ou `npm run test` pour exécuter les tests automatisés.

Ce projet utilise eslint pour de la validation additionnelle. Si vous utilisez VS Code avec l'extension ESLint officielle, ceci sera fait automatiquement pour vous. Sinon, vous pouvez exécuter `npm run lint` pour valider, ou `npm run lint-fix` pour corriger automatiquement les erreurs qui peuvent l'être. 