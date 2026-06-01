import os
import unittest


class FixtureEnvironmentTest(unittest.TestCase):
    def test_message_reaches_test_process(self):
        self.assertEqual(
            os.environ.get('QA_PLATFORM_FIXTURE_MESSAGE'),
            'hello-from-ui',
        )

    def test_default_python_runtime_is_available(self):
        self.assertTrue(os.environ.get('PATH'))
