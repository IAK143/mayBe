import pytest
from benchmarks.runner import BenchmarkRunner, AblationTester

def test_benchmark_runner():
    runner = BenchmarkRunner("bmk_001", "synthetic_gold_dataset")

    def dummy_task():
        return sum(range(1000))

    res = runner.run_eval("test_task", dummy_task)
    assert res["benchmark_id"] == "bmk_001"
    assert "runtime_seconds" in res
    assert "metrics" in res

def test_ablation_tester():
    results = AblationTester.run_ablations(["doc1", "doc2"])
    assert "lexical_only" in results
    assert "full_pipeline_with_state_inference" in results
    assert results["full_pipeline_with_state_inference"]["mrr"] > results["lexical_only"]["mrr"]
