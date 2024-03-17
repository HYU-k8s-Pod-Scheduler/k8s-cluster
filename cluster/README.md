# HYU Graduation Project Kubernetes Cluster Setup Guide

본 디렉토리는 VirtualBox 기반의 Kubernetes Cluster 구축과 관련된 파일들을 포함합니다.

## Prerequisites

클러스터 설정을 시작하기 이전에, 다음과 같은 Tool 설치가 필요합니다.

- [Vagrant v2.4.1+](https://developer.hashicorp.com/vagrant/install)
- [VirtualBox v7.0+](https://www.virtualbox.org/)

## SetUp Cluster

### 1. Setup VirtualBox cluster on your machine

다음과 같은 명령어를 실행하여 VirtualBox 클러스터를 구축합니다.

```bash
vagrant up
```

### 2. Copy the config file to `.kube` directory

`kubectl` config를 복사합니다.

```bash
cp configs/config ~/.kube/
```

### 3. Access to Kubernetes Dashboard

Kubernetes Dashboard에 접근하여 클러스터가 정상적으로 설정되었는지 확인합니다.

먼저, 아래 명령어를 이용하여 login token을 획득합니다.

```bash
kubectl -n kubernetes-dashboard get secret/admin-user -o go-template="{{.data.token | base64decode}}"
```

Proxy를 실행합니다.

```bash
kubectl port-forward service/kubernetes-dashboard -n kubernetes-dashboard 8080:443
```

브라우저에서 아래 사이트에 접속합니다.

```text
https://localhost:8080
```

## Clean Up

환경을 정리하기 위해서 다음의 명령어를 사용할 수 있습니다.

```bash
# Remove VirtualBox cluster
vagrant destory -f
```
