from data_fetcher import DataFetcher
from recommendations import Recommendations


if __name__ == '__main__':

    file = '/Users/aggrom/Desktop/MSDS/5_Data_mining/Assignment_1/friend-recommender/data/facebook_combined.txt'

    fetcher = DataFetcher(file)
    graph = fetcher.network_dict

    recommender = Recommendations(graph)

    t = recommender.run_algorithm('100', 'common_neighbors')
    top_ten_friends = t[:10] if len(t) > 10 else t
    to_compare = dict()
    to_compare['100'] = set()

    if len(top_ten_friends) > 0:
        for item in top_ten_friends:
            print(item)
            to_compare['100'].add(item[0])

    recommender.find_recommendations(score='common_neighbors')
    recommender.find_recommendations(score='jaccard')
    recommender.find_recommendations(score='adamic_adar')


