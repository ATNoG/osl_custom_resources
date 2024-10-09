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

# HELM
helm-package:
	helm package $(HELM_CHART_NAME)

helm-push:
	helm push $(HELM_CHART_NAME)-0.1.0.tgz  oci://$(REPOSITORY_HOST)


# Deploy Operator
install-operator:
	helm install --kubeconfig=$(KUBECONFIG) $(HELM_CHART_NAME) oci://$(REPOSITORY_HOST)/$(HELM_CHART_NAME) --version 0.1.0 --set sliceManagerBaseUrl=http://10.16.10.74:8000 --namespace nslice-profile-op --create-namespace

uninstall-operator:
	helm uninstall --kubeconfig=$(KUBECONFIG) $(HELM_CHART_NAME) --namespace nslice-profile-op

# K8S Manifests
#create-operator:
#	kubectl apply -f ./cr/crd.yaml && kubectl apply -f ./cr/cr.yaml && kubectl apply -f ./k8s/operator-namespace.yaml && kubectl apply -f ./k8s/
#
#get-operator-pods:
#	kubectl get pods -n nslice-profile-op -l app=nslice-profile-op -o jsonpath="{.items[0].metadata.name}" 
#
get-operator-logs:
	kubectl logs -f $$(kubectl get pods -n nslice-profile-op  -l app=nslice-profile-op -o jsonpath="{.items[0].metadata.name}") -n nslice-profile-op 

#delete-operator:
#	kubectl delete -f ./k8s || true
#
#delete-cr:
#	kubectl delete -f ./cr || true
#

docker: docker-build docker-tag docker-push
helm: helm-package helm-push
create_and_push_artifacts: docker helm
redeploy: delete-operator delete-cr docker create-operator
