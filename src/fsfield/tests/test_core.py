# -*- coding: utf8 -*-
import os.path as op
from django.test import TestCase
from fsfield.core import path_hash, hashed_path


class CoreTests(TestCase):

    def test_path_hash(self):
        self.assertEqual(path_hash("abc"), "qZk_NkcGgWq6PiVxeFDCbJzQ2J0")
        self.assertEqual(path_hash("abcé"), "bTkvtRcwOXVMzUc-qEmUth6Z3OM")
        self.assertEqual(path_hash(1), "NWoZK3kTsExUV00Ywo1G5jlUKKs")

    def test_hashed_path(self):
        self.assertEqual(hashed_path(1, 3), 
                op.join("N", "W", "o", "NWoZK3kTsExUV00Ywo1G5jlUKKs"))
