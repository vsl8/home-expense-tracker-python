# GitHub Actions Environments Setup Guide

This document provides instructions for setting up GitHub repository environments for the CI/CD pipeline.

## Overview

The pipeline uses three environments with progressive deployment:
- **DEV** - Development environment (automatic deployment)
- **QA** - Quality Assurance environment (automatic after DEV)
- **PROD** - Production environment (requires approval)

## Setting Up Environments

### 1. Navigate to Repository Settings

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click **Environments**

### 2. Create DEV Environment

1. Click **New environment**
2. Name: `dev`
3. Click **Configure environment**
4. Optional: Add deployment branch rules
5. Click **Save protection rules**

### 3. Create QA Environment

1. Click **New environment**
2. Name: `qa`
3. Click **Configure environment**
4. Optional: Add deployment branch rules (e.g., only `main`)
5. Click **Save protection rules**

### 4. Create Production Environment (with Approval)

1. Click **New environment**
2. Name: `production`
3. Click **Configure environment**
4. Enable **Required reviewers**
5. Add reviewer(s) who can approve production deployments
6. Optional: Set **Wait timer** (e.g., 5 minutes)
7. Add deployment branch rule: `main` only
8. Click **Save protection rules**

## Setting Up Secrets

### Repository Secrets

Navigate to **Settings** > **Secrets and variables** > **Actions**

Add the following secrets:

#### SonarQube Integration

| Secret Name | Description |
|-------------|-------------|
| `SONAR_TOKEN` | SonarQube authentication token |
| `SONAR_HOST_URL` | SonarQube server URL (e.g., `https://sonarqube.example.com`) |

#### Deployment Secrets (per environment)

Each environment may need specific secrets:

| Secret Name | Description |
|-------------|-------------|
| `DEPLOY_KEY` | SSH key for server deployment |
| `DEPLOY_HOST` | Deployment server hostname |
| `DEPLOY_USER` | Deployment server username |

### Creating Environment-Specific Secrets

1. Go to **Settings** > **Environments** > Select environment
2. Under **Environment secrets**, click **Add secret**
3. Add secrets specific to that environment

## SonarQube Setup

### 1. Create Project in SonarQube

1. Log in to your SonarQube instance
2. Create a new project
3. Note the project key

### 2. Generate Token

1. Go to **My Account** > **Security**
2. Generate a new token
3. Copy the token and add it as `SONAR_TOKEN` secret

### 3. Configure Quality Gate (Optional)

1. Go to **Quality Gates** in SonarQube
2. Create or modify a quality gate with these rules:
   - Coverage on New Code >= 80%
   - Duplicated Lines on New Code <= 3%
   - Maintainability Rating = A
   - Reliability Rating = A
   - Security Rating = A

## Deployment Configuration

### Option 1: Azure App Service

Add these secrets for Azure deployment:

```yaml
AZURE_WEBAPP_NAME: your-app-name
AZURE_WEBAPP_PUBLISH_PROFILE: <publish profile XML>
```

Update deployment step in workflow:
```yaml
- name: Deploy to Azure Web App
  uses: azure/webapps-deploy@v2
  with:
    app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
    publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
    package: expense-tracker-${{ github.sha }}.tar.gz
```

### Option 2: AWS Elastic Beanstalk

Add these secrets:
```yaml
AWS_ACCESS_KEY_ID: your-access-key
AWS_SECRET_ACCESS_KEY: your-secret-key
AWS_REGION: us-east-1
EB_APPLICATION_NAME: expense-tracker
EB_ENVIRONMENT_NAME: expense-tracker-env
```

### Option 3: Self-Hosted Server (SSH)

Add these secrets:
```yaml
DEPLOY_HOST: server.example.com
DEPLOY_USER: deploy
DEPLOY_KEY: <SSH private key>
DEPLOY_PATH: /var/www/expense-tracker
```

Update deployment step:
```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USER }}
    key: ${{ secrets.DEPLOY_KEY }}
    script: |
      cd ${{ secrets.DEPLOY_PATH }}
      tar -xzf expense-tracker-*.tar.gz
      pip install -r requirements.txt
      sudo systemctl restart expense-tracker
```

## Branch Protection Rules

### Recommended Setup for `main` Branch

1. Go to **Settings** > **Branches**
2. Add rule for `main`
3. Enable:
   - Require a pull request before merging
   - Require status checks to pass
     - Select: `lint`, `test`
   - Require branches to be up to date
   - Include administrators

## Troubleshooting

### Pipeline Fails at SonarQube Step

- Verify `SONAR_TOKEN` is correctly set
- Verify `SONAR_HOST_URL` is accessible
- Check SonarQube server logs

### Production Deployment Stuck

- Check if required reviewers have approved
- Verify reviewer has appropriate permissions
- Check the Actions tab for approval button

### Caching Not Working

- Verify `hashFiles('requirements.txt')` matches your file
- Clear cache in **Actions** > **Caches** if needed

## Pipeline Flow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Lint     │────▶│    Test     │────▶│ SonarQube   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Build    │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Deploy DEV  │  ◀── Automatic
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Deploy QA   │  ◀── Automatic (main only)
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Deploy PROD │  ◀── Requires Approval
                    └─────────────┘
```
