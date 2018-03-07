class DataFetcher:
    def __init__(self):
        pass

    def load_data(self):
        pass

    @staticmethod
    def create_undirected_graph(directed_graph):
        """
        It transforms a directed graph into an undirected one.
        :param directed_graph: list of tuples with the directed graph
        :return: list of tuples with the undirected graph
        """
        undirected_graph = directed_graph
        for directed_edge in undirected_graph:
            undirected_edge = [directed_edge[1], directed_edge[0]]
            if undirected_edge not in graph:
                undirected_graph.append(undirected_edge)

        return undirected_graph


if __name__ == '__main__':
    graph = [(1, 0),
             (2, 3),
             (3, 1),
             (3, 0),
             (3, 4),
             (4, 5),
             (4, 6),
             (5, 4),
             (5, 6)]

    un_graph = DataFetcher.create_undirected_graph(graph)
    print(un_graph)
