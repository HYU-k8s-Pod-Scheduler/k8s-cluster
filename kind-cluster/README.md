# HYU Graduation Project Kubernetes Cluster Setup Guide

본 문서는 [kind](https://kind.sigs.k8s.io/)를 이용하여 클러스터를 생성하고, Istio와 모니터링 툴을 설치하는 과정을 포함하고 있습니다.

## Prerequisites

클러스터 설정을 시작하기 이전에, 다음과 같은 Tool 설치가 필요합니다.

- [kubectl v1.2.40+](https://kubernetes.io/docs/tasks/tools/)
- [kind v0.22.0+](https://kind.sigs.k8s.io/)
- [istioctl v1.21+](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/)

## Setup Cluster

### 1. Setup kind cluster on your machine

아래의 명령어를 이용하여 kind 클러스터를 실행합니다.

```bash
kind create cluster --config ./kind-config.yaml
```

`kind-cinfig.yaml` 파일은 다음과 같은 설정을 포함합니다.

1. local host가 Ingress Controller에 특정 포트로 접근할 수 있도록 `extraPortMpaaings`를 이용하여 포트 개방
2. `node-labels`를 이용하여 `ingress-ready=true`인 노드에게만 트래픽이 전달될 수 있게 함

### 2. Install Ingress Nginx

Kind 클러스터에서는 물리적인 Ingress를 Provisioning 할 수 없으므로, Nginx Ingress를 설치합니다.

```bash
# 설치
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# 설치 완료 대기
kubectl wait --namespace ingress-nginx \
                --for=condition=ready pod \
                --selector=app.kubernetes.io/component=controller \
                --timeout=90s
```

### 3. Install MetaILB

Kind 클러스터에서는 물리적인 LoadBalancer를 Provisioning 할 수 없으므로, MetaILB를 설치하여 LoadBalncer 타입의 Service를 배포 가능하도록 합니다. 또, MetaILB를 통해 External IP 주소를 가질 수 있습니다.

아래의 명령어를 이용하여 MetaILB를 설치합니다.

```bash
# 설치
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml

# 설치 완료 대기
kubectl wait --namespace metallb-system \
                --for=condition=ready pod \
                --selector=app=metallb \
                --timeout=90s
```

LoadBalacner가 사용할 Address Pool을 설정합니다.

```bash
docker network inspect -f '{{.IPAM.Config}}' kind
```

MetaILB Config를 배포합니다.

```bash
kubectl apply -f https://kind.sigs.k8s.io/examples/loadbalancer/metallb-config.yaml
```

### 4. Install Istio

Kind Cluster에 istio를 설치하기 위해 Dashboard UI를 설치합니다.

```bash
# To deploy Dashboard, run the following command:
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Verify that Dashboard is deployed and running.
kubectl create serviceaccount -n kubernetes-dashboard admin-user
kubectl create clusterrolebinding -n kubernetes-dashboard admin-user --clusterrole cluster-admin --serviceaccount=kubernetes-dashboard:admin-user

# To log in to your Dashboard, you need a Bearer Token. Use the following command to store the token in a variable.
token=$(kubectl -n kubernetes-dashboard create token admin-user)

# Display the token using the echo command and copy it to use for logging in to your Dashboard.
echo $token

# Starting to serve on 127.0.0.1:8001
kubectl proxy
```

Proxy를 실행하고 난 후에는 [이 링크](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/)에 접속하여 정상적으로 설치하였는지 확인합니다.

아래의 명령어를 이용하여 istio를 클러스터에 설치합니다.

```bash
istioctl install --set profile=default -y

# envoy proxy를 default namespace에 사이드카 패턴으로 Injection할 수 있게 함
kubectl label namespace default istio-injection=enabled
```

### 5. Install Addons

Prometheus, Grafana, Kiali를 istio에서 제공하는 Addon YAML을 이용하여 설치합니다.

```bash
# Prometheus
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.21/samples/addons/prometheus.yaml

# Grafana
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.21/samples/addons/grafana.yaml

# Kiali
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.21/samples/addons/kiali.yaml
```

설치가 완료된 후에는 아래의 명령어를 이용하여 Grafana에 접속하여 설치가 정상적으로 진행되었는지 확인할 수 있습니다.

```bash
istioctl dashboard grafana
```
