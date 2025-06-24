## Objectifs et périmètres

```
Langages ciblés : 
    - Python
    - Php
    - Html
    - ...
    
Tâches précises :
    - génération de code
    - correction d'erreurs
    - optimisation d'erreurs
    - optimisation de performance,
    - revue de style
    - ...    
```

## Collecte et préparation des données

```
    - Sources variées : dépôts open source (GitHub, GitLab), plateformes d’exercices (LeetCode, Codewars), bases de données de bugs (BugsInPy, Defects4J).
    - Annotations : exemples de code corrigé, optimisé, ou annoté par des experts.
    - Nettoyage : suppression des doublons, anonymisation, filtrage des exemples de mauvaise qualité.
```

## Prétraitement des données

```
    - Tokenisation adaptée au code : prise en compte de la syntaxe, indentation, commentaires.
    - Structuration : séparer le code, les descriptions, les commentaires, les tests unitaires.
    - Augmentation de données : génération de variantes, introduction contrôlée d’erreurs pour la correction.
```

## Choix du modèle

```
    - Modèles spécialisés : GPT-3/4, CodeBERT, Codex, StarCoder, Llama-2 Code, etc.
    - Fine-tuning : adapter un modèle pré-entraîné sur vos données spécifiques.
    - Multi-tâches : formulation des tâches sous forme d’instructions (ex. : “Corrige ce code”, “Optimise cette fonction”).
```

## Entraînement

```
    - Objectifs de perte adaptés : génération séquentielle, apprentissage par renforcement (RLHF) pour la revue de code.
    - Validation croisée : évaluer sur des jeux de données séparés pour chaque tâche.
    - Équilibrage des tâches : éviter le surapprentissage sur une tâche au détriment des autres.
```

## Evaluation

```
    - Métriques automatiques : BLEU, CodeBLEU, Exact Match, Pass@k (exécution des tests unitaires).
    - Évaluation humaine : revue par des développeurs, analyse qualitative.
    - Tests de robustesse : évaluer sur des codes inconnus, des langages différents, des cas limites.
```

## Amélioration continue

```
    - Collecte de feedback : intégration des retours utilisateurs.
    - Retraining régulier : mise à jour avec de nouveaux exemples, corrections, optimisations.
    - Surveillance des biais et erreurs : analyse des cas d’échec pour affiner le modèle.
```

# /!\ Filtrer les exemples de code potentiellement dangereux

## Ressources utiles : 

```
    - https://paperswithcode.com/task/code-generation
    - https://github.com/openai/openai-cookbook
    - https://huggingface.co/bigcode
```