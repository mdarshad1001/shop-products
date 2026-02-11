import os
import asyncio
import json
import requests
from ragas import evaluate, SingleTurnSample, EvaluationDataset
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.run_config import RunConfig
from langchain_openai import ChatOpenAI

ak = os.getenv("OPENAI_API_KEY")
oai_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=ak)

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def print_eval_res(eval_result):
    scores = eval_result.scores
    eval_str = ' | Q | '
    for k in scores[0].keys():
        eval_str = eval_str + str(k) + ' | '
    print(eval_str)
    for i, score in enumerate(scores):
        eval_str = ' | ' + str(i + 1) + ' | '
        for k in score.keys():
            eval_str = eval_str + str(score[k]) + ' | '
        print(eval_str)
    res = eval_result.to_pandas()
    means = res.mean(numeric_only=True).to_dict()
    print("\n📈 Averages:")
    for k, v in means.items():
        print(f"- {k}: {v:.3f}")
        

async def evaluate_rag_system(test_path="../seed/qna_test.json"):
    test_data = load_jsonl(test_path)
    results = []

    for item in test_data:
        question = item["question"]
        reference_answer = item["answer"]
        url = 'http://localhost:8000/search'
        myobj = {'query': question}
        res = requests.post(url, json=myobj).json()
        answer, contexts = res['answer'], res['contexts']

    #TODO

if __name__ == "__main__":
    asyncio.run(evaluate_rag_system())