import importlib
import sys
import unittest
import warnings
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import nookara
from nookara import Client, Ember, Instance, BotProgram, EMBER_APP_MASK


class OldNamesTests(unittest.TestCase):
    def assert_warns(self, fn):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            result = fn()
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught), caught)
        return result

    def test_velora_api_still_imports(self):
        sys.modules.pop('velora_api', None)
        module = self.assert_warns(lambda: importlib.import_module('velora_api'))
        self.assertIs(module.Client, Client)
        self.assertIs(importlib.import_module('velora_api.client'), nookara.client)
        self.assertIs(importlib.import_module('velora_api.bonfire'), nookara.ember)
        from velora_api.client import login_app
        self.assertIs(login_app, nookara.login_app)

    def test_old_module_names(self):
        self.assertIs(self.assert_warns(lambda: nookara.Bonfire), Ember)
        self.assertEqual(self.assert_warns(lambda: nookara.BONFIRE_APP_MASK), EMBER_APP_MASK)
        self.assertEqual(self.assert_warns(lambda: nookara.scopes.BONFIRE_APP_SCOPES), nookara.scopes.EMBER_APP_SCOPES)
        self.assertNotIn('Bonfire', nookara.__all__)

    def test_old_client_methods_call_the_new_ones(self):
        c = Client('t')
        with patch.object(Client, 'ember_instances', return_value=['x']) as new:
            self.assertEqual(self.assert_warns(lambda: c.bonfire_instances()), ['x'])
        new.assert_called_once_with()
        with patch.object(Client, 'start_ember_import', return_value={'job_id': 'j'}) as new:
            self.assert_warns(lambda: c.start_bonfire_import('discord', '1', ['2'], 'https://chat.example'))
        new.assert_called_once_with('discord', '1', ['2'], 'https://chat.example')

    def test_old_instance_names(self):
        inst = self.assert_warns(lambda: Instance('https://chat.example', velora_url='https://other.example'))
        self.assertEqual(inst.nookara_origin, 'https://other.example')
        self.assertEqual(self.assert_warns(lambda: inst.velora_origin), 'https://other.example')
        self.assertEqual(Instance('https://chat.example').nookara_origin, 'https://nookara.cc')
        with patch.object(Instance, 'login_with_nookara', return_value='ok') as new:
            self.assertEqual(self.assert_warns(lambda: inst.login_with_velora('client', sign=True)), 'ok')
        new.assert_called_once_with('client', sign=True)

    def test_old_keywords(self):
        program = self.assert_warns(lambda: BotProgram('b', velora_url='http://127.0.0.1:1', allow_insecure=True))
        self.assertEqual(program._nookara.base_url, 'http://127.0.0.1:1')
        client = Client('t')
        hub = self.assert_warns(lambda: Ember(velora=client))
        self.assertIs(hub.nookara, client)
        self.assertIs(self.assert_warns(lambda: hub.velora), client)


if __name__ == '__main__':
    unittest.main()
