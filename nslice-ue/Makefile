# Variables
LOCAL_IMAGE_NAME = itav-ue-operator
LOCAL_TAG = latest

DOCKER_REPOSITORY_IMAGE_NAME = itav-ue-op
DOCKER_REPOSITORY_TAG = latest
HELM_CHART_NAME = itav-ue-op-chart
REPOSITORY_HOST = atnog-harbor.av.it.pt/atnog

HELM_CHART_NAME = itav-ue-op-chart
REPOSITORY_HOST = atnog-harbor.av.it.pt/atnog

KUBECONFIG ?= /etc/rancher/k3s/k3s.yaml 
NAMESPACE = itav-slice-manager-client


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


# Local Testing
prepare-local-testing-environment:
	kubectl apply -f ./cr/crd.yaml && kubectl apply -f ./k8s/operator-namespace.yaml && kubectl apply -f ./k8s/operator-role.yaml

terminate-local-testing-environment:
	kubectl delete -f ./cr/crd.yaml && kubectl delete -f ./k8s/operator-namespace.yaml && kubectl delete -f ./k8s/operator-role.yaml

run-local:
	. src/venv/bin/activate && CR_GROUP="av.it.pt" CR_VERSION="v1" CR_PLURAL="itav-ues" SLICE_MANAGER_BASE_URL="http://10.255.28.141:8000" SLICE_MANAGER_USERNAME="admin" SLICE_MANAGER_PASSWORD="password" python3 src/k8s_operator.py


# K8S Manifests
create-operator:
	kubectl apply -f ./cr/crd.yaml && kubectl apply -f ./k8s/operator-namespace.yaml && kubectl apply -f ./k8s/

get-operator-pods:
	kubectl get pods -n $(NAMESPACE) -l app=itav-ue-op -o jsonpath="{.items[0].metadata.name}" 

get-operator-logs:
	kubectl logs -f $$(kubectl get pods -n $(NAMESPACE)  -l app=itav-ue-op -o jsonpath="{.items[0].metadata.name}") -n $(NAMESPACE) 

delete-operator:
	kubectl delete -f ./k8s || true


# K8S Custom Resource
create-crd:
	kubectl apply -f ./cr/crd.yaml

delete-crd:
	kubectl delete -f ./cr/crd.yaml || true

create-cr:
	kubectl apply -f ./cr/cr.yaml

describe-cr:
	kubectl describe itav-ue itav-ue

delete-cr:
	kubectl delete -f ./cr/cr.yaml || true

recreate-cr: delete-cr create-cr

# HELM
helm-package:
	helm package $(HELM_CHART_NAME)

helm-push:
	helm push $(HELM_CHART_NAME)-0.1.0.tgz  oci://$(REPOSITORY_HOST)

helm: helm-package helm-push


# Deploy Operator
install-operator:
	helm install --kubeconfig=$(KUBECONFIG) $(HELM_CHART_NAME) oci://$(REPOSITORY_HOST)/$(HELM_CHART_NAME) --version 0.1.0 --set sliceManagerBaseUrl=http://10.255.28.141:8000 --namespace $(NAMESPACE) --create-namespace

uninstall-operator:
	helm uninstall --kubeconfig=$(KUBECONFIG) $(HELM_CHART_NAME) --namespace $(NAMESPACE)

