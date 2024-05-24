import mlflow
import openai
import os
import pandas as pd
from getpass import getpass

if __name__ == "__main__":
    data = pd.DataFrame(
        {
            "questions": [
                "What is MLflow?",
                "What is Databricks?",
                "How to serve a model on Databricks?",
                "How to enable MLflow Autologging for my workspace by default?",
            ],
            "retrieved_context": [
                [
                    "mlflow/index.html",
                    "mlflow/quick-start.html",
                ],
                [
                    "introduction/index.html",
                    "getting-started/overview.html",
                ],
                [
                    "machine-learning/model-serving/index.html",
                    "machine-learning/model-serving/model-serving-intro.html",
                ],
                [],
            ],
            "ground_truth_context": [
                ["mlflow/index.html"],
                ["introduction/index.html"],
                [
                    "machine-learning/model-serving/index.html",
                    "machine-learning/model-serving/llm-optimized-model-serving.html",
                ],
                ["mlflow/databricks-autologging.html"],
            ],
        }
    )

    mlflow.set_tracking_uri("http://localhost:5001")
    mlflow.set_experiment("experiment_test")
    with mlflow.start_run() as run:
        evaluate_results = mlflow.evaluate(
            data=data,
            model_type="retriever",
            targets="ground_truth_context",
            predictions="retrieved_context",
            evaluators="default",
            evaluator_config={"retriever_k": 1}
        )
