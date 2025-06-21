# Variables
KUBECONFIG ?= /etc/rancher/k3s/k3s.yaml 
NAMESPACE = itav-slice-manager-client
SLICE_MANAGER_BASE_URL = http://10.255.28.141:8000
SLICE_MANAGER_USERNAME = admin
SLICE_MANAGER_PASSWORD = password


# Deploy Operators
install-itav-slice-manager-operators:
	# Slice Operator
	helm install --kubeconfig=$(KUBECONFIG) itav-netslice-op-chart oci://atnog-harbor.av.it.pt/osl-custom-resources/itav-netslice-op-chart --version 0.1.0 --set sliceManager.baseUrl=$(SLICE_MANAGER_BASE_URL) --set sliceManager.username=$(SLICE_MANAGER_USERNAME) --set sliceManager.password=$(SLICE_MANAGER_PASSWORD) --namespace $(NAMESPACE) --create-namespace

	# UE Operator
	helm install --kubeconfig=$(KUBECONFIG) itav-ue-op-chart oci://atnog-harbor.av.it.pt/osl-custom-resources/itav-ue-op-chart --version 0.1.0 --set sliceManager.baseUrl=$(SLICE_MANAGER_BASE_URL) --set sliceManager.username=$(SLICE_MANAGER_USERNAME) --set sliceManager.password=$(SLICE_MANAGER_PASSWORD) --namespace $(NAMESPACE) --create-namespace

uninstall-itav-slice-manager-operators:
	# Slice Operator
	helm uninstall --kubeconfig=$(KUBECONFIG) itav-netslice-op-chart --namespace $(NAMESPACE)
	# UE Operator
	helm uninstall --kubeconfig=$(KUBECONFIG) itav-ue-op-chart --namespace $(NAMESPACE)

# Log
get-nslice-operator-logs:
	kubectl logs -f $$(kubectl get pods -n $(NAMESPACE)  -l app=itav-netslice-op -o jsonpath="{.items[0].metadata.name}") -n $(NAMESPACE) 

get-nslice-ue-operator-logs:
	kubectl logs -f $$(kubectl get pods -n $(NAMESPACE)  -l app=itav-ue-op -o jsonpath="{.items[0].metadata.name}") -n $(NAMESPACE) 
