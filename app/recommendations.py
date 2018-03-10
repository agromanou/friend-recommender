from pprint import pprint
import operator
import numpy as np


class Recommendations:
    def __init__(self, graph, number_of_suggestions=10):
        """
        :param graph: dict, of network nodes with a list of each node's friends
        :param number_of_suggestions: int, the number of top recommendations
        """
        self.graph = graph
        self.number_of_suggestions = number_of_suggestions
        self.recommendations = dict()

    def run_common_neighbors(self, node, candidate_node):
        """
        This method calculates common neighbors score for user similarity, i.e. measures the number
        of common friends of two nodes that are not yet friends
        :param node: id of a node
        :param candidate_node: id of a node
        :return: int, the common neighbors score
        """

        set_a = self.graph[node]
        set_b = self.graph[candidate_node]
        common_nodes = set_a & set_b

        score = len(common_nodes)

        return score

    def run_jaccard(self, node, candidate_node):
        """
        This method calculates jaccard distance score for user similarity, i.e. measures the number
        of common friends of two nodes that are not yet friends devided by their friends' union
        :param node: id of a node
        :param candidate_node: id of a node
        :return: int, the Jaccard score
        """
        set_a = self.graph[node]
        set_b = self.graph[candidate_node]
        common_nodes = set_a & set_b
        union = set_a | set_b

        score = len(common_nodes) / len(union)

        return score

    def run_adamin_adar(self, node, candidate_node):
        """
        This method calculates Adamin and Adar function score for user similarity, i.e. measures
        the inverse log frequency of their occurrence
        :param node: id of a node
        :param candidate_node: id of a node
        :return: int, the Adamin & Adar score
        """
        set_a = self.graph[node]
        set_b = self.graph[candidate_node]
        common_nodes = set_a & set_b

        score = 0
        for node in common_nodes:
            try:
                score += 1 / np.log(len(self.graph.get(node)))
            except TypeError:
                score += 0

        return score

    @staticmethod
    def sort_nodes(nodes_dict):
        """
        This method sorts a python dictionary based on their values
        :param nodes_dict: dict. with the nodes and their score
        :return: a sorted list of nodes based on their score
        """
        # In the case of ties in friendship score yields the node with the smallest nodeID
        sorted_nodes_score = [v for v in sorted(nodes_dict.items(), key=lambda kv: (-kv[1], kv[0]))]

        return sorted_nodes_score

    def run_algorithm(self, node, algorithm):
        """
        This method finds for a given node, its candidate recommendations sorted by their score
        :param node: int. the id number of a node
        :param algorithm: str. the name of the similarity score that will be calculated
        :return: list with sorted candidate node recommendations
        """
        node_rec = dict()
        for candidate_node in self.graph:

            # accept candidate nodes that are different the given node and are not
            # present in the friend list of the current node
            if candidate_node != node and candidate_node not in self.graph[node]:

                if algorithm == 'common_neighbors':
                    score = self.run_common_neighbors(node, candidate_node)

                elif algorithm == 'jaccard':
                    score = self.run_jaccard(node, candidate_node)

                elif algorithm == 'adamic_adar':
                    score = self.run_adamin_adar(node, candidate_node)

                else:
                    score = 0

                # ignore nodes with zero common friends (score)
                if score != 0:
                    node_rec[candidate_node] = score

        return self.sort_nodes(node_rec)

    def find_recommendations(self, score):
        """
        This method find top recommendations for each node of a network
        :return: dict. with the top recommended nodes for each node of the network
        """
        assert (score == 'common_neighbors' or 'jaccard' or 'adamic_adar')

        rec = dict()
        for node in self.graph:
            rec[node] = self.run_algorithm(node, algorithm=score)[:self.number_of_suggestions]

        self.recommendations = rec


if __name__ == '__main__':
    dict_ex = {'0': {'1', '3'},
               '1': {'0', '2', '3'},
               '2': {'1', '3'},
               '3': {'0', '1', '2', '4'},
               '4': {'3', '5', '6'},
               '5': {'4', '6'},
               '6': {'4', '5'}}

    rec_obj = Recommendations(dict_ex)

    rec_obj.find_recommendations(score='common_neighbors')
    pprint(rec_obj.recommendations)

    rec_obj.find_recommendations(score='jaccard')
    pprint(rec_obj.recommendations)

    rec_obj.find_recommendations(score='adamic_adar')
    pprint(rec_obj.recommendations)
