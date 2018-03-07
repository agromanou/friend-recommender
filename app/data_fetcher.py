from pprint import pprint


class DataFetcher:
    def __init__(self):
        self.graph = self.load_data()
        self.network_dict = self.create_friend_dict(self.create_undirected_graph(self.graph))

    @staticmethod
    def load_data():
        graph = [[1, 0],
                 [2, 3],
                 [3, 1],
                 [3, 0],
                 [3, 4],
                 [4, 5],
                 [4, 6],
                 [5, 4],
                 [5, 6]]

        return graph

    @staticmethod
    def create_undirected_graph(directed_graph):
        """
        It transforms a directed graph into an undirected one.
        :param directed_graph: list of lists with the directed graph
        :return: list of tuples with the undirected graph
        """
        undirected_graph = directed_graph
        for directed_edge in undirected_graph:
            undirected_edge = [directed_edge[1], directed_edge[0]]
            if undirected_edge not in undirected_graph:
                undirected_graph.append(undirected_edge)

        return undirected_graph

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
            if element[0] not in network.keys():
                network[element[0]] = list()
            network[element[0]].append(element[1])

        return network


if __name__ == '__main__':
    data_obj = DataFetcher()
    pprint(data_obj.network_dict)
