import json
from unittest import TestCase

import jsonh


class DumpsTest(TestCase):
    def test_compress(self):
        data = {
            'a': 1,
            'b': 2,
            'c': [
                {'name': 'john', 'age': 12},
                {'name': 'steve', 'age': 55},
                {'name': 'phillipe', 'age': 23},
            ],
        }

        exp_res_1 = json.dumps({
            'a': 1,
            'b': 2,
            'c': [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
        }, separators=(',', ':'))
        exp_res_2 = json.dumps({
            'a': 1,
            'b': 2,
            'c': [2, 'name', 'age', 'john', 12, 'steve', 55, 'phillipe', 23],
        }, separators=(',', ':'))


        res = jsonh.dumps(data)
        try:
            self.assertEqual(exp_res_1, res)
        except AssertionError:
            try:
                self.assertEqual(exp_res_2, res)
            except:
                raise


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

        res = jsonh.loads(data)
        self.assertEqual(exp_res, res)


class CompressTest(TestCase):
    def setUp(self):
        """Returns array of possible list that's compressed since dictionary
        does not guarantee order."""

        self.possibles = [
            [2, 'age', 'name', 12, 'john', 55, 'steve', 23, 'phillipe'],
            [2, 'name', 'age', 'john', 12, 'steve', 55, 'phillipe', 23]]

    def assert_compressed(self, res, possible_results):
        exc = None
        for possible_result in possible_results:
            try:
                self.assertEqual(possible_result, res)
            except AssertionError:
                pass
            except Exception as err:
                exc = err
        if exc is not None:
            raise exc

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

        res = jsonh.compress(data)

        exp_res_1 = {
            'a': 1,
            'b': 2,
            'c': self.possibles[0],
        }

        exp_res_2 = {
            'a': 1,
            'b': 2,
            'c': self.possibles[1],
        }
        self.assert_compressed(res, possible_results=[exp_res_1, exp_res_2])

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

        exp_res_1 = {
            'a': {
                'b': self.possibles[0],
            },
        }
        exp_res_2 = {
            'a': {
                'b': self.possibles[1],
            },
        }

        res = jsonh.compress(data)
        self.assert_compressed(res, possible_results=[exp_res_1, exp_res_2])

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

        exp_res_1 = {
            'data': [ 
                2, 'data', 'email',
                self.possibles[0],
                'test.1@email.com',
                self.possibles[0],
                'test.2@email.com',
            ],
        }
        exp_res_2 = {
            'data': [ 
                2, 'data', 'email',
                self.possibles[0],
                'test.1@email.com',
                self.possibles[1],
                'test.2@email.com',
            ],
        }
        exp_res_3 = {
            'data': [ 
                2, 'data', 'email',
                self.possibles[1],
                'test.1@email.com',
                self.possibles[0],
                'test.2@email.com',
            ],
        }
        exp_res_4 = {
            'data': [ 
                2, 'data', 'email',
                self.possibles[1],
                'test.1@email.com',
                self.possibles[1],
                'test.2@email.com',
            ],
        }

        res = jsonh.compress(data)
        self.assert_compressed(res, possible_results=[exp_res_1, exp_res_2,
                                                      exp_res_3, exp_res_4])


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

        res = jsonh.uncompress(data)
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

        res = jsonh.uncompress(data)
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

        res = jsonh.uncompress(data)
        self.assertEqual(exp_res, res)
