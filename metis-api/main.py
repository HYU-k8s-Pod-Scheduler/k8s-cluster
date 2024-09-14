from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pymetis

# FastAPI 인스턴스 생성
app = FastAPI()


# 입력 데이터 모델 정의
class GraphData(BaseModel):
    adjacency_list: List[List[int]]  # 인접 리스트
    num_parts: int  # 파티션 수
    eweights: List[List[int]]  # 간선 가중치


# 그래프 파티셔닝 API 엔드포인트
@app.post("/partition")
async def partition_graph(graph_data: GraphData):
    try:
        # xadj, adjncy, eweights 계산
        xadj = [0]
        adjncy = []
        eweights = []

        for i, adj in enumerate(graph_data.adjacency_list):
            xadj.append(xadj[-1] + len(adj))
            adjncy.extend(adj)
            eweights.extend(graph_data.eweights[i])

        # PyMetis로 그래프 분할 수행
        cuts, parts = pymetis.part_graph(
            graph_data.num_parts, xadj=xadj, adjncy=adjncy, eweights=eweights
        )

        # 결과 반환
        return {
            "cuts": cuts,  # 자른 간선의 수
            "parts": parts,  # 각 노드의 파티션 할당 결과
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 테스트 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
