from __future__ import annotations

__version__ = "0.0.0"

def get_provider_info():
    return {
        "package-name": "airflow-provider-infisical",
        "name": "Infisical",
        "description": "An Airflow provider to connect to Infisical",
        "secrets-backends": ["airflow.providers.infisical.secrets.infisical.InfisicalBackend"],
        "optional-dependencies": {"boto3": ["boto3>=1.33.0"], "google": ["apache-airflow-providers-google"]},
        "devel-dependencies": [],
        "dependencies": ["apache-airflow>=2.9.0", "infisicalsdk>=1.0.6"],
        "versions": [__version__],
    }