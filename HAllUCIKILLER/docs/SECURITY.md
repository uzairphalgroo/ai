# SECURITY POLICY & THREAT MODEL // HALLUCIKILLER

## 1. Security Architecture & Threat Model
HALLUCIKILLER operates as a Level 4 defensive evaluation harness for Large Language Models. Its security posture consists of:

1. **Dual Evaluation Pipeline:**
   - **Deterministic Scanner:** Zero-inference regex laser scanner checking for SSN, credit cards, JWT tokens, AWS/OpenAI keys, and injected canary strings.
   - **Neural Safety Judge:** Structured semantic evaluator assessing policy adherence, toxicity, and hallucination bounds.
2. **Deterministic Canary Verification:**
   - Synthetic UUID canary tokens injected into prompts. If leaked in model output, the scanner immediately flags a critical security breach without relying on fuzzy heuristics.
3. **Hardened API Endpoints:**
   - GZip payload compression with buffer boundary limits.
   - HTTP Security Headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`).
   - XSS sanitization (`escapeHtml`) on all rendered client-side strings.

## 2. Supported Versions
Security updates are actively applied to the latest `main` branch.

| Version | Supported |
|---|---|
| 2027.1.x | :white_check_mark: Yes |
| < 2027.0.0 | :x: No |

## 3. Reporting a Vulnerability
If you discover a security vulnerability within the HALLUCIKILLER codebase (e.g. regex bypass, injection vulnerability, or server crash vector):
1. **Do not disclose publicly.**
2. Open a confidential GitHub Security Advisory on the repository: https://github.com/uzairphalgroo/ai/security/advisories
3. Include detailed reproduction steps, target payload, and expected vs observed behavior.
4. Maintainers will review and respond within 48 hours.
