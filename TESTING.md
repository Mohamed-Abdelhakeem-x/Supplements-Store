# Testing Strategy and Guide

## 1. Test Coverage and E2E Tests

**Is 74.4% coverage good for E2E tests?**
**Yes, this is excellent.**

*   **E2E (End-to-End) Tests** focus on the "Happy Path" and critical user journeys (e.g., "Can a user sign up, buy a product, and pay?"). They are expensive to run and difficult to maintain.
*   **Coverage Expectation**: E2E tests typically cover 50-70% of the code because they rarely hit edge cases, error handlers, or defensive coding logic (e.g., specific database connection failures) which are better tested by Unit Tests.
*   **Goal**: The goal of E2E is **Confidence** that the system works together, not line-by-line **Coverage**.

## 2. Testing folder Structure

Your `tests/` directory is organized into layers of the **Testing Pyramid**:

### `tests/unit/` (The Base)
*   **What it does:** Tests individual functions, classes, or models in **complete isolation**.
*   **Mocking:** Heavy use of mocks. For example, testing `User.check_password` without a real database.
*   **Speed:** Extremely fast (milliseconds).
*   **Purpose:** Verify *logic* correctness.

### `tests/integration/` (The Middle)
*   **What it does:** Tests how different parts of the system work **together**.
*   **Scope:** API Routes + Database, or Forms + Views.
*   **Realism:** Uses a real (test) database.
*   **Purpose:** Verify *component wiring* and data flow.

### `tests/e2e/` (The Top)
*   **What it does:** Tests the application from the **User's Perspective**.
*   **Tools:** Uses Selenium/Browser to click buttons and type in input fields against a running server.
*   **Realism:** Maximum. It simulates a real user on Chrome.
*   **Purpose:** Verify *user journeys* and system integrity.

## 3. How to Test the Whole Project

To run **ALL** tests (Unit + Integration + E2E) and get a combined coverage report:

### Run All Tests
```bash
python -m pytest
```

### Run All Tests with Detailed Coverage Report
```bash
python -m pytest --cov=Prime_Supplements --cov-report=term-missing
```

### Run Specific Layers
*   **Unit Only:** `pytest tests/unit`
*   **Integration Only:** `pytest tests/integration`
*   **E2E Only:** `pytest tests/e2e`
