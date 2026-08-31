# AI Career Engine - Test Suite Architecture & Coverage

This directory contains the automated test suite for the AI Career Engine platform.

---

## 📁 Directory Layout & Test Suites

- **`test_agents.py`**: Unit tests verifying individual agent lifecycle execution, context validation, and error safety.
- **`test_llm.py`**: Integration tests verifying `LLMProvider` REST dispatch (Gemini, OpenAI, NVIDIA Nemotron), fallback behavior, and agent narrative explanations.
- **`test_scenarios.py`**: Scenario evaluation tests (S001 - S007) matching real-world candidate archetypes and SRS requirements.
- **`test_regression_edge_cases.py`**: Regression edge-case tests covering protected career gap rules (`protected: true` vs `protected: false` vs missing flag), proficiency score clamping (`0.0 - 1.0`), duplicate skills, and ranking invariants.
- **`test_data_contracts.py`**: Data contract validation tests verifying candidate IDs, target role IDs, proficiency ranges, and JSON data schemas.
- **`test_integration_invariants.py`**: Full matrix integration tests running every candidate against every target role to assert state structure, readiness score bounds `[0, 100]`, and opportunity ranking order invariants.

---

## 🚀 Running the Tests

### Run All Unit & Integration Tests
```bash
python -m unittest discover -s tests
```

### Run Specific Test Suite
```bash
python -m unittest tests/test_regression_edge_cases.py
python -m unittest tests/test_data_contracts.py
python -m unittest tests/test_integration_invariants.py
```

### Run Benchmark Evaluation
```bash
python evaluate.py
```
