from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="Jenkins Kubernetes CI/CD Demo",
    description="Sample application for automated DevOps deployment",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Jenkins Kubernetes CI/CD Project",
        "status": "success",
        "application": "FastAPI",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/info")
def application_info():
    return {
        "application": "Jenkins Kubernetes CI/CD Demo",
        "environment": "development",
        "version": "1.0.0"
    }
