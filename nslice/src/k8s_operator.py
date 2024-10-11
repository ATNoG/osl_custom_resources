import kopf
import json
from kubernetes import client, config, watch
from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_pod import V1Pod
from kubernetes.client.models.v1_container_status import V1ContainerStatus
import time

from config import Config
from nslice_cr_handler import NSliceCRHandler
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


def watch_network_slice_profile_resources(v1: client.CoreV1Api, custom_api: client.CustomObjectsApi) -> None:
    """Watch all custom resources in all namespaces"""
    logger.info(f"Watching all custom resources of type {Config.cr_group}/{Config.cr_version}/{Config.cr_plural} across all namespaces")
    w = watch.Watch()


    # Use CustomObjectsApi to list and watch custom resources at the cluster level
    while True:
        for event in w.stream(custom_api.list_cluster_custom_object, Config.cr_group, Config.cr_version, Config.cr_plural, timeout_seconds=10):
            logger.info(f"Event: {event}")
        time.sleep(Config.interval)
        

#@kopf.on.startup()
#def on_startup(**kwargs):
#    """On startup, watch pods"""
#    logger.info("Starting up")
#    watch_network_slice_profile_resources(v1, custom_api)    
#    
#@kopf.on.timer(Config.cr_group, Config.cr_version, Config.cr_plural,interval=Config.interval)
#def on_timer(**kwargs):
#    """On timer, watch pods"""
#    logger.info("Starting up on timmer")
#    watch_network_slice_profile_resources(v1, custom_api)


@kopf.on.create(Config.cr_group, Config.cr_version, Config.cr_plural)
def create_fn(spec, logger, **kwargs):

    nslice_cr_handler.logger = logger
    nslice_cr_handler.process_nslice_add_event(spec)



def main():
    kopf.run()
    
if __name__ == '__main__':
    v1 = kubeconfig()
    custom_api = client.CustomObjectsApi()
    nslice_cr_handler = NSliceCRHandler(
        ITAvNetworkSliceManager("http://10.10.10.10:1000")
    )
    main()