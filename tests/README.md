# Rising Topics Test Suite

This directory contains all test files for the Rising Topics project.

## Test Organization

### Python Tests
- `test_*.py` - Individual test modules for different components
- `run_tests.py` - Test runner that executes all tests
- `__init__.py` - Makes this a Python package

### Test Categories

#### Data Pipeline Tests
- `test_pipeline.py` - Main pipeline functionality
- `test_scoring.py` - Scoring algorithm tests
- `test_deduplication.py` - Deduplication logic tests
- `test_filtering.py` - Data filtering tests
- `test_archive_system.py` - Archive management tests
- `test_error_handling.py` - Error handling tests
- `test_file_size.py` - File size optimization tests

#### Integration Tests
- `test_mvp_functionality.py` - End-to-end MVP functionality tests
- `test_advanced_dedup.py` - Advanced deduplication scenarios

## Running Tests

### Run All Tests
```bash
npm run test
# or
python tests/run_tests.py
```

### Run Specific Test
```bash
python tests/test_mvp_functionality.py
```

### Run MVP Tests Only
```bash
npm run test:mvp
```

## Test Structure

Each test file should:
- Be self-contained and runnable independently
- Print clear PASS/FAIL status
- Provide useful output for debugging
- Exit with appropriate status codes (0 for success, 1 for failure)

## Best Practices

- Tests should be fast and reliable
- Use descriptive test names and clear output
- Test both success and failure scenarios
- Keep tests independent (no shared state)
- Document any special setup requirements
