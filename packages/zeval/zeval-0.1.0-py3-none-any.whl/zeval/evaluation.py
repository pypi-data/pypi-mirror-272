from datasets import Dataset
from dataclasses import asdict, dataclass

def evaluate(dataset: Dataset, evaluator_names: list[str], model_config: dict):
    results = []
    for evaluator in evaluator_names:
        evaluator = evaluator()
        score, reasoning, responses = evaluator.score(dataset, model_config)
        result = Result(score, reasoning, responses)
    return result

@dataclass
class Result:
    score: float
    reasoning: str
    responses: list[dict]