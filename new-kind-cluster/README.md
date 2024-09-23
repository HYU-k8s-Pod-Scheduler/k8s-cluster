# New Kind Cluster

본 문서는 METIS 스케듈러를 테스트하기 위한 새로운 Kind 클러스터를 생성하는 방법을 설명합니다.

## Prerequisites

- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

## 과정

1. 새로운 Kind 클러스터를 생성합니다.

   ```bash
   sh ./1.\ create-cluster.sh
   ```

2. 생성된 클러스터에 METIS 스케듈러를 설치합니다.

   ```bash
   sh ./2.\ create-scheduler.sh
   ```

3. METIS API를 설치합니다.

   ```bash
   sh ./3.\ create-metis-api.sh
   ```

4. Pod를 생성하여 METIS 스케듈러가 동작하는지 확인합니다.

   ```bash
   sh ./4.\ create-pod.sh
   ```

5. 클러스터를 삭제합니다.

   ```bash
   sh ./5.\ clean-up.sh
   ```
