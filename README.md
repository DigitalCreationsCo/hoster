# Hoster

Effortless cloud hosting for React and static web applications — deploy full-stack projects to Azure with zero configuration.

---

## Overview

**Hoster** is a **Python + Django-based deployment automation platform** built to host React applications and static websites on Azure with minimal setup. It integrates backend, frontend, and infrastructure provisioning into one unified workflow — enabling developers to deploy and manage production-grade applications with zero manual configuration.

Whether you’re deploying a personal project or a full-scale web platform, Hoster simplifies the entire process — from environment creation and PostgreSQL configuration to automated CI/CD and secure secret management.

---

## Key Features

* **Zero-Config Deployment** — One-command hosting for static sites and full-stack React+Django apps.
* **Fully Managed Backend** — Django backend deployed automatically to **Azure App Service**.
* **Static Frontend Hosting** — React bundle deployed to **Azure Blob Storage** with CDN acceleration.
* **Integrated PostgreSQL Database** — Managed PostgreSQL instance provisioned and connected automatically.
* **Azure Key Vault Integration** — Securely store and manage sensitive credentials with automatic retrieval during deployment.
* **GitHub Actions CI/CD** — End-to-end continuous integration pipeline triggered on every push to `main`.
* **Infrastructure Automation** — Built-in scripts and workflows handle Azure provisioning, environment generation, and deployment orchestration.
* **Environment Generation Scripts** — `.env` files created automatically for dev and production environments via Azure CLI.
* **Cross-Platform Ready** — Works on macOS, Linux, and Windows environments using the Azure Developer CLI (azd).

---

## Tech Stack

* **Backend:** Python, Django
* **Frontend:** React (static or single-page app)
* **Database:** Azure Database for PostgreSQL
* **Infrastructure:** Azure App Service, Azure Blob Storage, Azure Key Vault
* **Automation:** Azure Developer CLI (`azd`), GitHub Actions
* **Deployment:** Azure Cloud + GitHub CI/CD

---

## Architecture Overview

```
Frontend (React App)
     ↓ (Static Build)
Azure Blob Storage + CDN
     ↑
Backend (Django App)
Azure App Service
     ↑
PostgreSQL (Managed DB)
     ↑
Azure Key Vault + GitHub Actions
```

Hoster orchestrates deployment across all Azure components, ensuring the frontend, backend, and database remain tightly synchronized through automated workflows.

---

## Automatic Environment Configuration

### `create-prod-env.py`

A Python script that generates `.env.production` automatically by pulling Azure configuration via CLI commands. It fetches:

* Azure Subscription & Tenant IDs
* Client credentials and resource group details
* Storage account information
* PostgreSQL connection parameters

The result is a fully configured `.env.production` ready for secure deployment.

### `master_hoster.yml`

A GitHub Actions workflow that:

1. Builds backend and frontend projects.
2. Authenticates with Azure using a service principal.
3. Fetches production environment variables from Azure Key Vault.
4. Deploys Django backend to Azure App Service.
5. Uploads React bundle to Azure Blob Storage.

This pipeline provides consistent, repeatable deployments from source to production with no manual steps required.

---

## Secure Secret Management with Azure Key Vault

Sensitive variables (database passwords, API keys, client secrets) are stored in **Azure Key Vault**. During the CI/CD pipeline:

* The GitHub Action authenticates via the Azure service principal.
* Secrets are retrieved using `az keyvault secret show`.
* Environment variables are injected securely into the runtime.

This ensures end-to-end security, auditability, and compliance for all sensitive deployment configurations.

---

## Local Development

```bash
# Clone the repository
git clone <repo-url> hoster
cd hoster/backend

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Apply migrations and run the backend
python3 manage.py migrate
python3 manage.py runserver 8000

# Run React frontend
cd ../frontend
npm install
npm start
```

---

## Deployment Steps

```bash
# Authenticate with Azure
azd auth login

# Initialize Azure resources
azd init

# Provision and deploy
azd up
```

Subsequent deployments:

```bash
azd deploy
```

To configure CI/CD:

```bash
azd pipeline config
```

Push to `main` to trigger automatic deployment.

---

## License

MIT License

Best regards,
Bryant Mejia
