from app.recommendations import Recommendations

import unittest


class RecommendationsTest(unittest.TestCase):
    def setUp(self):
        self.friend_dict = {'0': {'1', '3'},
                            '1': {'0', '2', '3'},
                            '2': {'1', '3'},
                            '3': {'0', '1', '2', '4'},
                            '4': {'3', '5', '6'},
                            '5': {'4', '6'},
                            '6': {'4', '5'}}

        self.rec_obj = Recommendations(self.friend_dict)

    def tearDown(self):
        pass

    def test_run_common_neighbors(self):
        expected_outcome = [(('0', '2'), 2), (('0', '4'), 1), (('0', '5'), 0),
                            (('0', '6'), 0), (('1', '4'), 1), (('1', '5'), 0),
                            (('1', '6'), 0), (('2', '0'), 2), (('2', '4'), 1),
                            (('2', '5'), 0), (('2', '6'), 0), (('3', '5'), 1),
                            (('3', '6'), 1), (('4', '0'), 1), (('4', '1'), 1),
                            (('4', '2'), 1), (('5', '0'), 0), (('5', '1'), 0),
                            (('5', '2'), 0), (('5', '3'), 1), (('6', '0'), 0),
                            (('6', '1'), 0), (('6', '2'), 0), (('6', '3'), 1)]

        score_list = list()
        for node in self.friend_dict:
            for candidate_node in self.friend_dict:
                if candidate_node != node and candidate_node not in self.friend_dict[node]:
                    score_ex = self.rec_obj.run_common_neighbors(node, candidate_node)
                    score_list.append(((node, candidate_node), score_ex))

        self.assertEqual(len(score_list), len(expected_outcome))
        self.assertEqual(type(score_list), type(expected_outcome))
        self.assertCountEqual(score_list, expected_outcome)

    def test_run_jaccard(self):
        expected_outcome = [(('0', '2'), 1.0), (('0', '4'), 0.25), (('0', '5'), 0.0),
                            (('0', '6'), 0.0), (('1', '4'), 0.2), (('1', '5'), 0.0),
                            (('1', '6'), 0.0), (('2', '0'), 1.0), (('2', '4'), 0.25),
                            (('2', '5'), 0.0), (('2', '6'), 0.0), (('3', '5'), 0.2),
                            (('3', '6'), 0.2), (('4', '0'), 0.25), (('4', '1'), 0.2),
                            (('4', '2'), 0.25), (('5', '0'), 0.0), (('5', '1'), 0.0),
                            (('5', '2'), 0.0), (('5', '3'), 0.2), (('6', '0'), 0.0),
                            (('6', '1'), 0.0), (('6', '2'), 0.0), (('6', '3'), 0.2)]

        score_list = list()
        for node in self.friend_dict:
            for candidate_node in self.friend_dict:
                if candidate_node != node and candidate_node not in self.friend_dict[node]:
                    score_ex = self.rec_obj.run_jaccard(node, candidate_node)
                    score_list.append(((node, candidate_node), score_ex))

        self.assertEqual(len(score_list), len(expected_outcome))
        self.assertEqual(type(score_list), type(expected_outcome))
        self.assertCountEqual(score_list, expected_outcome)

    def test_run_adamin_adar(self):
        expected_outcome = [(('0', '2'), 1.631586747071319), (('0', '4'), 0.72134752044448169),
                            (('0', '5'), 0), (('0', '6'), 0),
                            (('1', '4'), 0.72134752044448169), (('1', '5'), 0),
                            (('1', '6'), 0), (('2', '0'), 1.631586747071319),
                            (('2', '4'), 0.72134752044448169), (('2', '5'), 0),
                            (('2', '6'), 0), (('3', '5'), 0.91023922662683732),
                            (('3', '6'), 0.91023922662683732), (('4', '0'), 0.72134752044448169),
                            (('4', '1'), 0.72134752044448169), (('4', '2'), 0.72134752044448169),
                            (('5', '0'), 0), (('5', '1'), 0),
                            (('5', '2'), 0), (('5', '3'), 0.91023922662683732),
                            (('6', '0'), 0), (('6', '1'), 0),
                            (('6', '2'), 0), (('6', '3'), 0.91023922662683732)]

        score_list = list()
        for node in self.friend_dict:
            for candidate_node in self.friend_dict:
                if candidate_node != node and candidate_node not in self.friend_dict[node]:
                    score_ex = self.rec_obj.run_adamin_adar(node, candidate_node)
                    score_list.append(((node, candidate_node), score_ex))

        self.assertEqual(len(score_list), len(expected_outcome))
        self.assertEqual(type(score_list), type(expected_outcome))
        self.assertCountEqual(score_list, expected_outcome)

    def test_find_recommendations(self):
        expected_outcome_common_neighbors = {'0': ['2', '4'],
                                             '1': ['4'],
                                             '2': ['0', '4'],
                                             '3': ['5', '6'],
                                             '4': ['0', '1', '2'],
                                             '5': ['3'],
                                             '6': ['3']}

        expected_outcome_jaccard = {'0': ['2', '4'],
                                    '1': ['4'],
                                    '2': ['0', '4'],
                                    '3': ['5', '6'],
                                    '4': ['0', '2', '1'],
                                    '5': ['3'],
                                    '6': ['3']}

        expected_outcome_a_a = {'0': ['2', '4'],
                                '1': ['4'],
                                '2': ['0', '4'],
                                '3': ['5', '6'],
                                '4': ['0', '1', '2'],
                                '5': ['3'],
                                '6': ['3']}

        kn_obj_1 = Recommendations(self.friend_dict)

        kn_obj_1.find_recommendations(score='common_neighbors')
        rec = kn_obj_1.recommendations
        self.assertEqual(len(rec), len(expected_outcome_common_neighbors))
        self.assertEqual(type(rec), type(expected_outcome_common_neighbors))
        self.assertCountEqual(rec, expected_outcome_common_neighbors)

        kn_obj_2 = Recommendations(self.friend_dict)
        kn_obj_2.find_recommendations(score='jaccard')
        rec = kn_obj_2.recommendations
        self.assertEqual(len(rec), len(expected_outcome_jaccard))
        self.assertEqual(type(rec), type(expected_outcome_jaccard))
        self.assertCountEqual(rec, expected_outcome_jaccard)

        kn_obj_3 = Recommendations(self.friend_dict)
        kn_obj_3.find_recommendations(score='adamic_adar')
        rec = kn_obj_3.recommendations
        self.assertEqual(len(rec), len(expected_outcome_a_a))
        self.assertEqual(type(rec), type(expected_outcome_a_a))
        self.assertCountEqual(rec, expected_outcome_a_a)
