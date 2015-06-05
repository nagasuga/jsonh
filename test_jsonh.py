import json
from unittest import TestCase

from .jsonh import dumps, loads, compress, uncompress


class DumpsTest(TestCase):
    def test_compress(self):
        data = {
            'a': 1,
            'b': 2,
            'c': [
                {'name': 'john', 'age': 12},
                {'name': 'steve', 'age': 55},
                {'name': 'phillipe', 'age': 23},
            ]
        }

        exp_res = json.dumps({
            'a': 1,
            'b': 2,
            'c': [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
        })

        res = dumps(data)
        self.assertEqual(exp_res, res)


class LoadsTest(TestCase):
    def test_nested(self):
        exp_res = {
            'data': [
                {
                    'email': 'test.1@email.com',
                    'data': [
                        {'name': 'john', 'age': 12},
                        {'name': 'steve', 'age': 55},
                        {'name': 'phillipe', 'age': 23},
                    ],
                },
                {
                    'email': 'test.2@email.com',
                    'data': [
                        {'name': 'john', 'age': 12},
                        {'name': 'steve', 'age': 55},
                        {'name': 'phillipe', 'age': 23},
                    ],
                },
            ]
        }

        data = json.dumps({
            'data': [ 
                2, 'data', 'email',
                [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
                'test.1@email.com',
                [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
                'test.2@email.com',
            ],
        })

        res = loads(data)
        self.assertEqual(exp_res, res)


class CompressTest(TestCase):
    def test_compress(self):
        data = {
            'a': 1,
            'b': 2,
            'c': [
                {'name': 'john', 'age': 12},
                {'name': 'steve', 'age': 55},
                {'name': 'phillipe', 'age': 23},
            ]
        }

        exp_res = {
            'a': 1,
            'b': 2,
            'c': [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
        }

        res = compress(data)
        self.assertEqual(exp_res, res)

    def test_second_level(self):
        data = {
            'a': {
                'b': [
                    {'name': 'john', 'age': 12},
                    {'name': 'steve', 'age': 55},
                    {'name': 'phillipe', 'age': 23},
                ],
            },
        }

        exp_res = {
            'a': {
                'b': [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
            },
        }

        res = compress(data)
        self.assertEqual(exp_res, res)

    def test_nested(self):
        data = {
            'data': [
                {
                    'email': 'test.1@email.com',
                    'data': [
                        {'name': 'john', 'age': 12},
                        {'name': 'steve', 'age': 55},
                        {'name': 'phillipe', 'age': 23},
                    ],
                },
                {
                    'email': 'test.2@email.com',
                    'data': [
                        {'name': 'john', 'age': 12},
                        {'name': 'steve', 'age': 55},
                        {'name': 'phillipe', 'age': 23},
                    ],
                },
            ]
        }

        exp_res = {
            'data': [ 
                2, 'data', 'email',
                [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
                'test.1@email.com',
                [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
                'test.2@email.com',
            ],
        }

        res = compress(data)
        self.assertEqual(exp_res, res)


class UncompressTest(TestCase):
    def test_uncompress(self):
        data = {
            'a': 1,
            'b': 2,
            'c': [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
        }

        exp_res = {
            'a': 1,
            'b': 2,
            'c': [
                {'name': 'john', 'age': 12},
                {'name': 'steve', 'age': 55},
                {'name': 'phillipe', 'age': 23},
            ]
        }

        res = uncompress(data)
        self.assertEqual(exp_res, res)

    def test_second_level(self):
        data = {
            'a': {
                'b': [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
            },
        }

        exp_res = {
            'a': {
                'b': [
                    {'name': 'john', 'age': 12},
                    {'name': 'steve', 'age': 55},
                    {'name': 'phillipe', 'age': 23},
                ],
            },
        }

        res = uncompress(data)
        self.assertEqual(exp_res, res)

    def test_nested(self):
        exp_res = {
            'data': [
                {
                    'email': 'test.1@email.com',
                    'data': [
                        {'name': 'john', 'age': 12},
                        {'name': 'steve', 'age': 55},
                        {'name': 'phillipe', 'age': 23},
                    ],
                },
                {
                    'email': 'test.2@email.com',
                    'data': [
                        {'name': 'john', 'age': 12},
                        {'name': 'steve', 'age': 55},
                        {'name': 'phillipe', 'age': 23},
                    ],
                },
            ]
        }

        data = {
            'data': [ 
                2, 'data', 'email',
                [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
                'test.1@email.com',
                [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
                'test.2@email.com',
            ],
        }

        res = uncompress(data)
        self.assertEqual(exp_res, res)
