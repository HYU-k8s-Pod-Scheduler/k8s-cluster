from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from collections import deque
import pymetis

# FastAPI 인스턴스 생성
app = FastAPI()

scheduling_info = {}


# 입력 데이터 모델 정의
class PartitionRequest(BaseModel):
    node_list: List[str] = Field(
        description="노드명 리스트", example=["node-1", "node-2"]
    )
    pod_list: List[str] = Field(
        description="파드명 리스트",
        example=["pod-1", "pod-2", "pod-3", "pod-4", "pod-5"],
    )
    vweights: List[int] = Field(
        description="파드 가중치 리스트 / 파드명 순서와 동일함",
        example=[512, 128, 128, 128, 128],
    )
    adjacency_list: List[List[int]] = Field(
        description="인접 리스트 / 파드명 순서와 동일함",
        example=[[1, 2], [0, 2, 3], [0, 1, 3], [1, 2, 4], [3]],
    )
    eweights: List[List[int]] = Field(
        description="간선 가중치 리스트 / 파드명 순서와 동일함",
        example=[[1, 2], [1, 2, 3], [1, 2, 3], [1, 2, 1], [1]],
    )


class SchedulingRequest(BaseModel):
    pod_name: str = Field(description="파드명", example="pod-1")


# 그래프 파티셔닝 API 엔드포인트
@app.post("/partition")
async def partition_graph(data: PartitionRequest):
    global scheduling_info
    try:
        # xadj, adjncy, eweights 계산
        xadj = [0]
        adjncy = []
        eweights = []
        num_parts = len(data.node_list)

        for i, adj in enumerate(data.adjacency_list):
            xadj.append(xadj[-1] + len(adj))
            adjncy.extend(adj)
            eweights.extend(data.eweights[i])

        # PyMetis로 그래프 분할 수행
        cuts, parts = pymetis.part_graph(
            num_parts,
            xadj=xadj,
            adjncy=adjncy,
            eweights=eweights,
            vweights=data.vweights,
        )

        scheduling_info = {}

        for pod in data.pod_list:
            scheduling_info[pod] = deque()

        for i, part in enumerate(parts):
            scheduling_info[data.pod_list[i]].append(data.node_list[part])

        # 결과 반환
        return {
            "cuts": cuts,  # 자른 간선의 수
            "parts": parts,  # 각 노드의 파티션 할당 결과
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scheduling")
async def get_scheduling_info(data: SchedulingRequest):
    global scheduling_info

    if data.pod_name not in scheduling_info:
        raise HTTPException(status_code=500, detail="Pod not found")

    if len(scheduling_info[data.pod_name]) == 0:
        raise HTTPException(status_code=500, detail="Node not found")

    return scheduling_info[data.pod_name].popleft()


# 테스트 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
