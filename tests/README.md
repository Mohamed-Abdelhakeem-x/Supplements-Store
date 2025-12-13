# Software Testing Strategy: Unit vs Integration Tests

## Unit Tests
**Location**: `tests/unit/test_services.py`
**Goal**: Test isolated components (functions/methods) without external dependencies.
**Technique**: Mocking.
**Key Features**:
- **Isolation**: Uses `unittest.mock` to simulate Database (`db.session`) and Bcrypt behavior.
- **Speed**: Very fast because they do not interact with a real database or file system.
- **Scope**: Tests business logic in `models.py` (e.g., `check_password`, `calculate_total`, `validate_content`) to ensure the logic *inside* the function is correct.
- **Fault Isolation**: If a test fails, you know the bug is in that specific function, not in said dependencies.

## Integration Tests
**Location**: `tests/integration/test_flows.py`
**Goal**: Test how different components work *together*.
**Technique**: Real (in-memory) Dependencies.
**Key Features**:
- **Real Environment**: Uses a real SQLite database (in-memory) and the actual Flask application context via `pytest` fixtures.
- **Scope**: Tests entire user flows (e.g., Register -> Login -> Add to Cart). It verifies that the Route calls the Model, the Model talks to the DB, and the response is correct.
- **Validation**: Ensures that the pieces (Routes, Models, Database) communicate correctly, catching issues like specific SQL errors (e.g., integrity errors) or template rendering bugs that unit tests miss.
