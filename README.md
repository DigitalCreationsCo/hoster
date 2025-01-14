---
page_type: sample
languages:
- react
- python
- azure-cli
- github-actions
products:
- azure
- azure-app-service
- azure-database-postgresql
urlFragment: django-react-azure-deployment
name: Deploy Django + React Application with PostgreSQL on Azure
---

# Deploy Django + React Application with PostgreSQL on Azure

This project deploys a full-stack web application with a Django backend and React frontend. It leverages Azure services for hosting and includes infrastructure automation with Azure Developer CLI (azd) and GitHub Actions.

## Project Features

- **Frontend Deployment**: React app hosted on Azure Blob Storage.
- **Backend Deployment**: Django app hosted on Azure App Service.
- **Database**: Azure PostgreSQL integrated with the Django application.
- **Infrastructure Automation**: Azure resources provisioned using azd and GitHub workflows.
- **Traffic Management**: Azure Application Gateway configured to route traffic efficiently.

## Running the Project Locally

1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project directory and set up the backend:
   ```sh
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set environment variables for the PostgreSQL database:
   ```sh
   export POSTGRES_HOST=<host>
   export POSTGRES_PORT=<port>
   export POSTGRES_DATABASE=<database_name>
   export POSTGRES_USERNAME=<username>
   export POSTGRES_PASSWORD=<password>
   ```
4. Apply database migrations and seed data:
   ```sh
   python3 manage.py migrate
   python3 manage.py loaddata seed_data.json
   ```
5. Start the backend server:
   ```sh
   python3 manage.py runserver 8000
   ```
6. Navigate to the frontend directory and run the React app:
   ```sh
   cd ../frontend
   npm install
   npm start
   ```

## Deployment Steps

### Prerequisites

1. Sign up for an [Azure account](https://azure.microsoft.com/free/).
2. Install the [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd).
3. Authenticate with Azure:
   ```sh
   azd auth login
   ```

### Deployment Process

1. Initialize the azd project:
   ```sh
   azd init
   ```
2. Provision resources and deploy the application:
   ```sh
   azd up
   ```
   Follow the prompts to provide an environment name, Azure subscription, and resource location.

3. For subsequent deployments after code changes:
   ```sh
   azd deploy
   ```

### CI/CD Pipeline

This project includes GitHub workflows for automatic deployments. To configure:

1. Run the following command to set up pipeline secrets:
   ```sh
   azd pipeline config
   ```
2. Push your changes to the `main` branch to trigger the workflow.

## Additional Notes

- **Terraform Support**: Terraform scripts are included for infrastructure setup but require a compatible environment with `azure-cli` installed.
- **Live Application**: Access the live app [here](Insert-live-link).

---

For any issues or questions, feel free to contact Bryant Mejia at bryantmejia722@outlook.com.
