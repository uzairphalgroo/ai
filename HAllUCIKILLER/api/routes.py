"""
FastAPI Routes for Hallucikiller AI Safety Pipeline.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field

from core.models import (
    TestVector,
    ModelConfig,
    EvalResult,
    BatchEvaluationSummary,
    GatingConfig,
    GatingReport,
    AttackCategory,
    SeverityLevel,
    HeuristicResult
)
from core.datasets.loader import DatasetLoader
from core.pipeline.runner import EvaluationRunner
from core.pipeline.reporter import GatingEvaluator, ReportExporter
from core.evaluators.heuristic_scanner import HeuristicScanner

router = APIRouter(prefix="/api", tags=["Hallucikiller Evaluation API"])

# In-memory run store
_EVAL_RUN_CACHE: Dict[str, BatchEvaluationSummary] = {}
_SCANNER = HeuristicScanner()


class QuickScanRequest(BaseModel):
    response_text: str
    canary_tokens: List[str] = Field(default_factory=list)
    forbidden_patterns: List[str] = Field(default_factory=list)


class RunEvaluationRequest(BaseModel):
    target_config: ModelConfig
    categories: Optional[List[AttackCategory]] = None
    severities: Optional[List[SeverityLevel]] = None
    limit: Optional[int] = None
    gating_config: Optional[GatingConfig] = None


class ExportRequest(BaseModel):
    run_id: str
    export_format: str = Field("json", description="json | sarif | junit | markdown")
    gating_config: Optional[GatingConfig] = None


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Hallucikiller AI Safety Pipeline",
        "version": "2027.1.0",
        "total_vectors_loaded": len(DatasetLoader.load_all_vectors())
    }


@router.get("/vectors", response_model=List[TestVector])
async def list_vectors(
    category: Optional[AttackCategory] = Query(None, description="Filter by attack category"),
    severity: Optional[SeverityLevel] = Query(None, description="Filter by severity"),
    limit: Optional[int] = Query(None, description="Limit count of returned vectors")
):
    categories = [category] if category else None
    severities = [severity] if severity else None
    return DatasetLoader.filter_vectors(categories=categories, severities=severities, limit=limit)


@router.get("/vectors/stats")
async def vector_statistics():
    return DatasetLoader.get_summary_stats()


@router.post("/vectors/add", response_model=TestVector)
async def add_custom_vector(vector: TestVector):
    all_vecs = DatasetLoader.load_all_vectors()
    all_vecs.append(vector)
    return vector


@router.post("/eval/scan-text", response_model=HeuristicResult)
async def scan_text(payload: QuickScanRequest):
    temp_vec = TestVector(
        id="VEC-ADHOC",
        category=AttackCategory.PII_EXTRACTION,
        title="Ad-hoc Heuristic Scan",
        prompt="",
        expected_behavior="",
        canary_tokens=payload.canary_tokens,
        forbidden_patterns=payload.forbidden_patterns
    )
    return _SCANNER.scan(payload.response_text, temp_vec)


@router.post("/eval/run", response_model=Dict[str, Any])
async def run_evaluation(payload: RunEvaluationRequest):
    vectors = DatasetLoader.filter_vectors(
        categories=payload.categories,
        severities=payload.severities,
        limit=payload.limit
    )

    if not vectors:
        raise HTTPException(status_code=400, detail="No matching test vectors found.")

    runner = EvaluationRunner(model_config=payload.target_config)
    summary = await runner.run_batch(vectors)
    _EVAL_RUN_CACHE[summary.run_id] = summary

    # Check Gating
    gating_cfg = payload.gating_config or GatingConfig()
    gating_report = GatingEvaluator.evaluate_gate(summary, gating_cfg)

    return {
        "summary": summary,
        "gating_report": gating_report
    }


@router.get("/runs/{run_id}", response_model=BatchEvaluationSummary)
async def get_run_results(run_id: str):
    if run_id not in _EVAL_RUN_CACHE:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found.")
    return _EVAL_RUN_CACHE[run_id]


@router.post("/eval/export")
async def export_evaluation_report(payload: ExportRequest):
    if payload.run_id not in _EVAL_RUN_CACHE:
        raise HTTPException(status_code=404, detail=f"Run {payload.run_id} not found.")

    summary = _EVAL_RUN_CACHE[payload.run_id]
    gating_cfg = payload.gating_config or GatingConfig()
    gating_report = GatingEvaluator.evaluate_gate(summary, gating_cfg)

    fmt = payload.export_format.lower()
    if fmt == "json":
        return {"format": "json", "content": ReportExporter.to_json(summary, gating_report)}
    elif fmt == "sarif":
        return {"format": "sarif", "content": ReportExporter.to_sarif(summary)}
    elif fmt == "junit" or fmt == "xml":
        return {"format": "junit_xml", "content": ReportExporter.to_junit_xml(summary)}
    elif fmt == "markdown" or fmt == "md":
        return {"format": "markdown", "content": ReportExporter.to_markdown_summary(summary, gating_report)}
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {payload.export_format}")
