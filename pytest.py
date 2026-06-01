from __future__ import annotations

import argparse
import html
import os
import sys
import time
import traceback
import unittest


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--junitxml', default='results/junit.xml')
    known, remaining = parser.parse_known_args()
    paths = [value for value in remaining if not value.startswith('-')] or ['.']

    class RecordingResult(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.records = []

        def addSuccess(self, test):
            super().addSuccess(test)
            self.records.append((test, 'passed', None, ''))

        def addFailure(self, test, err):
            super().addFailure(test, err)
            self.records.append((test, 'failed', str(err[1]), ''.join(traceback.format_exception(*err))))

        def addError(self, test, err):
            super().addError(test, err)
            self.records.append((test, 'error', str(err[1]), ''.join(traceback.format_exception(*err))))

        def addSkip(self, test, reason):
            super().addSkip(test, reason)
            self.records.append((test, 'skipped', reason, ''))

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for value in paths:
        if os.path.isdir(value):
            suite.addTests(loader.discover(value))
            continue
        module_name = os.path.splitext(os.path.basename(value))[0]
        module_dir = os.path.dirname(os.path.abspath(value)) or os.getcwd()
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)
        suite.addTests(loader.loadTestsFromName(module_name))

    start = time.time()
    runner = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult)
    result = runner.run(suite)
    elapsed = time.time() - start
    write_junit(known.junitxml, result, elapsed)
    print_summary(result, elapsed)
    return 0 if result.wasSuccessful() else 1


def write_junit(path: str, result, elapsed: float) -> None:
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    failed = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(f'<testsuite name="qa-platform-fixture" tests="{result.testsRun}" failures="{failed}" errors="{errors}" skipped="{skipped}" time="{elapsed:.3f}">\n')
        for test, status, message, detail in result.records:
            name = html.escape(str(test))
            classname = html.escape(test.__class__.__name__)
            fh.write(f'  <testcase classname="{classname}" name="{name}" time="0">')
            if status == 'failed':
                fh.write(f'<failure message="{html.escape(message or "failed")}">{html.escape(detail)}</failure>')
            elif status == 'error':
                fh.write(f'<error message="{html.escape(message or "error")}">{html.escape(detail)}</error>')
            elif status == 'skipped':
                fh.write(f'<skipped message="{html.escape(message or "skipped")}"/>')
            fh.write('</testcase>\n')
        fh.write('</testsuite>\n')


def print_summary(result, elapsed: float) -> None:
    passed = sum(1 for _, status, _, _ in result.records if status == 'passed')
    parts = []
    if passed:
        parts.append(f'{passed} passed')
    if result.failures:
        parts.append(f'{len(result.failures)} failed')
    if result.errors:
        parts.append(f'{len(result.errors)} errors')
    if result.skipped:
        parts.append(f'{len(result.skipped)} skipped')
    print(f"===== {', '.join(parts) or '0 passed'} in {elapsed:.2f}s =====")


if __name__ == '__main__':
    raise SystemExit(main())
