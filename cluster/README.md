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
