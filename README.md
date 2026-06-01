# QA Platform Fixture: Python Environment Variables

Private fixture repository for QA Platform UI environment-variable verification.

Suggested UI configuration:

- Git URL: `https://github.com/Ike-li/qa-platform-fixture-python-env.git`
- Default branch: `main`
- Base image: `python:3.12-alpine`
- Runner: `pytest`
- Test paths: `test_env.py`
- Collector path: `results/junit.xml`
- Environment variable: `QA_PLATFORM_FIXTURE_MESSAGE=hello-from-ui`

This repository is dependency-free. It verifies that environment variables configured in the QA Platform UI reach the test process.
