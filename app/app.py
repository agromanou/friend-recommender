from data_fetcher import DataFetcher
from recommendations import Recommendations


if __name__ == '__main__':

    file = '/Users/aggrom/Desktop/MSDS/5_Data_mining/Assignment_1/friend-recommender/data/facebook_combined.txt'
    algo_list = ['common_neighbors', 'jaccard', 'adamic_adar', 'cosine']

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

    for algo in algo_list:
        print()
        print()
        print('Calculating {} score'.format(algo))
        recommender.find_recommendations(score=algo)
        print()
        print('Recommendations for node 107:')
        print(recommender.recommendations['107'])

        print('-'*10)
        print('Recommendations for node 1126:')
        print(recommender.recommendations['1126'])

        print('-'*10)
        print('Recommendations for node 14:')
        print(recommender.recommendations['14'])

        print('-'*10)
        print('Recommendations for node 35:')
        print(recommender.recommendations['35'])
