# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2024-10-09 13:35:42
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2025-06-21 16:26:12
import kopf
from kubernetes import client, config
from config import Config
from netslice_cr_handler import NetSliceCRHandler
from itav_network_slice_manager import ITAvNetworkSliceManager

# Set up logging
logger = Config.setup_logging()

cluster = Config.cluster()

# To store the resource version for each resource to prevent duplicate processing
#processed_resource_versions = {}

def kubeconfig() -> client.CoreV1Api:
    """This is for using the kubeconfig to auth with the k8s api
    with the first try it will try to use the in-cluster config (so for in cluster use)
    If it cannot find an incluster because it is running locally, it will use your local config"""
    try:
        config.load_incluster_config()
        logger.info("Loaded in-cluster configuration.")
    except config.ConfigException as e:
        logger.warning("Failed to load in-cluster config, attempting local kubeconfig.")
        try:
            config.load_kube_config(context=cluster)
            logger.info(f"Loaded kubeconfig file with context {cluster}.")
        except config.ConfigException as e:
            logger.error("Failed to load kubeconfig: ensure your kubeconfig is valid.")
            raise

    # Now you can use the client
    api = client.CoreV1Api()
    return api

@kopf.on.create(Config.cr_group, Config.cr_version, Config.cr_plural)
def on_create_network_slice(spec, meta, logger, **kwargs):
    nslice_cr_handler.process_nslice_event("ADD", spec, meta)

@kopf.on.update(Config.cr_group, Config.cr_version, Config.cr_plural)
def on_update_network_slice(spec, old, new, diff, meta, logger, **kwargs):
    nslice_cr_handler.process_nslice_event("UPDATE", spec, meta)

def main():
    kopf.run()
    
if __name__ == '__main__':
    v1 = kubeconfig()
    custom_api = client.CustomObjectsApi()
    nslice_cr_handler = NetSliceCRHandler(
        ITAvNetworkSliceManager(
            Config.slice_manager_base_url,
            Config.slice_manager_username,
            Config.slice_manager_password
        ),
        custom_api
    )
    main()