#! /usr/bin/env python3
import recommendations
import codecs

def main():
    check_ids = find_similar_users()
    lens_data = recommendations.loadMovieLens()

    substitute_me = '645'
    find_favorite_movies(check_ids, lens_data)
    find_least_favorite_movies(check_ids, lens_data)
    find_correlated_users_subsitute(substitute_me, lens_data)
    find_least_correlated_users_subsitute(substitute_me, lens_data)
    get_top_recomendations(substitute_me,lens_data)
    get_worst_recomendations(substitute_me, lens_data)
    find_corerelated_films(lens_data)

def find_corerelated_films(data):
    favorite_film = "Schindler's List (1993)"
    least_film = 'Spice World (1997)'
    print('here')
    data_dict = recommendations.calculateSimilarItems(data)
    second_dict = recommendations.calculateNotSimilarItems(data)
    print(f'\n Films matching {favorite_film} are: ', data_dict[favorite_film], '\n')
    print(f'\n Films matching {favorite_film} are: ', second_dict[favorite_film], '\n')

    print(f'\n Films matching {least_film} are: ', second_dict[least_film], '\n')
    print(f'\n Films Not matching {least_film} are: ', data_dict[least_film], '\n')



def get_worst_recomendations(id, data):
    new_data = recommendations.getRecommendations(data, id)
    new_data.reverse()
    print('\n Worst Recommendation\n',new_data[0:5])

def get_top_recomendations(id,data):
    output = recommendations.getRecommendations(data, id)
    print('\n Top Recommendation\n',output[0:5])

def find_correlated_users_subsitute(id, lens_data):
    print('best matches: ')
    print(recommendations.topMatches(lens_data,id),"\n")

def find_least_correlated_users_subsitute(id, lens_data):
    print('worst matches: ')
    print(recommendations.worstMatches(lens_data, id))


def find_favorite_movies(ids, movie_db):
    print("Favorite Movies: \n")
    for each in ids:
        usr_movies = movie_db[each[0]]
        usr_movies = sorted(usr_movies.items(), key= lambda kv:(kv[1], kv[0]), reverse=True)
        print(f'user: {each}')
        for i in range(3):
            print(f'movie {i}: ',usr_movies[i][0])
        print('\n')

def find_least_favorite_movies(ids, movie_db):
    print("Least Favorite Movies: \n")
    for each in ids:
        usr_movies = movie_db[each[0]]
        usr_movies = sorted(usr_movies.items(), key= lambda kv:(kv[1], kv[0]))
        print(f'user: {each}')
        for i in range(3):
            print(f'movie {i}: ',usr_movies[i][0])
        print('\n')

def find_similar_users():
    user = {}
    #best_match = {}

    f = codecs.open("./ml-100k/u.user",'r',encoding='ISO-8859-1')
    score = 0
    #user['me'] = {'age':27, 'gender':'M', 'occupation':'programmer'}
    for line in f:

        (id, age, gender,occupation, zipcode) = line.split('|')
        if int(age) == 27:
            score += 1
        if gender == 'M':
            score += 1
        if occupation == 'programmer':
            score += 1
        user[id] = score
        score = 0

    best_match = sorted(user.items(), key= lambda kv:(kv[1], kv[0]), reverse=True)

    return best_match[0:5]

main()
