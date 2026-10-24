"""Offline regression for the observed pre-pixel Earth Engine setup failure."""
from pathlib import Path
import json
import unittest
from unittest.mock import Mock,patch
import acquire_input


class InitializationTests(unittest.TestCase):
    def test_initialize_precedes_transport_deadline(self):
        fake=Mock()
        with patch.object(acquire_input,'ee',fake):
            acquire_input.initialize_earth_engine()
        self.assertEqual(fake.mock_calls,[
            unittest.mock.call.Initialize(project='gen-lang-client-0932704594'),
            unittest.mock.call.data.setDeadline(120000)])

    def test_failed_initialize_does_not_configure_transport(self):
        fake=Mock()
        fake.Initialize.side_effect=RuntimeError('credentials unavailable')
        with patch.object(acquire_input,'ee',fake), self.assertRaises(RuntimeError):
            acquire_input.initialize_earth_engine()
        fake.data.setDeadline.assert_not_called()


if __name__=='__main__':
    result=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(InitializationTests))
    (Path(__file__).parent/'INITIALIZATION_REGRESSION_TESTS.json').write_text(json.dumps({
        'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,
        'scope':'MOCK_EE_ONLY; NO_NETWORK_OR_PIXELS'},indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
