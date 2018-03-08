from app.data_fetcher import DataFetcher
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
        This method calculates common neighbors score for user similarity
        :param node: The node
        :param candidate_node:
        :return:
        """

        # search candidate node's friend list for common friends
        set_a = self.graph[node]
        set_b = self.graph[candidate_node]
        common_nodes = set_a & set_b

        score = len(common_nodes)

        return score

    def run_jaccard(self, node, candidate_node):
        """
        This method calculates jaccard distance score for user similarity
        :param node:
        :param candidate_node:
        :return:
        """

        # search candidate node's friend list for common friends
        set_a = self.graph[node]
        set_b = self.graph[candidate_node]
        common_nodes = set_a & set_b
        union = set_a | set_b

        score = len(common_nodes) / len(union)

        return score

    def run_adamin_adar(self, node, candidate_node):
        """
        This method calculates Adamin and Adar function score for user similarity
        :param node:
        :param candidate_node:
        :return:
        """

        # search candidate node's friend list for common friends
        set_a = self.graph[node]
        set_b = self.graph[candidate_node]
        common_nodes = set_a & set_b

        score = 0
        for node in common_nodes:
            score += 1 / np.log(len(self.graph[node]))

        return score

    @staticmethod
    def sort_nodes(nodes_dict):
        """
        This method sorts a python dictionary based on their values
        :param nodes_dict: dict. with the nodes and their score
        :return: a sorted list of nodes based on their score
        """
        sorted_nodes_score = sorted(nodes_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_nodes = list(map(lambda x: x[0], sorted_nodes_score))

        return sorted_nodes

    def run_algorithm(self, node, algo):
        """
        This method finds for a given node, its candidate recommendations sorted by their score
        :param node: int. the id number of a node
        :return: list with sorted candidate node recommendations
        """
        node_rec = dict()
        for candidate_node in self.graph:

            # accept candidate nodes that are different the given node and are not
            # present in the friend list of the current node
            if candidate_node != node and candidate_node not in self.graph[node]:

                if algo == 'common_neighbors':
                    score = self.run_common_neighbors(node, candidate_node)

                elif algo == 'jaccard':
                    score = self.run_jaccard(node, candidate_node)

                elif algo == 'adamic_adar':
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
        assert(score == 'common_neighbors' or 'jaccard' or 'adamic_adar')
        self.algo = score

        rec = dict()
        for node in self.graph:
            rec[node] = self.run_algorithm(node, algo=score)[:self.number_of_suggestions]

        self.recommendations = rec


if __name__ == '__main__':
    data_obj = DataFetcher()

    kn_obj = Recommendations(data_obj.network_dict)

    kn_obj.find_recommendations(score='common_neighbors')
    pprint(kn_obj.recommendations)

    kn_obj.find_recommendations(score='jaccard')
    pprint(kn_obj.recommendations)

    kn_obj.find_recommendations(score='adamic_adar')
    pprint(kn_obj.recommendations)




