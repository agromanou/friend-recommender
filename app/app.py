from data_fetcher import DataFetcher
from recommendations import Recommendations


if __name__ == '__main__':

    file = '/Users/aggrom/Desktop/MSDS/5_Data_mining/Assignment_1/friend-recommender/data/facebook_combined.txt'
    percentages = []
    algo_list = ['common_neighbors', 'jaccard', 'adamic_adar', 'cosine']

    fetcher = DataFetcher(file)
    graph = fetcher.network_dict

    recommender = Recommendations(graph)

    recommender.compute_the_number_users_with_the_same_first_and_different_10_recommendations()

    percentages.append(recommender.compute_similarity_percentage('common_neighbors', 'jaccard'))
    percentages.append(recommender.compute_similarity_percentage('common_neighbors', 'adamic_adar'))
    percentages.append(recommender.compute_similarity_percentage('jaccard', 'adamic_adar'))
    percentages.append(recommender.compute_similarity_percentage('cosine', 'common_neighbors'))
    percentages.append(recommender.compute_similarity_percentage('cosine', 'jaccard'))
    percentages.append(recommender.compute_similarity_percentage('cosine', 'adamic_adar'))

    total = 0
    for percentage in percentages:
        total = total + percentage

    average_similarity = round((total/ len(percentages)), 2)
    print('The average similarity between the algorithms is: ' + str(average_similarity))
    
    recommender.evaluate_scoring_functions()
    
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
