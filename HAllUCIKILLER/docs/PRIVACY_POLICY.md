# PRIVACY POLICY // HALLUCIKILLER DEFENSE MATRIX

**Effective Date:** September 20, 2026  
**Architecture:** Zero-Telemetry, Ephemeral In-Memory Execution  

---

## 1. Core Privacy Philosophy
HALLUCIKILLER adheres to strict **Data Sovereignty by Design**. We believe that LLM security benchmarks, vulnerability telemetry, and prompt injection payloads must remain private to your local or self-hosted deployment.

## 2. Information We Do NOT Collect
- **No Secret Telemetry:** HALLUCIKILLER does not transmit any user prompts, model responses, canary tokens, or benchmark verdicts to external telemetry servers.
- **No Private Key Retention:** All API keys (`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, etc.) supplied via environment variables or the UI header are stored ephemerally in session memory or client browser memory. Keys are never logged, persisted in public files, or exfiltrated.
- **No Tracking or Cookies:** The web application does not use tracking cookies, analytics trackers, or third-party fingerprinting scripts.

## 3. Data Processing & Flow
- **Local In-Memory Execution:** Test vector evaluation results and SARIF artifacts reside in local process memory (`_EVAL_RUN_CACHE`) and are cleared upon server restart.
- **Direct Target Inferences:** When you trigger a benchmark run against a target endpoint (e.g. OpenRouter or local Ollama), HTTPS requests are routed directly to the specified endpoint with your authorization headers.

## 4. Synthetic Adversarial Datasets
All test vector datasets included in `core/datasets/` contain purely **synthetic canary tokens**, mock PII, and synthetic secret patterns. No real-world customer PII or proprietary credentials are included.

## 5. Security of Exported Artifacts
SARIF (`.sarif`), JUnit XML (`.xml`), and JSON reports downloaded from the platform contain diagnostic vulnerability traces. Users are advised to store these artifacts within secure, access-controlled CI/CD artifact vaults.
