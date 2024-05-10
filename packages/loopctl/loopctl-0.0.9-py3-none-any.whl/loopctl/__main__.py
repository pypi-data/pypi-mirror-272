import os
import asyncio

import fire
from itllib.resources import ResourcePile
from itllib import Itl
import yaml


def _apply_loop_resource(resources_path, secrets_path, files):
    try:
        # Collect the configs
        prior_configs = ResourcePile(resources_path, secrets_path, read_fully=True)
        new_configs = ResourcePile(*files)

        # Push the updates
        new_configs.apply(prior_configs, resources_path, secrets_path)

    except ValueError as e:
        print(e)
        print("Fix the errors and try again.")
        return


def _read_yaml_files(files):
    for f in files:
        if os.path.isfile(f):
            if f.endswith(".yaml"):
                yield f
            continue

        for root, dirs, filenames in os.walk(f):
            for filename in filenames:
                if not filename.endswith(".yaml"):
                    continue
                path = os.path.join(root, filename)
                yield path


def _apply_itl_operation(resources_path, secrets_path, client, files):
    def decorator(func):
        itl = Itl(resources_path, secrets_path, client=client)
        itl.start()

        for path in _read_yaml_files(files):
            try:
                with open(path, "r") as file:
                    data = list(yaml.safe_load_all(file))
            except:
                print(f"Error reading {path}")
                continue

            for doc in data:
                if "metadata" not in doc:
                    print(f"Missing metadata for a config in {path}")
                    continue
                metadata = doc["metadata"]
                if "name" not in metadata:
                    print(f"Missing metadata.name for a config in {path}")
                    continue
                name = metadata["name"]

                try:
                    func(itl, doc)
                except:
                    print(f"Error applying {name} in {path}")
                    raise
        itl.stop()

    return decorator


def _apply_cluster_resource(client, cluster, resources_path, secrets_path, files):
    @_apply_itl_operation(resources_path, secrets_path, client, files)
    def apply(itl, data):
        task = itl.cluster_apply(cluster, data)
        asyncio.run(task)


def _post_cluster_resource(client, cluster, resources_path, secrets_path, files):
    @_apply_itl_operation(resources_path, secrets_path, client, files)
    def post(itl, data):
        task = itl.cluster_post(cluster, data)
        asyncio.run(task)


def _delete_cluster_resource(client, cluster, resources_path, secrets_path, files):
    @_apply_itl_operation(resources_path, secrets_path, client, files)
    def delete(itl: Itl, data):
        group, version = data["apiVersion"].split("/")
        kind = data["kind"]
        name = data["metadata"]["name"]
        fiber = data["metadata"].get("fiber", "resource")
        remote = data["metadata"].get("remote")

        if remote == None:
            cluster_id = itl.get_resource("Cluster", cluster).id

        task = itl.cluster_delete(
            cluster, group, version, kind, name, fiber, cluster_id
        )
        asyncio.run(task)


def _create_cluster_resource(client, cluster, resources_path, secrets_path, files):
    @_apply_itl_operation(resources_path, secrets_path, client, files)
    def create(itl: Itl, data):
        task = itl.cluster_create(cluster, data)
        asyncio.run(task)


def _get_cluster_resource(client, cluster, resources_path, secrets_path, files):
    async def read_resource(
        itl, cluster, group, version, kind, name, fiber, cluster_id
    ):
        resource = await itl.cluster_get(
            cluster, group, version, kind, name, fiber, cluster_id
        )
        print(yaml.dump(resource, default_flow_style=False))

    @_apply_itl_operation(resources_path, secrets_path, client, files)
    def get(itl: Itl, data):
        group, version = data["apiVersion"].split("/")
        kind = data["kind"]
        name = data["metadata"]["name"]
        fiber = data["metadata"].get("fiber", "resource")
        remote = data["metadata"].get("remote")

        if remote == None:
            cluster_id = itl.get_resource("Cluster", cluster).id

        task = read_resource(
            itl, cluster, group, version, kind, name, fiber, cluster_id
        )
        asyncio.run(task)


class Commander:
    def apply(
        self,
        *files,
        client=None,
        cluster=None,
        resources="./loop-resources",
        secrets="./loop-secrets",
    ):
        """Apply the configuration in the given files."""
        if (
            resources.startswith("http:")
            or resources.startswith("https:")
            or secrets.startswith("http:")
            or secrets.startswith("https:")
        ):
            raise ValueError("The resources and secrets paths cannot be urls.")

        resources_path = os.path.realpath(resources)
        secrets_path = os.path.realpath(secrets)

        if cluster == None:
            if client:
                print(
                    "Warning: The client argument is ignored when not using --cluster."
                )
            _apply_loop_resource(resources_path, secrets_path, files)
        else:
            _apply_cluster_resource(
                client, cluster, resources_path, secrets_path, files
            )

    def post(
        self,
        cluster,
        *files,
        client=None,
        resources="./loop-resources",
        secrets="./loop-secrets",
    ):
        """Post the configuration in the given files."""
        if (
            resources.startswith("http:")
            or resources.startswith("https:")
            or secrets.startswith("http:")
            or secrets.startswith("https:")
        ):
            raise ValueError("The resources and secrets paths cannot be urls.")

        resources_path = os.path.realpath(resources)
        secrets_path = os.path.realpath(secrets)

        _post_cluster_resource(client, cluster, resources_path, secrets_path, files)

    def create(
        self,
        *files,
        client=None,
        cluster=None,
        resources="./loop-resources",
        secrets="./loop-secrets",
    ):
        """Apply the configuration in the given files."""
        if cluster == None:
            raise ValueError(
                "The cluster argument is required for create. To edit resources, use apply."
            )

        if (
            resources.startswith("http:")
            or resources.startswith("https:")
            or secrets.startswith("http:")
            or secrets.startswith("https:")
        ):
            raise ValueError("The resources and secrets paths cannot be urls.")

        resources_path = os.path.realpath(resources)
        secrets_path = os.path.realpath(secrets)

        _create_cluster_resource(client, cluster, resources_path, secrets_path, files)

    def get(
        self,
        *files,
        client=None,
        cluster=None,
        resources="./loop-resources",
        secrets="./loop-secrets",
    ):
        """Apply the configuration in the given files."""
        if cluster == None:
            raise ValueError(
                "The cluster argument is required for get. To edit resources, use apply."
            )

        if (
            resources.startswith("http:")
            or resources.startswith("https:")
            or secrets.startswith("http:")
            or secrets.startswith("https:")
        ):
            raise ValueError("The resources and secrets paths cannot be urls.")

        resources_path = os.path.realpath(resources)
        secrets_path = os.path.realpath(secrets)

        _get_cluster_resource(client, cluster, resources_path, secrets_path, files)

    def delete(
        self,
        *files,
        client=None,
        cluster=None,
        resources="./loop-resources",
        secrets="./loop-secrets",
    ):
        """Apply the configuration in the given files."""
        if cluster == None:
            raise ValueError(
                "The cluster argument is required for delete. To edit resources, use apply."
            )

        if (
            resources.startswith("http:")
            or resources.startswith("https:")
            or secrets.startswith("http:")
            or secrets.startswith("https:")
        ):
            raise ValueError("The resources and secrets paths cannot be urls.")

        resources_path = os.path.realpath(resources)
        secrets_path = os.path.realpath(secrets)

        _delete_cluster_resource(client, cluster, resources_path, secrets_path, files)


if __name__ == "__main__":
    fire.Fire(Commander(), name="loopctl")
