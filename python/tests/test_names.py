import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import nookara
from nookara import Client, Ember, Instance


class NamesTests(unittest.TestCase):
    def test_old_names_are_gone(self):
        self.assertFalse((Path(nookara.__file__).parents[1] / 'velora_api').exists())
        for name in ('Bonfire', 'BONFIRE_APP_MASK'):
            self.assertFalse(hasattr(nookara, name), name)
        self.assertFalse(hasattr(nookara.scopes, 'BONFIRE_APP_SCOPES'))
        for name in ('bonfire_instances', 'start_bonfire_import', 'bonfire_session'):
            self.assertFalse(hasattr(Client, name), name)
        for name in ('login_with_velora', 'register_with_velora', 'import_from_velora', 'velora_origin'):
            self.assertFalse(hasattr(Instance, name), name)

    def test_new_names(self):
        self.assertIn('Ember', nookara.__all__)
        self.assertIn('EMBER_APP_MASK', nookara.__all__)
        self.assertEqual(Instance('https://chat.example', nookara_url='https://other.example').nookara_origin, 'https://other.example')
        self.assertIs(Ember(Client('t')).nookara.__class__, Client)
        with self.assertRaises(TypeError):
            Instance('https://chat.example', velora_url='https://other.example')


if __name__ == '__main__':
    unittest.main()
