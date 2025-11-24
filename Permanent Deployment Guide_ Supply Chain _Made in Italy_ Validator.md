# Permanent Deployment Guide: Supply Chain "Made in Italy" Validator

This guide provides the steps and files necessary to permanently deploy your Streamlit application using Docker on a cloud platform (e.g., AWS, Google Cloud, Azure, DigitalOcean, or a dedicated Streamlit hosting service).

## 1. Prerequisites

Before starting, ensure you have the following:

1.  **The complete project folder** (`supply-chain-validator/`) downloaded to your local machine.
2.  **Docker** installed on your local machine.
3.  An account with a **Cloud Provider** (e.g., AWS, GCP, Azure) or a dedicated Streamlit hosting service.

## 2. Deployment Files

The following files have been added to your project to facilitate Docker deployment:

| File | Purpose |
|---|---|
| `Dockerfile` | Defines the container environment (Python 3.11, dependencies, exposed port). |
| `start.sh` | The script that executes the Streamlit application inside the container. |
| `requirements.txt` | Lists all Python dependencies. |
| `app.py` | The main Streamlit application file. |

## 3. Local Docker Build and Run (Testing)

You can test the container locally before deploying it to the cloud.

### Step 3.1: Build the Docker Image

Open your terminal, navigate to the `supply-chain-validator` directory, and run the build command:

```bash
# Build the image and tag it
docker build -t supply-chain-validator:latest .
```

### Step 3.2: Run the Container

Run the image, mapping the container's internal port 8501 to a port on your local machine (e.g., 8080):

```bash
# Run the container in detached mode (-d)
docker run -d -p 8080:8501 --name supply-chain-app supply-chain-validator:latest
```

### Step 3.3: Verify

Open your web browser and navigate to `http://localhost:8080`. Your application should be running.

## 4. Cloud Deployment (Production)

The most common and robust way to deploy a containerized application is via a cloud service. The general steps are:

### Step 4.1: Push to a Container Registry

You need to push your image to a public or private registry (e.g., Docker Hub, AWS ECR, Google Container Registry).

**Example (Docker Hub):**

```bash
# 1. Log in to Docker Hub
docker login

# 2. Tag the image with your username/repository name
docker tag supply-chain-validator:latest yourusername/supply-chain-validator:latest

# 3. Push the image
docker push yourusername/supply-chain-validator:latest
```

### Step 4.2: Deploy to a Cloud Service

Once the image is in a registry, you can deploy it using various services:

| Cloud Service | Recommended Deployment Method | Notes |
|---|---|---|
| **Streamlit Community Cloud** | Direct connection to your GitHub repository. | Easiest method, but requires a public GitHub repo. |
| **AWS** | **AWS App Runner** or **ECS (Fargate)** | App Runner is the simplest for a single container. |
| **Google Cloud** | **Cloud Run** | Excellent for serverless container deployment. |
| **Azure** | **Azure Container Apps** | Managed service for microservices and containers. |
| **DigitalOcean** | **App Platform** or **Droplet + Docker** | App Platform is simpler; Droplet gives more control. |

**General Deployment Configuration:**

- **Image Source**: `yourusername/supply-chain-validator:latest`
- **Port**: `8501` (Must match the `EXPOSE` in the Dockerfile)
- **Environment Variables**: You may need to set the `OPENAI_API_KEY` environment variable in your cloud service's configuration panel if you switch to a live Neo4j instance or a different LLM.

## 5. Final Files for Your Reference

### `Dockerfile`

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the application using the start script
CMD ["./start.sh"]
```

### `start.sh`

```bash
#!/bin/bash

# Ensure the script is executable
chmod +x start.sh

# Set Streamlit to run on all interfaces and not open a browser
# The --server.port is set to 8501 to match the EXPOSE instruction in the Dockerfile
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

With these files and instructions, you are fully equipped to deploy your **Supply Chain "Made in Italy" Validator** permanently!
