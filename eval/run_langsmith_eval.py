import asyncio
from langsmith import aevaluate
from eval.target import target
from typing import Dict,Any
from dotenv import load_dotenv


def field_match(run:Any, example:Any) -> Dict[str,Any]:
    predicted = run.outputs or {}
    expected = (example.outputs or {}).get("expected_output", example.outputs or {})
    fields = ["service_name", "error_type", "occurrence_count", "endpoint"]
    correct = sum(1 for f in fields if predicted.get(f) == expected.get(f))
    return {"key": "field_accuracy", "score": correct / len(fields), "comment": f"predicted={predicted}, expected={expected}"}


async def main():
    results = await aevaluate(
        target,
        data="log_analyzer_golden",
        evaluators=[field_match],
        experiment_prefix="log-analyzer",
    )
    print(results)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())