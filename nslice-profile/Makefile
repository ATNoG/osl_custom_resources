# Variables
LOCAL_IMAGE_NAME = nsp-operator
LOCAL_TAG = latest

DOCKER_REPOSITORY_IMAGE_NAME = nslice-profile-op
DOCKER_REPOSITORY_TAG = latest
HELM_CHART_NAME = nslice-profile-op-chart
REPOSITORY_HOST = atnog-harbor.av.it.pt/atnog

KUBECONFIG ?= /etc/rancher/k3s/k3s.yaml 

# DOCKER

docker-build:
	docker build -t $(LOCAL_IMAGE_NAME):$(LOCAL_TAG) .

docker-tag:
	docker tag $(LOCAL_IMAGE_NAME):$(LOCAL_TAG) $(REPOSITORY_HOST)/$(DOCKER_REPOSITORY_IMAGE_NAME):$(DOCKER_REPOSITORY_TAG)

docker-push:
	docker push $(REPOSITORY_HOST)/$(DOCKER_REPOSITORY_IMAGE_NAME):$(DOCKER_REPOSITORY_TAG)

docker-clean:
	docker image prune -f

docker-remove:
	docker rmi $(LOCAL_IMAGE_NAME):$(LOCAL_TAG)

docker: docker-build docker-tag docker-push


# K8S Manifests
create-operator:
	kubectl apply -f ./cr/crd.yaml && kubectl apply -f ./k8s/operator-namespace.yaml && kubectl apply -f ./k8s/

get-operator-pods:
	kubectl get pods -n nslice-profile-op -l app=nslice-profile-op -o jsonpath="{.items[0].metadata.name}" 

get-operator-logs:
	kubectl logs -f $$(kubectl get pods -n nslice-profile-op  -l app=nslice-profile-op -o jsonpath="{.items[0].metadata.name}") -n nslice-profile-op 

delete-operator:
	kubectl delete -f ./k8s || true


# K8S Custom Resource
create-cr:
	kubectl apply -f ./cr/cr.yaml

delete-cr:
	kubectl delete -f ./cr || true


