# opcp-openstack-first-steps

Cadre de formation pratique pour apprendre les bases d'OpenStack sur la plateforme OPCP (On-Premise Cloud Platform). Le projet combine un cours interactif basé sur le web (SkillHub) avec un environnement de laboratoire où les étudiants pratiquent des appels d'API réels contre un déploiement OPCP en direct.

## Structure du dépôt

```
├── skillhub/          # Site de formation statique (EN + FR)
│   ├── en/            # Leçons en anglais
│   ├── fr/            # Leçons en français
│   └── assets/        # CSS, JS (navigation, i18n, suivi de progression)
├── labs/              # Cadre de laboratoire Python
│   ├── base/          # Dockerfile, point d'entrée, dépendances pip
│   ├── core/          # Exécuteur, chargeur de configuration, évaluation, progression, limiteur de ressources
│   ├── modules/       # Modules d'exercices (first_steps, compute, networking, storage, lacp)
│   ├── templates/     # Classes de base pour les exercices et évaluations
│   ├── scripts/       # Scripts de configuration, nettoyage et validation
│   ├── config/        # lab_config.yaml (point de terminaison OpenStack, limites, ordre des modules)
│   └── tests/         # Tests unitaires
├── Specs/             # Documents de conception et spécifications
└── docs/              # Documentation opérationnelle supplémentaire
```

## SkillHub — Formation Web

SkillHub est un site statique multilingue (EN/FR) qui guide les apprenants à travers le chemin suivant :

1. **Introduction** — aperçu et validation de la configuration
2. **Prérequis** — configuration de l'environnement et outils
3. **Concepts Fondamentaux** — services OpenStack fondamentaux (Nova, Neutron, Cinder, Keystone, Glance)
4. **Gestion des utilisateurs** — création d'utilisateurs dans Keycloak et attribution des rôles OPCP
5. **Authentification** — authentification via Keystone avec des identifiants d'application
6. **Réseau** — réseaux, sous-réseaux et routeurs (Neutron)
7. **Stockage** — volumes et instantanés (Cinder)
8. **Calcul** — instances et instantanés (Nova)
9. **Configuration LACP** — agrégation de liens et configuration de bond (Neutron)
10. **Résumé et Prochaines Étapes** — récapitulatif et apprentissage supplémentaire
11. **Nettoyage des Ressources** — suppression des ressources de laboratoire
12. **Annexe A - Accès à OpenStack** — concepts fondamentaux d'OpenStack (projets, services, points de terminaison)

Ouvrez `skillhub/index.html` dans un navigateur pour commencer. Le site détecte automatiquement la langue du navigateur et redirige vers la locale appropriée.

## Labs — Exercices Pratiques

Le cadre de laboratoire s'exécute à l'intérieur d'un conteneur Docker et se connecte à un point de terminaison OpenStack réel.

### Prérequis

- Python 3.9+
- Accès à un environnement OPCP / OpenStack

### Démarrage Rapide

1. Copiez et modifiez la configuration :
   ```bash
   cp labs/config/lab_config.example.yaml labs/config/lab_config.yaml
   # Modifier le point de terminaison, le type d'instance et l'image pour correspondre à votre environnement
   ```

2. Définissez vos identifiants :

   **Utilisateur / Mot de passe**
   ```bash
   export OS_AUTH_URL="https://auth.cloud.example.com/v3"
   export OS_USERNAME="<votre-nom-d'utilisateur>"
   export OS_PASSWORD="<votre-mot-de-passe>"
   export OS_PROJECT_NAME="<votre-projet>"
   export OS_DOMAIN_NAME="Default"
   ```

   **Option — Identifiants d'Application (pour compte de service uniquement)**
   ```bash
   export OS_AUTH_URL="https://auth.cloud.example.com/v3"
   export OS_AUTH_TYPE="v3applicationcredential"
   export OS_APPLICATION_CREDENTIAL_ID="<votre-id>"
   export OS_APPLICATION_CREDENTIAL_SECRET="<votre-secret>"
   ```

3. Construisez et exécutez le conteneur de laboratoire :
   ```bash
   docker build -t opcp-labs -f labs/base/Dockerfile labs/
   docker run --env-file .env opcp-labs --module first_steps --student-id <votre-id>
   ```

### Aperçu des Modules

|    Module   | Exercices |                      Sujets                             |
|-------------|-----------|---------------------------------------------------------|
| first_steps | 3         | Créer une instance, réseau, volume                      |
| compute     | 3         | Lancer, redimensionner, instantanés                     |
| networking  | 3         | Réseau, sous-réseau, routeur                            |
| storage     | 3         | Volume, attacher, instantanés                           |
| lacp        | 3         | Créer un bond, configurer LACP, attacher à une instance |

Chaque exercice fournit un énoncé de problème, des instructions étape par étape, une évaluation automatisée et une solution de référence dans `solutions/`.

### Nettoyage

```bash
python3 -m labs.scripts.cleanup_lab --student-id <votre-id>
```

## Licence

Libre.