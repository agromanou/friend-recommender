from pprint import pprint
import networkx as nx
import json


class DataFetcher:
    def __init__(self, path):
        self.graph = self.load_network(path)
        # print('Data loaded: {}'.format(len(self.graph)))

        self.undirected = self.create_undirected_graph(self.graph)
        # print('Undirected graph has been created: {}'.format(len(self.undirected)))

        self.network_dict = self.create_friend_dict(self.undirected)

    @staticmethod
    def load_data_example():
        graph = [['1', '0'], ['2', '3'],
                 ['3', '1'], ['3', '0'], ['3', '4'],
                 ['4', '5'], ['4', '6'], ['5', '4'],
                 ['5', '6']]

        return graph

    @staticmethod
    def load_network(path):
        """
        This method loads the data form the given txt file
        :return: list of lists with the edges of the graph
        """
        with open(path) as f:
            content = f.read()

        edge_str = content.split('\n')
        network = list()
        for edge in edge_str:
            network.append(edge.split())

        return network

    @staticmethod
    def create_undirected_graph(directed_graph):
        """
        It transforms a directed graph into an undirected one.
        :param directed_graph: list of lists with the directed graph
        :return: list of tuples with the undirected graph
        """
        undirected_graph = list()
        for directed_edge in directed_graph:
            try:
                undirected_edge = [directed_edge[1], directed_edge[0]]
                undirected_graph.append(undirected_edge)
            except IndexError:
                pass

        return directed_graph + undirected_graph

        # d_graph = nx.Graph()
        # for element in directed_graph:
        #     d_graph.add_path(element)
        #
        # undirected_graph = d_graph.to_undirected()
        #
        # return nx.edges(undirected_graph)

    @staticmethod
    def create_friend_dict(undirected_graph):
        """
        This method takes undirected edges from a graph and creates a dictionary for each node
        with a list of nodes that it is connected with
        :param undirected_graph: a list of lists with the undirected edges of a graph
        :return: a dictionary of nodes with a list of the nodes they are connected to
        """
        network = dict()
        for element in undirected_graph:
            try:
                if element[0] not in network.keys():
                    network[element[0]] = set()
                network[element[0]].add(element[1])
            except IndexError:
                pass

        return network

    @staticmethod
    def save_network_to_file(network, file_name):
        with open(file_name, 'w') as fp:
            json.dump(network, fp)


if __name__ == '__main__':
    file = '/Users/aggrom/Desktop/MSDS/5_Data_mining/Assignment_1/friend-recommender/data/facebook_combined.txt'

    data_obj = DataFetcher(file)

    print('Initial graph - edges')
    pprint(data_obj.graph)
    print('-'*30)
    print('Undirected graph - edge')
    pprint(data_obj.undirected)
    print('-'*30)
    print('Undirected graph - dictionary')
    pprint(data_obj.network_dict)


