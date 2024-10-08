import kopf
from kubernetes import client, config, watch
from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_pod import V1Pod
from kubernetes.client.models.v1_container_status import V1ContainerStatus
import requests
import threading

from config import Config
from itav_network_slice_manager import ITAvNetworkSliceManager

# Set up logging
logger = Config.setup_logging()


class NetworkSliceProfileCRHandler:

    processed_resource_versions = {}

    def __init__(
        self, core_api: client.CoreV1Api,
        custom_objects_api: client.CustomObjectsApi,
        slice_manager: ITAvNetworkSliceManager
    ):
        self.core_api = core_api
        self.custom_objects_api = custom_objects_api
        self.slice_manager = slice_manager

        
    def process_event(self, event: dict) -> None:
          
        event_type = event['type']
        resource = event['object']
        resource_name = resource['metadata']['name']
        resource_version = resource['metadata']['resourceVersion']
        resource_namespace = resource['metadata']['namespace']
        
        # Custom Resource Data
        spec_network_slice = resource["spec"]["network-slice"]
        spec_network_slice_profile = spec_network_slice["profile"]
        spec_profile_enforcement = resource['spec'].get("profile-enforcement")

        logger.info(f"Received {event_type} event for {resource_name} with resourceVersion {resource_version}")
        
        # Check if the resource version has already been processed
        if resource_name in self.processed_resource_versions:
            if self.processed_resource_versions[resource_name] == resource_version:
                logger.info(f"Skipping already processed event for {resource_name} with resourceVersion {resource_version}")
                return
        
        logger.info(f"Event: {event}")

        # Handle the event, if needed
        if (
            (event_type == "ADDED" and 
            (not spec_profile_enforcement or 
            spec_profile_enforcement.get("enforced-profile") != spec_network_slice_profile)
            ) 
            or 
            (event_type == "MODIFIED" and 
            (spec_profile_enforcement.get("enforced-profile") not in (None, spec_network_slice_profile))
            )
        ):
            logger.info(f"Processing {event_type} event for {resource_name}")
            self.process_network_slice_profile_enforcement(resource_namespace, resource_name, spec_network_slice_profile)
            self.processed_resource_versions[resource_name] = resource_version
        else:
            logger.info(f"Skipping network slice profile enforcement for {resource_name} with resourceVersion {resource_version}")

    
    def process_network_slice_profile_enforcement(self, namespace: str, name: str, slice_profile: str) -> None:
        
        profile_enforcement_result = self.slice_manager.enforce_profile(
            slice_profile
        )
        
        # Define the patch payload to update 
        patch = {
            "spec": {
                "profile-enforcement": profile_enforcement_result
            }
        }

        try:
            # Apply the patch to update 'spec.data2' of the custom resource
            self.custom_objects_api.patch_namespaced_custom_object(
                group=Config.cr_group,
                version=Config.cr_version,
                namespace=namespace,
                plural=Config.cr_plural,
                name=name,
                body=patch
            )
            logger.info(f"Updated 'spec.profile-enforcement' for {name} in {namespace} to {profile_enforcement_result}")
        except client.exceptions.ApiException as e:
            logger.error(f"Exception when updating 'spec.profile-enforcement' in custom resource: {e}")


