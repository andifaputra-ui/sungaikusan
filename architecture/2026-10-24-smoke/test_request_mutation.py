"""Offline reproduction of EE's in-place request mutation and receipt failure."""
from pathlib import Path
import json
import unittest
from acquire_input import download_url_without_mutation


class MutatingImage:
    def getDownloadURL(self,params):
        params['image']=self
        params['dimensions'][0]=999
        return 'https://example.invalid/not-requested'


class RequestTests(unittest.TestCase):
    def test_upstream_mutation_would_break_json(self):
        request={'dimensions':[512,512]}
        MutatingImage().getDownloadURL(request)
        with self.assertRaises(TypeError):
            json.dumps(request)

    def test_provenance_remains_serializable_and_unchanged(self):
        request={'dimensions':[512,512]}
        url=download_url_without_mutation(MutatingImage(),request)
        self.assertEqual(request,{'dimensions':[512,512]})
        self.assertEqual(json.loads(json.dumps(request)),request)
        self.assertEqual(url,'https://example.invalid/not-requested')


if __name__=='__main__':
    result=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(RequestTests))
    (Path(__file__).parent/'REQUEST_MUTATION_TESTS.json').write_text(json.dumps({
        'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,
        'scope':'MOCK_ONLY; NO_NETWORK_OR_PIXELS'},indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
