# Code Coverage Analysis

## Commands
To measure code coverage including branch coverage, use the following commands:

### Run Coverage
```bash
coverage run --branch --source=Prime_Supplements -m pytest tests/
```
- `--branch`: Measurement of branch coverage (if/else paths).
- `--source=Prime_Supplements`: Restricts coverage to the application source code (ignoring tests and venv).

### View Text Report
```bash
coverage report -m
```
- `-m`: Shows the line numbers of missing statements.

### Generate HTML Report
```bash
coverage html
```
- Generates an interactive report in `htmlcov/index.html`. Open this file in a browser to see highlighted code.

## Coverage Criteria & Challenges

### Achievement
- **Service Layer**: High coverage achieved via Unit tests (`tests/unit`) which target specific logic methods.
- **Routes & Flows**: Good coverage achieved via Integration tests (`tests/integration`) which simulate real user traffic.

### Hardest Parts to Cover
1. **Error Handling**: `try/except` blocks for database errors are hard to trigger deterministically without complex mocking in integration tests.
2. **Edge Case Branches**: `if` statements checking for rare data invalidity (e.g., malformed sessions) are often missed by standard "happy path" integration tests.
3. **Template Logic**: Logic inside Jinja2 templates (`{% if ... %}`) is not measured by `coverage.py`, requiring careful manual review or UI testing to verify.
