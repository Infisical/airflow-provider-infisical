# Airflow Infisical Provider

This package enables Airflow to use Infisical as a custom secrets backend.

**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Installing airflow-provider-infisical](#installing-airflow-provider-infisical)
- [Quick-start Example](#quick-start-example)
  - [Initializing Airflow](#initializing-airflow)
  - [Start the Remaining Services](#start-the-remaining-services)

## Installing airflow-provider-infisical
~~~
pip install airflow-provider-infisical
~~~

## Enabling the Infisical Secrets Backend

To enable Infisical as your secrets backend, you first need to install the `airflow-provider-infisical` package like seen in the [previous section](#installing-airflow-provider-infisical).

You can then set Infisical as your secrets backend by updating the `[secrets]` section in your `airflow.cfg` file.

```ini
[secrets]
backend = airflow.providers.infisical.secrets.infisical.InfisicalBackend
backend_kwargs = { "connections_path": "/connections-folder-path", "variables_path": "/variables-folder-path", "url": "https://app.infisical.com","auth_type": "universal-auth", "universal_auth_client_id": "<universal-auth-client-id>", "universal_auth_client_secret": "<universal-auth-client-secret>", "project_id": "<project-id>", "environment_slug": "<env-slug>" }
```

## Quick-start Example

This repository includes a `docker-compose` file designed to let you quicky set up an environment with everything needed to run the example DAG's with Infisical as the secrets backend. The `docker-compose` file is based on the file provided in the Airflow quick-start guide but with a few modifications.

* A custom `Dockerfile` to extend Airflow to include airflow-provider-infisical.

The Airflow quick-start guide and the original `docker-compose` file can be found here [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)


### Setting up your Infisical project
In order to use Infisical as your secrets backend, you need to create a [new project in Infisical](https://infisical.com/docs/documentation/platform/project) _(or use an existing project)_. Secret backends within Airflow support variables and connections. You need to create two new folders in your Infisical project for variables and connections. In this example we'll create `variables` and `connections` folders.

![Infisical Project Overview](./docs/images/infisical-overview.png)

Inside each of the folders, we'll create a new secret. Inside the `/variables` folder, we'll create a new secret called `TEST_VARIABLE` with the value `test value`. Inside the `/connections` folder, we'll create a new connection called `test_id` with the value `{"conn_id": "https://test.com"}`.

**Please note that it is important that connection secrets are formatted as JSON objects**.
<br/>Below is a full example of how a connection should be structured in Infisical:

```
conn_id (str) -- The connection ID.
conn_type (str) -- The connection type.
description (str) -- The connection description.
host (str) -- The host.
login (str) -- The login.
password (str) -- The password.
schema (str) -- The schema.
port (int) -- The port number.
extra (Union[str, dict]) -- Extra metadata. Non-standard data such as private/SSH keys can be saved here. JSON encoded object.
uri (str) -- URI address describing connection parameters.
```


#### Authenticating with Infisical through Apache Airflow

In order to authenticate with Infisical through Apache Airflow, you need to create a new machine identity in Infisical. This machine identity needs to have access to the project you want to use as a secrets backend. You will need to add the machine identity to the project that you created in the previous step. You can [read more about machine identities in the Infisical documentation](https://infisical.com/docs/documentation/platform/identities/machine-identities).

Currently the Infisical airflow provider only supports authenticating with Infisical through the Universal Auth method. You can read more about Universal Auth in the [Infisical documentation](https://infisical.com/docs/documentation/platform/identities/universal-auth).

### Configuring the custom secrets backend for Airflow
Finally, we are ready to configure the custom secrets backend for Airflow. In this quick-start example, all you'll need to do is update the `docker-compose.yaml` file. Under the `x-airflow-common.environment` section, you'll need to set the arguments for the secrets backend.

Default environment variables in your `docker-compose.yaml` file should look like this:
```yaml
# Infisical Secrets Backend Quick-start
AIRFLOW__SECRETS__BACKEND: airflow.providers.infisical.secrets.infisical.InfisicalBackend
AIRFLOW__SECRETS__BACKEND_KWARGS: '<<<ENTER-YOUR-ARGUMENTS-HERE>>>'
```

You'll need to update the `AIRFLOW__SECRETS__BACKEND_KWARGS` variable with the correct arguments for your Infisical project. The `AIRFLOW__SECRETS__BACKEND_KWARGS` variable should be formatted as a JSON object.

```yaml
  AIRFLOW__SECRETS__BACKEND_KWARGS: '{
    # The folder we created in Infisical for connections, this is where connections will be fetched from.
    "connections_path": "/connections",
    
    # The folder we created in Infisical for variables, this is where variables will be fetched from.
    "variables_path": "/variables",
    
    # The URL of your Infisical instance.
    "url": "https://app.infisical.com",
    # The authentication type to use. Currently only universal-auth is supported.
    "auth_type": "universal-auth",

    # The client ID for the universal-auth authentication type.
    "universal_auth_client_id": "<machine-identity-universal-auth-client-id>",

    # The client secret for the universal-auth authentication type.
    "universal_auth_client_secret": "<machine-identity-universal-auth-client-secret>",

    # The project ID for the Infisical project.
    "project_id": "<infisical-project-id>",

    # The environment slug for the Infisical project.
    "environment_slug": "<infisical-environment-slug>"
  }'
```

Remember to remove the comments from the above example before using it in your `docker-compose.yaml` file, or it will fail to parse the JSON object.

### Initializing Airflow
The following directories and environment files need to be created before you initialize Airflow.

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
cp ./example_dags/* ./dags/ # Copy the example DAGs to the dags folder
```

To initialize Airflow, run.
```bash
docker compose up airflow-init
```
After initialization is complete, you should see a message like this:

```yaml
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.10.5
start_airflow-init_1 exited with code 0
```

### Start the Remaining Services

To start the remaining Airflow services, run.
```bash
docker compose up -d
```