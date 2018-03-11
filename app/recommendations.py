from pprint import pprint
import numpy as np
import random


class Recommendations:

    SEED = 12356778

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
        This method calculates Jaccard distance score for user similarity, i.e. measures the number
        of common friends of two nodes that are not yet friends divided by their friends' union
        :param node: id of a node
        :param candidate_node: id of a node
        :return: int, the Jaccard score
        """
        set_a = self.graph[node]
        set_b = self.graph[candidate_node]
        common_nodes = set_a & set_b
        union = set_a | set_b

        score = len(common_nodes) / len(union)

        return round(score, 4)

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

        return round(score, 4)

    def run_cosine(self, node, candidate_node):
        """
        This method calculates cosine similarity score, i.e. measures the cosine of the angle
        between the characteristic vectors of the two neighborhoods.
        :param candidate_node: id of a node
        :return: int, the cosine score
        """
        set_a = self.graph[node]
        set_b = self.graph[candidate_node]
        common_nodes = set_a & set_b

        score = len(common_nodes) / np.sqrt(len(set_a)*len(set_b))

        return round(score, 4)

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

                elif algorithm == 'cosine':
                    score = self.run_cosine(node, candidate_node)

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

    def evaluate_scoring_functions(self):
        """
        This method evaluates which scoring function recommends the best links
        """
        times_of_execution = 0
        while (times_of_execution < 100):

            #Step 1: Randomly choose a real friend connection; call the two friends F1 and F2.
            f1 = random.choice(list(self.graph.keys()))
            if (len(self.graph[f1]) > 0) :
                times_of_execution = times_of_execution + 1

                f2 = random.choice(list(self.graph[f1]))
                print('The ids of friends that are chosen for the evaluation purposes are f1 = ' + str(f1) + ' and f2 = ' + str(f2))

                #Step 2: Remove their friendship from the graph.
                print('Print the graph before removing the edge')
                print(self.graph)
                self.remove_edge(f1, f2)
                print('Print the graph after removing the edge')
                print(self.graph)

                #Step 5: Put their friendship back in the graph.
                print('Add again the edge to the original graph')
                self.add_edge(f1, f2)
                print(self.graph)

            else:
                continue

    def remove_edge(self, e, e2):
        try:
            if self.graph != None:
                if e in self.graph and e2 in self.graph[e]:
                    self.graph[e].remove(e2)
                if e2 in self.graph and e in self.graph[e2]:
                    self.graph[e2].remove(e)
            return True

        except:
            return None

    def add_edge(self, f1, f2):
        try:
            if self.graph != None:
                self.graph[f1].add(f2)
                self.graph[f2].add(f1)
            return True

        except:
            return None

    def get_ids_multiple_to_100(self):
        nodeId = 0
        examined_facebook_users = []
        for x in range(0, 40):
            nodeId = nodeId + 100
            examined_facebook_users.append(str(nodeId))

        return examined_facebook_users


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
    print()
    print('Toy example')
    pprint(dict_ex)
    print('-'*30)
    print('Common neighbors results')
    pprint(rec_obj.recommendations)
    print('-'*30)

    rec_obj.find_recommendations(score='jaccard')
    print()
    print('Toy example')
    pprint(dict_ex)
    print('-'*30)
    print('Jaccard results')
    pprint(rec_obj.recommendations)

    rec_obj.find_recommendations(score='adamic_adar')
    print()
    print('Toy example')
    pprint(dict_ex)
    print('-'*30)
    print('Adamic & Adar results')
    pprint(rec_obj.recommendations)

    rec_obj.find_recommendations(score='cosine')
    print()
    print('Toy example')
    pprint(dict_ex)
    print('-' * 30)
    print('Cosine results')
    pprint(rec_obj.recommendations)

    rec_obj.evaluate_scoring_functions()
    print(rec_obj.get_ids_multiple_to_100())
