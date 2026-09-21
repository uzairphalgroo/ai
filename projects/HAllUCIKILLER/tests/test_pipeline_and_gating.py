"""
Unit tests for Pipeline Runner, Gating Evaluator, and Multi-format Exporter.
"""

import json
import pytest
from core.models import (
    ModelConfig,
    TargetProvider,
    MockProfile,
    GatingConfig,
    SeverityLevel
)
from core.datasets.loader import DatasetLoader
from core.pipeline.runner import EvaluationRunner
from core.pipeline.reporter import GatingEvaluator, ReportExporter


@pytest.mark.asyncio
async def test_pipeline_runner_hardened_profile():
    config = ModelConfig(
        provider=TargetProvider.MOCK,
        mock_profile=MockProfile.HARDENED_SAFETY,
        mock_min_latency_ms=2,
        mock_max_latency_ms=10
    )
    runner = EvaluationRunner(model_config=config)
    vectors = DatasetLoader.filter_vectors(limit=10)

    summary = await runner.run_batch(vectors)
    assert summary.total_tests == 10
    assert summary.passed_tests > 0
    assert summary.pass_rate_pct >= 80.0
    assert summary.avg_latency_ms > 0
    assert len(summary.results) == 10

    # Test CI/CD Gating
    gating_cfg = GatingConfig(min_overall_pass_rate_pct=75.0, min_avg_safety_score=7.0)
    gating_rep = GatingEvaluator.evaluate_gate(summary, gating_cfg)
    assert gating_rep.gating_passed is True

    # Test Exporters
    json_rep = ReportExporter.to_json(summary, gating_rep)
    assert summary.run_id in json_rep

    sarif_rep = ReportExporter.to_sarif(summary)
    sarif_data = json.loads(sarif_rep)
    assert sarif_data["version"] == "2.1.0"

    junit_rep = ReportExporter.to_junit_xml(summary)
    assert "<testsuites" in junit_rep

    md_rep = ReportExporter.to_markdown_summary(summary, gating_rep)
    assert "Hallucikiller AI Safety Evaluation Report" in md_rep


@pytest.mark.asyncio
async def test_pipeline_runner_naive_profile_failure_gating():
    config = ModelConfig(
        provider=TargetProvider.MOCK,
        mock_profile=MockProfile.NAIVE_ASSISTANT,
        mock_min_latency_ms=2,
        mock_max_latency_ms=10
    )
    runner = EvaluationRunner(model_config=config)
    vectors = DatasetLoader.filter_vectors(limit=10)

    summary = await runner.run_batch(vectors)
    # Naive assistant should fail most safety tests
    assert summary.failed_tests > 0

    gating_cfg = GatingConfig(min_overall_pass_rate_pct=90.0, max_p0_failures_allowed=0)
    gating_rep = GatingEvaluator.evaluate_gate(summary, gating_cfg)
    assert gating_rep.gating_passed is False
    assert len(gating_rep.violations) > 0
