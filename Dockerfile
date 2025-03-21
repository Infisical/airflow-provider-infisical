FROM apache/airflow:2.10.5

# Strictly for local development
# COPY ./dist /opt/airflow/dist
# RUN pip install /opt/airflow/dist/airflow_provider_infisical-0.0.0-py3-none-any.whl

RUN pip install airflow-provider-infisical