# Variables
LOCAL_IMAGE_NAME = nsp-operator
LOCAL_TAG = latest

DOCKER_REPOSITORY_IMAGE_NAME = nslice-op
DOCKER_REPOSITORY_TAG = latest
HELM_CHART_NAME = nslice-op-chart
REPOSITORY_HOST = atnog-harbor.av.it.pt/atnog

HELM_CHART_NAME = nslice-op-chart
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
	export CR_GROUP=av.it.pt && export CR_VERSION=v1 && export CR_PLURAL=networkslices && . src/venv/bin/activate && python3 src/k8s_operator.py 

# K8S Manifests
create-operator:
	kubectl apply -f ./cr/crd.yaml && kubectl apply -f ./k8s/operator-namespace.yaml && kubectl apply -f ./k8s/

get-operator-pods:
	kubectl get pods -n $(NAMESPACE) -l app=nslice-op -o jsonpath="{.items[0].metadata.name}" 

get-operator-logs:
	kubectl logs -f $$(kubectl get pods -n $(NAMESPACE)  -l app=nslice-op -o jsonpath="{.items[0].metadata.name}") -n $(NAMESPACE) 

delete-operator:
	kubectl delete -f ./k8s || true


# K8S Custom Resource
create-cr:
	kubectl apply -f ./cr/cr.yaml

delete-cr:
	kubectl delete -f ./cr/cr.yaml || true


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

