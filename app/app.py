from app.data_fetcher import DataFetcher
from app.recommendations import Recommendations


if __name__ == '__main__':

    file = '~/friend-recommender/data/facebook_combined.txt'

    fetcher = DataFetcher(file)
    graph = fetcher.network_dict

    recommender = Recommendations(graph)

    recommender.find_recommendations(score='common_neighbors')
    recommender.find_recommendations(score='jaccard')
    recommender.find_recommendations(score='adamic_adar')


