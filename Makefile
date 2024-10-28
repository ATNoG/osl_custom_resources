# Variables
KUBECONFIG ?= /etc/rancher/k3s/k3s.yaml 
NAMESPACE = itav-slice-manager-client
SLICE_MANAGER_BASE_URL = http://10.255.28.141:8000


# Deploy Operators
install-itav-slice-manager-operators:
	# Slice Operator
	helm install --kubeconfig=$(KUBECONFIG) nslice-op-chart oci://atnog-harbor.av.it.pt/atnog/nslice-op-chart --version 0.1.0 --set sliceManagerBaseUrl=$(SLICE_MANAGER_BASE_URL) --namespace $(NAMESPACE) --create-namespace
	# UE Operator
	helm install --kubeconfig=$(KUBECONFIG) nslice-ue-op-chart oci://atnog-harbor.av.it.pt/atnog/nslice-ue-op-chart --version 0.1.0 --set sliceManagerBaseUrl=$(SLICE_MANAGER_BASE_URL) --namespace $(NAMESPACE) --create-namespace

uninstall-itav-slice-manager-operators:
	# Slice Operator
	helm uninstall --kubeconfig=$(KUBECONFIG) nslice-op-chart --namespace $(NAMESPACE)
	# UE Operator
	helm uninstall --kubeconfig=$(KUBECONFIG) nslice-ue-op-chart --namespace $(NAMESPACE)

# Log
get-nslice-operator-logs:
	kubectl logs -f $$(kubectl get pods -n $(NAMESPACE)  -l app=nslice-op -o jsonpath="{.items[0].metadata.name}") -n $(NAMESPACE) 

get-nslice-ue-operator-logs:
	kubectl logs -f $$(kubectl get pods -n $(NAMESPACE)  -l app=nslice-ue-op -o jsonpath="{.items[0].metadata.name}") -n $(NAMESPACE) 
