# runt-hq

Reference implementation of the API server to manage creating runts for
notebooks

## Testing

This project uses pytest for testing with coverage reporting. The testing setup
follows the guidelines in `docs/testing.md`.

### Setup

Install development dependencies:

```bash
uv sync
```

The development dependencies are automatically installed when using
`uv run pytest`.

### Running Tests

Run tests using `uv run pytest`:

```bash
# Run all tests
uv run pytest tests/ -v

# Run all tests
uv run pytest tests/ -v

# Run tests with coverage report
uv run pytest tests/ --cov=src/runt_hq --cov-report=term-missing --cov-report=html
```

### Test Structure

- `tests/test_*.py` - Unit tests using TestClient
- `tests/conftest.py` - Global pytest fixtures
- `docs/testing.md` - Detailed testing philosophy and guidelines

### Coverage

Coverage reports are generated automatically when running tests. Reports are
available in:

- Terminal output (missing lines)
- `htmlcov/` directory (HTML report)
- `coverage.xml` (XML report for CI/CD)
