import asyncio
from langsmith import aevaluate
from eval.target import target,root_cause_target
from typing import Dict,Any
from dotenv import load_dotenv


def field_match(run:Any, example:Any) -> Dict[str,Any]:
    predicted = run.outputs or {}
    expected = (example.outputs or {}).get("expected_output", example.outputs or {})
    fields = ["service_name", "error_type", "occurrence_count", "endpoint"]
    correct = sum(1 for f in fields if predicted.get(f) == expected.get(f))
    return {"key": "field_accuracy", "score": correct / len(fields), "comment": f"predicted={predicted}, expected={expected}"}

def rag_grounding_correctness(run:Any, example:Any) -> Dict[str,Any]:
    predicted_grounded = (run.outputs or {}).get("rag_grounded")
    expected_grounded = (example.outputs or {}).get("expected_output", {}).get("should_ground")
    return {
        "key": "rag_grounding_correctness",
        "score": 1 if predicted_grounded == expected_grounded else 0,
        "comment": f"predicted={predicted_grounded}, expected={expected_grounded}",
    }


async def main():

    root_cause_results = await aevaluate(
        root_cause_target,
        data="sentinel_root_cause_rag_golden",  # the dataset name you upload the .jsonl as
        evaluators=[rag_grounding_correctness],
        experiment_prefix="root-cause-rag",
    )
    print(root_cause_results)
    # results = await aevaluate(
    #     target,
    #     data="log_analyzer_golden",
    #     evaluators=[field_match],
    #     experiment_prefix="log-analyzer",
    # )
    # print(results)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())