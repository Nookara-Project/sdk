import unittest

import nookara
from nookara import (EMBER_ALL_PERMISSIONS, EMBER_PERMISSIONS, ember_permission_bit, ember_permission_mask,
                     ember_permission_names, has_ember_permission)


class EmberPermissionTests(unittest.TestCase):
    def test_names_and_back(self):
        self.assertEqual(ember_permission_names(257), ["SEND", "ATTACH"])
        self.assertEqual(ember_permission_names("0x101"), ["SEND", "ATTACH"])
        self.assertEqual(ember_permission_names(0), [])
        self.assertEqual(ember_permission_mask("SEND", "ATTACH"), 257)
        self.assertEqual(ember_permission_mask(["SEND", "ATTACH"]), 257)
        self.assertEqual(ember_permission_mask(), 0)

    def test_words_labels_and_aliases(self):
        self.assertEqual(ember_permission_bit("send messages"), 1)
        self.assertEqual(ember_permission_bit("Mention @everyone, @here and all roles"), 128)
        self.assertEqual(ember_permission_bit("manage-messages"), 64)
        self.assertEqual(ember_permission_bit("administrator"), 512)
        self.assertEqual(ember_permission_bit(256), 256)
        with self.assertRaises(ValueError):
            ember_permission_bit("NOPE")
        with self.assertRaises(ValueError):
            ember_permission_bit(3)

    def test_unknown_bits_round_trip(self):
        self.assertEqual(ember_permission_names(4096 + 8192), ["UNMARKED_ALIASES", "BIT_13"])
        self.assertEqual(ember_permission_mask("UNMARKED_ALIASES", "BIT_13"), 12288)
        big = (1 << 60) | 1
        self.assertEqual(ember_permission_mask(ember_permission_names(big)), big)

    def test_every_permission_round_trips(self):
        everything = 0
        for bit in EMBER_PERMISSIONS.values():
            everything |= bit
        self.assertEqual(ember_permission_mask(ember_permission_names(everything)), everything)
        self.assertEqual(len(ember_permission_names(everything)), len(EMBER_PERMISSIONS))
        self.assertEqual(EMBER_ALL_PERMISSIONS & EMBER_PERMISSIONS["VIEW"], 0)

    def test_has_permission(self):
        self.assertTrue(has_ember_permission(257, "SEND"))
        self.assertFalse(has_ember_permission(257, "KICK"))
        self.assertTrue(has_ember_permission(512, "KICK"))
        self.assertFalse(has_ember_permission(512, "BIT_40"))
        with self.assertRaises(ValueError):
            has_ember_permission("abc", "SEND")
        with self.assertRaises(ValueError):
            ember_permission_names(-1)

    def test_exported(self):
        for name in ("ember_permission_mask", "ember_permission_names", "has_ember_permission", "EMBER_PERMISSIONS"):
            self.assertIn(name, nookara.__all__)


if __name__ == "__main__":
    unittest.main()
