from app.data_fetcher import DataFetcher
from pprint import pprint
import operator


class CommonNeighbors:
    def __init__(self, graph, number_of_suggestions=10):
        """
        :param graph: dict, of network nodes with a list of each node's friends
        :param number_of_suggestions: int, the number of top recommendations
        """
        self.graph = graph
        self.number_of_suggestions = number_of_suggestions
        self.recommendations = self.find_recommended_friends()

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

    def run_algorithm(self, node):
        """
        This method finds for a given node, its candidate recommendations sorted by their score
        :param node: int. the id number of a node
        :return: list with sorted candidate node recommendations
        """
        rec = dict()
        for candidate_node in self.graph:
            common_friends = 0

            # accept candidate nodes that are different the given node and are not
            # present in the friend list of the current node
            if candidate_node != node and candidate_node not in self.graph[node]:

                # search candidate node's friend list for common friends
                for candidate_node_friend in self.graph[candidate_node]:
                    if candidate_node_friend in self.graph[node]:
                        common_friends += 1

                # ignore nodes with zero common friends (score)
                if common_friends != 0:
                    rec[candidate_node] = common_friends

        return self.sort_nodes(rec)

    def find_recommended_friends(self):
        """
        This method find top recommendations for each node of a network
        :return: dict. with the top recommended nodes for each node of the network
        """
        rec = dict()
        for node in self.graph:
            rec[node] = self.run_algorithm(node)[:self.number_of_suggestions]

        return rec


if __name__ == '__main__':
    data_obj = DataFetcher()

    kn_obj = CommonNeighbors(data_obj.network_dict)
    recommendations = kn_obj.recommendations
    pprint(recommendations)




