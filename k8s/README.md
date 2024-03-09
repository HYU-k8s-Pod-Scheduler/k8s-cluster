# HYU Graduation Project Kubernetes Cluster Setup Guide

## Prerequisites

클러스터 설정을 시작하기 이전에, 다음과 같은 Tool 설치가 필요합니다.

- [kubectl v1.2.40+](https://kubernetes.io/docs/tasks/tools/)
- [Helm v3.0+](https://helm.sh/docs/intro/install/)
- [istioctl v1.17+](https://istio.io/latest/docs/setup/getting-started/#download)
- [Minikube v1.30+](https://minikube.sigs.k8s.io/docs/start/)

## Setup Cluster

### 1. Setup minikube on your machine

다음과 같은 명령어를 실행하여 로컬 환경에 단일 클러스터를 구축합니다.

```bash
minikube start
```

이후에 배포되는 Application에 접속을 가능하게 하기 위해 `ingress` addon을 설치하여 `nginx ingress controller`를 활성화합니다.

```bash
minikube addons enable ingress
```

### 2. Install Istio with `istioctl`

`istioctl`를 이용하여 Istio를 클러스터에 설치합니다.

```bash
istioctl install
```

#### Reference

- [Install with `istioctl`](https://istio.io/latest/docs/setup/install/istioctl/)

### 3. Install Prometheus

Istio에서 제공하는 Prometheus 설치 YAML 파일을 이용하여 Prometheus를 설치합니다.

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
```

#### Reference

- [Istio - Prometheus](https://istio.io/latest/docs/ops/integrations/prometheus/#option-1-quick-start)

### 4. Install Grafana

Istio에서 제공하는 Grafana 설치 YAML 파일을 이용하여 Grafana를 설치합니다.

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
```

다음의 명령어를 이용하여 Grafana 대시보드 동작을 확인할 수 있습니다.

```bash
istioctl dashboard grafana
```

#### Reference

- [Istio - Grafana](https://istio.io/latest/docs/ops/integrations/grafana/#option-1-quick-start)