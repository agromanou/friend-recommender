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
        for friend_node in self.graph[node]:

            for friend_of_friend_node in self.graph[friend_node]:

                # accept candidate nodes that are different the given node and are not
                # present in the friend list of the current node
                if friend_of_friend_node != node and friend_of_friend_node not in self.graph[node]:

                    if algorithm == 'common_neighbors':
                        score = self.run_common_neighbors(node, friend_of_friend_node)

                    elif algorithm == 'jaccard':
                        score = self.run_jaccard(node, friend_of_friend_node)

                    elif algorithm == 'adamic_adar':
                        score = self.run_adamin_adar(node, friend_of_friend_node)

                    elif algorithm == 'cosine':
                        score = self.run_cosine(node, friend_of_friend_node)

                    elif algorithm == 'baseline':
                        score = random.randint(0, len(self.graph))

                else:
                    score = 0

                # ignore nodes with zero common friends (score)
                if score != 0:
                    node_rec[friend_of_friend_node] = score

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
        algo_list = ['common_neighbors', 'jaccard', 'adamic_adar', 'cosine', 'baseline']
        total_rank_list = {'common_neighbors': [], 'jaccard': [], 'adamic_adar': [], 'cosine': [], 'baseline': []}
        while (times_of_execution < 100):
            comparison_list = dict()
            # Step 1: Randomly choose a real friend connection; call the two friends F1 and F2.
            f1 = random.choice(list(self.graph.keys()))
            if (len(self.graph[f1]) > 0):

                f2 = random.choice(list(self.graph[f1]))
                #print('The ids of friends that are chosen for the evaluation purposes are f1 = ' + str(f1) + ' and f2 = ' + str(f2))
                # Step 2: Remove their friendship from the graph.
                self.remove_edge(f1, f2)
                for method_name in algo_list:

                    f1_list = self.run_algorithm(f1, method_name)
                    f2_list = self.run_algorithm(f2, method_name)
                    top10_f1 = f1_list[:10] if len(f1_list) > 10 else f1_list
                    top10_f2 = f2_list[:10] if len(f2_list) > 10 else f2_list

                    comparison_list[f1] = set()
                    if len(top10_f1) > 0:
                        for item in top10_f1:
                            comparison_list[f1].add(item[0])

                    comparison_list[f2] = set()
                    if len(top10_f2) > 0:
                        for item in top10_f2:
                            comparison_list[f2].add(item[0])
                    rank1 = -1
                    rank2 = - 1
                    i = 0
                    for x in comparison_list[f1]:
                        if f2 == x:
                            rank1 = i + 1
                            break
                        else:
                            i = i + 1
                    i = 0
                    for x in comparison_list[f2]:
                        if f1 == x:
                            rank2 = i + 1
                            break
                        else:
                            i = i + 1
                    if (rank1 != -1 and rank2 != -1):
                        times_of_execution = times_of_execution + 1
                        rank = round((rank1 + rank2)/2, 2)
                        total_rank_list[method_name].append(rank)
                    else :
                        rank = 0

                # Step 5: Put their friendship back in the graph.
                self.add_edge(f1, f2)

            else:
                continue
        for item in total_rank_list:
            average_rank = 0
            if len(total_rank_list[item]) > 0 :
                average_rank = round(sum(total_rank_list[item]) / len(total_rank_list[item]), 2)
            print('The average rank of the correct recommendation for ' + item + ' is: ' + str(average_rank))
            print(total_rank_list)

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
        """
        This method gets 40 Facebook users with an id that is a multiple of 100
        """
        nodeId = 0
        self.examined_facebook_users = []
        for x in range(0, 40):
            nodeId = nodeId + 100
            self.examined_facebook_users.append(str(nodeId))
            
    def compute_the_number_users_with_the_same_first_and_different_10_recommendations(self):
        self.get_ids_multiple_to_100()
        self.recommended_list_per_algorithm = {'common_neighbors': dict(), 'jaccard': dict(), 'adamic_adar': dict(), 'cosine': dict(), ''baseline': dict()}

        algo_list = ['common_neighbors', 'jaccard', 'adamic_adar', 'cosine', 'baseline']

        for recommendation_method in algo_list:
            print('Testing the scoring function ' + recommendation_method)
            comparsion_list = dict()
            for facebook_usr in self.examined_facebook_users:
                recommendation_list = self.run_algorithm(facebook_usr, recommendation_method)
                top_ten_friends = recommendation_list[:10] if len(recommendation_list) > 10 else recommendation_list
                comparsion_list[facebook_usr] = set()
                if len(top_ten_friends) > 0:
                    for item in top_ten_friends:
                       comparsion_list[facebook_usr].add(item[0])

            self.recommended_list_per_algorithm[recommendation_method] = comparsion_list
            list_of_similar_recommendations = set()
            list_of_different_recommendations = set()
            i = 0
            for user1 in self.examined_facebook_users:
                if i < 39:
                    compared_list1 = comparsion_list[self.examined_facebook_users[i]]
                    for fb_user in self.examined_facebook_users[i + 1:]:
                        compared_list2 = comparsion_list[fb_user]
                        if (len(compared_list2) == 10 and len(compared_list1) == len(compared_list2) and len(compared_list1 & compared_list2) == 10):
                            if fb_user not in list_of_similar_recommendations:
                                list_of_similar_recommendations.add(fb_user)
                            if user1 not in list_of_similar_recommendations:
                                list_of_similar_recommendations.add(user1)
                        else :
                            if fb_user not in list_of_different_recommendations:
                                list_of_different_recommendations.add(fb_user)
                            if user1 not in list_of_different_recommendations:
                                list_of_different_recommendations.add(user1)
                i = i + 1
            print('The number of Facebook users who have the same first 10 friend recommendations is ' + str(len(list_of_similar_recommendations)))
            print('The number of Facebook users who have the different first 10 friend recommendations is ' + str(len(list_of_different_recommendations)))
            print('\n')

    def compute_similarity_percentage(self, methodA = 'common_neighbors', methodB = 'jaccard'):
        recommendation_list1 = self.recommended_list_per_algorithm[methodA]
        recommendation_list2 = self.recommended_list_per_algorithm[methodB]

        number_of_similar_rec = 0
        total_number_of_rec = 0
        for fb_usr in self.examined_facebook_users:

            listA = recommendation_list1[fb_usr]
            listB = recommendation_list2[fb_usr]
            number_of_similar_rec = number_of_similar_rec + len(listA & listB)
            total_number_of_rec = total_number_of_rec + max(len(listA), len(listB))

        similarity_percentage = round((number_of_similar_rec * 100) / total_number_of_rec, 2)
        print('The similarity percentage of the recommended friend lists for the 40 users for pair ' + methodA + ' - ' + methodB + ' is: ' + str(similarity_percentage) + '%')
        return similarity_percentage
    
    
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

    # rec_obj.evaluate_scoring_functions()
    # print(rec_obj.get_ids_multiple_to_100())

    rec_obj.find_recommendations(score='common_neighbors')
    print()
    print('-'*30)
    print('Common neighbors results')
    pprint(rec_obj.recommendations)
    print('-'*30)

    rec_obj.find_recommendations(score='jaccard')
    print()
    print('-'*30)
    print('Jaccard results')
    pprint(rec_obj.recommendations)

    rec_obj.find_recommendations(score='adamic_adar')
    print()
    print('-'*30)
    print('Adamic & Adar results')
    pprint(rec_obj.recommendations)

    rec_obj.find_recommendations(score='cosine')
    print()
    print('-' * 30)
    print('Cosine results')
    pprint(rec_obj.recommendations)

    rec_obj.find_recommendations(score='baseline')
    print()
    print('-' * 30)
    print('Baseline results')
    pprint(rec_obj.recommendations)
