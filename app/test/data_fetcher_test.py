from app.data_fetcher import DataFetcher

import unittest


class DataFetcherTest(unittest.TestCase):
    def setUp(self):
        self.network_example = [[1, 0], [1, 2], [2, 3],
                                [3, 1], [3, 0], [3, 4],
                                [4, 5], [4, 6], [5, 4],
                                [5, 6]]

        self.undirected_2 = [[1, 0], [0, 1], [3, 1],
                             [1, 2], [2, 1], [1, 3],
                             [0, 3], [3, 0], [3, 2],
                             [2, 3], [3, 4], [4, 3],
                             [4, 5], [5, 4], [5, 6],
                             [6, 5], [4, 6], [6, 4]]

        self.undirected = [[1, 0], [1, 2], [2, 3],
                           [3, 1], [3, 0], [3, 4],
                           [4, 5], [4, 6], [5, 4],
                           [5, 6], [0, 1], [2, 1],
                           [3, 2], [1, 3], [0, 3],
                           [4, 3], [5, 4], [6, 4],
                           [4, 5], [6, 5]]

        self.friend_dict = {0: {1, 3},
                            1: {0, 2, 3},
                            2: {1, 3},
                            3: {0, 1, 2, 4},
                            4: {3, 5, 6},
                            5: {4, 6},
                            6: {4, 5}}

    def tearDown(self):
        pass

    def test_load_network_normal_execution(self):
        exp_network = [[1, 2], [2, 4]]
        network = DataFetcher.load_network()

        self.assertEqual(type(network), type(exp_network))

    def test_create_undirected_graph_normal_execution(self):
        undirected_graph = DataFetcher.create_undirected_graph(self.network_example)

        self.assertEqual(len(undirected_graph), len(self.undirected))
        self.assertEqual(type(undirected_graph), type(self.undirected))
        self.assertCountEqual(undirected_graph, self.undirected)

    def test_create_friend_dict_normal_execution(self):
        friend_dict_output = DataFetcher.create_friend_dict(self.undirected)

        self.assertEqual(len(friend_dict_output), len(self.friend_dict))
        self.assertEqual(type(friend_dict_output), type(self.friend_dict))
        self.assertCountEqual(friend_dict_output, self.friend_dict)
