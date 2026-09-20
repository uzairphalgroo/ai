"""
Unit tests for Dataset Loader & 100+ Adversarial Vector Suite.
"""

from core.datasets.loader import DatasetLoader
from core.models import AttackCategory, SeverityLevel


def test_dataset_size_and_categories():
    vectors = DatasetLoader.load_all_vectors()
    assert len(vectors) >= 100, f"Expected at least 100 benchmark vectors, got {len(vectors)}"

    stats = DatasetLoader.get_summary_stats()
    assert stats["total_vectors"] >= 100

    # Ensure all 5 categories have test cases
    for cat in AttackCategory:
        count = stats.get(cat.value, 0)
        assert count >= 10, f"Category {cat.value} has fewer than 10 vectors (count={count})"


def test_vector_schema_integrity():
    vectors = DatasetLoader.load_all_vectors()
    for v in vectors:
        assert v.id.startswith("VEC-")
        assert len(v.prompt) > 5
        assert len(v.expected_behavior) > 5
        assert isinstance(v.category, AttackCategory)
        assert isinstance(v.severity, SeverityLevel)


def test_vector_filtering():
    pii_only = DatasetLoader.filter_vectors(categories=[AttackCategory.PII_EXTRACTION])
    assert len(pii_only) > 0
    assert all(v.category == AttackCategory.PII_EXTRACTION for v in pii_only)

    limited = DatasetLoader.filter_vectors(limit=5)
    assert len(limited) == 5
