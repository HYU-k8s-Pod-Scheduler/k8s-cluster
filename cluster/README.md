# HYU Graduation Project Kubernetes Cluster Setup Guide

본 가이드에서는 Multi Cluster와 Karmada를 구축하여, Cluster Federation 환경을 구성합니다.

## Prerequisites

클러스터 설정을 시작하기 이전에, 다음과 같은 Tool 설치가 필요합니다.

- [Go v1.18+](https://go.dev/)
- [kubectl v1.19+](https://istio.io/latest/docs/setup/getting-started/#download)
- [kind v0.14.0+](https://minikube.sigs.k8s.io/docs/start/)

## Setup Cluster

### 1. Setup Control/Member Clusters & Join Karmada

다음과 같은 명령어를 실행하여, Kind에서 Karmada의 Control Cluster와 Member Cluster를 실행하고, Karamada에 Join 합니다.

```bash
sh ./local-up-karmada.sh
```

본 스크립트는 아래와 같은 내용을 포함합니다.

- Start a Kubernetes cluster to run the Karmada control plane, aka. the host cluster.
- Build Karmada control plane components based on a current codebase.
- Deploy Karmada control plane components on the host cluster.

#### Reference

- [Propagate a deployment by Karmada](https://karmada.io/docs/get-started/nginx-example/)

## Clean Up

환경을 정리하기 위해서 다음의 명령어를 사용할 수 있습니다.

```bash
sh ./local-down-karmada.sh
```
