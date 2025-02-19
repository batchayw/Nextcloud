# Nextcloud-Proxmox-Traefik-MinIO-Ansible

Ce projet permet de déployer **Nextcloud** dans une VM sur **Proxmox**, avec une gestion sécurisée via **Traefik** pour le HTTPS, et un stockage externe **MinIO**. Tout cela est automatisé à l'aide d'**Ansible**. Puis une pipeline **CI/CD GitHub Actions** pour déployer Nextcloud avec Proxmox, Ansible, MinIO et Traefik, avec envoie des alertes après déploiement sur **Slack**.

## Prérequis

- ***Proxmox VE*** installé et configuré (un serveur Proxmox installé et accessible).
- ***Docker*** et ***Docker Compose*** sur la VM cible.
- ***Traefik*** pour la gestion du HTTPS (certificats Let's Encrypt).
- ***MinIO*** pour le stockage des fichiers ***Nextcloud*** (peut être local ou distant).
- ***Ansible*** pour l'automatisation des tâches.
- Un domaine configuré pour utiliser avec ***Traefik*** (ex. `nextcloud.example.com`).
- ***Slack*** pour envoyer une alerte Slack après déploiement.
- ***Python*** pour vérifie si Nextcloud est bien en ligne.

## Structure du projet

```bash
README.md                    # Documentation du projet
LICENSE                      # License du projet (Auteur William)
nextcloud-proxmox-ansible/
│── inventory.ini            # Inventaire Ansible (Proxmox + VM Nextcloud)
│── ansible.cfg              # Configuration Ansible
│── create_vm_proxmox.yml    # Création de la VM sur Proxmox
│── install_nextcloud.yml    # Installation de Nextcloud sur la VM
│── backup_vm_proxmox.yml    # Sauvegarde de la VM Proxmox
│── group_vars/              # Variables Ansible
│   ├── proxmox.yml          # Configs spécifiques à Proxmox
│   ├── nextcloud.yml        # Configs spécifiques à Nextcloud
│── roles/                   # Rôles Ansible (optionnel pour modulariser)
│   ├── proxmox/             # Rôle pour gérer Proxmox
│   ├── nextcloud/           # Rôle pour configurer Nextcloud
│── files/                   # Fichiers à copier sur les machines
│   ├── docker-compose.yml   # Fichier Docker Compose pour Nextcloud
│   ├── ssh-key.pub          # Clé SSH pour accès sécurisé
│── logs/                    # Logs des exécutions Ansible
│── tests/                   
│   ├── check_nextcloud.py   # Vérifier que Nextcloud est bien accessible
│── img/                   
│   ├── check_nextcloud.py   # Code xml du diagramme fonctionnel à visualiser sur Draw.io
│── .github/                   
│   ├── workflows 
│   │   ├── main.yml         # Pipeline GitHub Actions
```

## Installation et Configuration

1. **Configurer Proxmox**

    - Création d'une VM: Utilise le fichier `create_vm_proxmox.yml` pour créer une machine virtuelle sur ton serveur Proxmox.
        - Spécifie la configuration de la VM (nom, ressources, etc.) dans le fichier `group_vars/proxmox.yml`.
    - Accès SSH sécurisé: La clé SSH est ajoutée dans `files/ssh-key.pub` pour un accès sécurisé à la VM.

2. **Configurer Nextcloud avec Docker**

    - Docker Compose: Le fichier `files/docker-compose.yml` configure Nextcloud avec Traefik pour un accès HTTPS, et MinIO comme stockage externe.
        - Assure-toi d'avoir configuré les bonnes clés et secrets pour MinIO dans `group_vars/nextcloud.yml`.

3. **Configurer Traefik pour HTTPS**

    - Traefik est configuré dans le fichier `docker-compose.yml` pour gérer les certificats SSL via Let's Encrypt et rediriger le trafic HTTP vers HTTPS.
    - Modifie la variable `NEXTCLOUD_DOMAIN` dans `group_vars/nextcloud.yml` pour refléter ton domaine (ex. `nextcloud.example.com`).

## Déploiement avec Ansible

1. **Inventaire Ansible:**

L'inventaire `inventory.ini` liste les machines cibles (Proxmox et VM Nextcloud). Assure-toi que les adresses IP et les clés SSH sont bien configurées.

2. **Créer la VM sur Proxmox:**

Exécute le playbook `create_vm_proxmox.yml` pour créer la VM sur ton hôte Proxmox.

```bash
ansible-playbook create_vm_proxmox.yml -i inventory.ini
```

3. **Installer Nextcloud sur la VM:**

Après avoir créé la VM, déploie Nextcloud avec ce playbook:

```bash
ansible-playbook install_nextcloud.yml -i inventory.ini
```

4. **Sauvegarde de la VM Proxmox:**

Tu peux automatiser la sauvegarde de la VM avec `backup_vm_proxmox.yml`:

```bash
ansible-playbook backup_vm_proxmox.yml -i inventory.ini
```

## Configuration de MinIO

1. **MinIO avec Docker:** Le fichier docker-compose.yml déploie MinIO et le configure avec les identifiants d'accès:
    - ***MINIO_ROOT_USER:*** Nom d'utilisateur pour MinIO.
    - ***MINIO_ROOT_PASSWORD:*** Mot de passe pour MinIO.

2. Utiliser **MinIO pour Nextcloud**: Dans le fichier `install_nextcloud.yml`, configure les variables d'environnement pour connecter Nextcloud à MinIO comme stockage externe.

    ```yaml
    NEXTCLOUD_OBJECTSTORE_S3_HOST: "minio:9000"
    NEXTCLOUD_OBJECTSTORE_S3_BUCKET: "nextcloud-bucket"
    NEXTCLOUD_OBJECTSTORE_S3_KEY: "adminaccess"
    NEXTCLOUD_OBJECTSTORE_S3_SECRET: "secretpassword"
    ```

## Accès à Nextcloud

1. **Accès Web:** Une fois l'installation terminée, tu peux accéder à Nextcloud via le domaine configuré dans Traefik (ex: `https://nextcloud.example.com`).
2. **Connexion:** Utilise les identifiants configurés pour l'admin dans `group_vars/nextcloud.yml`.

## Logs et Dépannage

- **Logs d'Ansible:** Les logs d'exécution sont stockés dans le dossier logs/. Vérifie-les si une erreur survient lors de l'exécution des playbooks.

- **Problèmes avec Traefik:** Si le certificat SSL n'est pas généré, vérifie les logs de Traefik à l'adresse `http://<ton-ip>:8080`.

- **MinIO:** Si MinIO n'est pas accessible, vérifie sa configuration dans le fichier `docker-compose.yml` et dans les variables d'environnement d'Ansible.


## Remarques:

- ***📌 Configuration GitHub Actions (Secrets & Variables)***

    Ajoute ces secrets **GitHub dans Settings** > **Secrets and variables** > **Actions:**
    - *PROXMOX_API_TOKEN=*	Token API Proxmox
    - *SLACK_WEBHOOK_URL=*	URL Webhook Slack
    - *ANSIBLE_USER=*	Utilisateur SSH pour Ansible 
    - *ANSIBLE_PASSWORD=*	Mot de passe SSH pour Ansible

- ***⚠️ Attention:***  

    pour avoir le ***Token API Proxmox***, tu dois te connecter  a ton serveur Proxmox et suivre les etapes suivants:
    - Va dans **Datacenter** > **API Tokens**.
    - Clique sur "**Add**".
    - Sélectionne l’utilisateur (**ansible_user**).

        Remplis les champs:
        - **Token ID**: ansible-token.
        - **Permissions**: **PVEAdmin** (Attention, accès complet).
    - Coche "**Privileged**" (pour un accès total).

    - Clique sur "**Add**".
    - Copie immédiatement le Token généré, il ressemble à ceci (Tu ne pourras plus le voir après):

    ```bash
    ansible_user!ansible-token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```

## Notes: 
- En suivant bien les étapes décrites, tu devrais obtenir une ***pipeline CI/CD*** fonctionnelle ainsi qu'une ***architecture opérationnelle***.
- Pour visualiser l'architecture, impoter le fichier `img/draw.xml` dans l'outil draw.io.

## Conclusion

Ce projet automatise le déploiement de **Nextcloud** avec **Traefik** et **MinIO** en utilisant **Proxmox** pour la virtualisation, **Ansible** pour l'orchestration et **Slack**pour la notification des alertes. Cela permet de simplifier le processus de mise en place d'un environnement *Nextcloud sécurisé et évolutif*.