import asyncio
import aiohttp
import mlflow
import pandas as pd
import ast


async def fetch(session, input, top_k, workspace_id, score_threshold, search_type):
    host = "http://127.0.0.1:8989"
    if search_type == "dense":
        url = "/api/v1/retrieval/dense_search/"
    elif search_type == "sparse":
        url = "/api/v1/retrieval/sparse_search/"
    elif search_type == "ensemble":
        url = "/api/v1/retrieval/ensemble_search/"
    elif search_type == "self":
        url = "/api/v1/retrieval/self_query/"

    data = {
        "input": input,
        "top_k": top_k,
        "workspace_id": workspace_id,
        "score_threshold": score_threshold
    }
    for attempt in range(5):
        try:
            async with session.post(host + url, json=data) as response:
                docs = await response.json()
                if isinstance(docs, list):
                    if len(docs) > 0:
                        response = [str(d["metadata"]["movieId"]) for d in docs]
                        print(response)
                        return response
                    else:
                        return []
        except aiohttp.ClientOSError as e:
            if attempt < 5-1:
                print(f"Request failed ({e}), retrying...")
                await asyncio.sleep(1)  # 1초 대기 후 재시도
            else:
                raise

async def main(data, top_k, workspace_id, score_threshold, search_type):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, q in enumerate(data['questions']):
        # 비동기 작업
        #     task = asyncio.create_task(fetch(session, q, top_k, workspace_id, score_threshold, search_type))
        #     tasks.append(task)
        # response = await asyncio.gather(*tasks)
        # return response

        # 동기 작업(OpenAI는 1분에 한정된 토큰 제한이 있어 동기로 테스트 진행)
            print(f'{i}')
            result = await fetch(session, q, top_k, workspace_id, score_threshold, search_type)
            tasks.append(result)
            await asyncio.sleep(1)
        return tasks


if __name__ == "__main__":
    data = pd.read_csv("../ops/data/test_300.csv")
    data = data[['questions', 'ground_truth_context']]
    ground_truth_context = []
    for r in data['ground_truth_context']:
        ground_truth_context.append(ast.literal_eval(r))
    data["ground_truth_context"] = ground_truth_context

    # filtered_df = data[data['ground_truth_context'].apply(lambda x: len(x) <= 5)]
    # new_df = filtered_df.sample(n=300, random_state=2024)
    # new_df.to_csv("../ops/data/test_300.csv")


    top_k = 5
    # workspace_id = "f8585417-67fc-420f-b08c-c1bfc7d82a9b" # openai
    workspace_id = "2592f14c-2f51-40fd-9ec2-89ed2742a0cc" # m3
    score_threshold = 0.6
    search_type = "self"

    retrieved_movieId = asyncio.run(main(data, top_k, workspace_id, score_threshold, search_type))
    data["retrieved_context"] = retrieved_movieId


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


