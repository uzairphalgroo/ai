"""
Adversarial Dataset Loader & Manager for Hallucikiller.
Loads, validates, and filters 100+ benchmark attack vectors.
"""

import json
import os
from typing import List, Optional, Dict
from core.models import TestVector, AttackCategory, SeverityLevel


DATASETS_DIR = os.path.dirname(os.path.abspath(__file__))


class DatasetLoader:
    """Manages loading and filtering of adversarial test vectors."""

    _cached_vectors: Optional[List[TestVector]] = None

    @classmethod
    def load_all_vectors(cls, force_reload: bool = False) -> List[TestVector]:
        if cls._cached_vectors is not None and not force_reload:
            return cls._cached_vectors

        vectors: List[TestVector] = []
        known_files = [
            "vectors_pii.json",
            "vectors_injection.json",
            "vectors_hallucination.json",
            "vectors_roleplay.json",
            "vectors_override.json"
        ]
        other_files = sorted([f for f in os.listdir(DATASETS_DIR) if f.endswith(".json") and f not in known_files])
        json_files = [f for f in known_files if os.path.exists(os.path.join(DATASETS_DIR, f))] + other_files

        for filename in json_files:
            filepath = os.path.join(DATASETS_DIR, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        raw_data = json.load(f)
                        if isinstance(raw_data, list):
                            for item in raw_data:
                                try:
                                    vector = TestVector(**item)
                                    vectors.append(vector)
                                except Exception as e:
                                    print(f"Warning: Failed to load vector {item.get('id')}: {e}")
                except Exception as e:
                    print(f"Warning: Failed to parse file {filename}: {e}")

        cls._cached_vectors = vectors
        return vectors

    @classmethod
    def filter_vectors(
        cls,
        categories: Optional[List[AttackCategory]] = None,
        severities: Optional[List[SeverityLevel]] = None,
        limit: Optional[int] = None
    ) -> List[TestVector]:
        all_vecs = cls.load_all_vectors()
        filtered = all_vecs

        if categories:
            filtered = [v for v in filtered if v.category in categories]

        if severities:
            filtered = [v for v in filtered if v.severity in severities]

        if limit is not None and limit > 0:
            filtered = filtered[:limit]

        return filtered

    @classmethod
    def get_summary_stats(cls) -> Dict[str, int]:
        all_vecs = cls.load_all_vectors()
        stats: Dict[str, int] = {
            "total_vectors": len(all_vecs)
        }
        for cat in AttackCategory:
            stats[cat.value] = sum(1 for v in all_vecs if v.category == cat)
        return stats
