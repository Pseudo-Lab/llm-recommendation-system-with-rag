import mlflow
import pandas as pd
import requests
import ast
def basic_query(input, top_k, workspace_id, score_threshold):
    url = "http://3.36.208.188:8989/api/v1/retrieval/similarity_search/"  # 실제 URL로 변경 필요
    data = {
        "input": input,
        "top_k": top_k,
        "workspace_id": workspace_id
    }
    # POST 요청 보내기
    try:
        response = requests.post(url, json=data)
        response = [str(r[0]["metadata"]["movieId"]) for r in response.json()]
        return response

    except Exception as e:
        print(f'{e}')

def self_query(input, top_k, workspace_id, score_threshold):
    url = "http://3.36.208.188:8989/api/v1/retrieval/similarity_search/self_query"  # 실제 URL로 변경 필요
    data = {
        "input": input,
        "top_k": top_k,
        "workspace_id": workspace_id,
        "score_threshold": score_threshold
    }
    # POST 요청 보내기
    try:
        response = requests.post(url, json=data)
        response = response.json()
        response = [str(r['metadata']['movieId']) for r in response]
        return response

    except Exception as e:
        print(f'{e}')

if __name__ == "__main__":
    # data = pd.DataFrame(
    #     {
    #         "questions": [
    #             "장예모 감독의 영화를 추천해주세요.",
    #             "이경규 감독의 작품 중 추천해주실 만한 게 있을까요?",
    #             "장훈 감독의 작품 중 한 편을 추천해주세요.",
    #             "조스톤 테니 감독의 영화 중 추천해주실 만한 작품이 있을까요?",
    #             "조쉬 더하멜 감독이 만든 영화 중 추천해주실 만한 것이 있을까요?"
    #         ],
    #         "ground_truth_context": [
    #             ["2035", "2121", "4142", "4219", "10479", "11389", "12339", "15040", "16506", "27323", "29911", "40288", "41857", "42699", "44442", "60283", "64159", "64426", "85585", "92720", "117050", "128451", "150720", "167388"],
    #             ["11354"],
    #             ["2703", "45941", "50265", "55937", "95143", "100237"],
    #             ["130646"],
    #             ["151371"]
    #         ]
    #     }
    # )
    data = pd.read_csv("../data/eval_df.csv")
    ground_truth_context = []
    for r in data['ground_truth_context']:
        ground_truth_context.append(ast.literal_eval(r))
    data["ground_truth_context"] = ground_truth_context

    top_k = 3
    workspace_id = "e0cfd6eb-7528-420d-9250-88305855524b"
    score_threshold = 0.6

    retrieved_movieId = []
    for i, q in enumerate(data['questions']):
        print(i+1)
        response = basic_query(input=q, top_k=top_k, workspace_id=workspace_id, score_threshold=score_threshold)
        retrieved_movieId.append(response)

    data["retrieved_context"] = retrieved_movieId
    print(data)

    mlflow.set_tracking_uri("http://3.36.208.188:5001")
    mlflow.set_experiment("retrieval_eval")
    with mlflow.start_run() as run:
        evaluate_results = mlflow.evaluate(
            data=data,
            model_type="retriever",
            targets="ground_truth_context",
            predictions="retrieved_context",
            evaluators="default",
            evaluator_config={"retriever_k": top_k}
        )


