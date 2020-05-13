from collections import OrderedDict
import pytest
from movielens_analysis import Ratings, Tags, Movies, Links

# to check if the methods return the correct data types
@pytest.mark.parametrize('ratings_file_name', ['ratings.csv'])
@pytest.mark.parametrize('n', [10])
#@pytest.mark.parametrize('ret_type', [[dict, dict, dict, dict, dict, dict, dict, dict]])
@pytest.mark.parametrize('ret_type', [[OrderedDict, OrderedDict, OrderedDict, OrderedDict, OrderedDict, OrderedDict, OrderedDict, OrderedDict]])
def test_ratings_class_type_error(ratings_file_name, n, ret_type):
	parent_class = Ratings(ratings_file_name)
	movies_class = parent_class.Movies(parent_class)
	users_class = parent_class.Users(parent_class)
	method_ret_list = []
	method_ret_list.append(type(movies_class.dist_by_year()))
	method_ret_list.append(type(movies_class.dist_by_rating()))
	method_ret_list.append(type(movies_class.top_by_num_of_ratings(n)))
	method_ret_list.append(type(movies_class.top_by_ratings(n)))
	method_ret_list.append(type(movies_class.top_controversial(n)))
	method_ret_list.append(type(users_class.top_valuers()))
	method_ret_list.append(type(users_class.valuers_with_ratings()))
	method_ret_list.append(type(users_class.top_controversial_valuers(n)))
#	print(method_ret_list)
	assert len(set(method_ret_list) ^ set(ret_type)) == 0

@pytest.mark.parametrize('tags_file_name', ['tags.csv'])
@pytest.mark.parametrize('n', [10])
@pytest.mark.parametrize('word', ['Ost'])
#@pytest.mark.parametrize('ret_type', [[dict, list, list, list]])
@pytest.mark.parametrize('ret_type', [[OrderedDict, list, list, OrderedDict, list]])
def test_tags_class_type_error(tags_file_name, n, word, ret_type):
	parent_class = Tags(tags_file_name)
	method_ret_list = []
	method_ret_list.append(type(parent_class.most_words(n)))
	method_ret_list.append(type(parent_class.longest(n)))
	method_ret_list.append(type(parent_class.most_words_and_longest(n)))
	method_ret_list.append(type(parent_class.most_popular(n)))
	method_ret_list.append(type(parent_class.tags_with(word)))
	print(method_ret_list)
	assert len(set(method_ret_list) ^ set(ret_type)) == 0

"""
@pytest.mark.parametrize('movies_file_name', ['movies.csv'])
@pytest.mark.parametrize('n', [10])
#@pytest.mark.parametrize('ret_type', [[dict, dict, dict]])
@pytest.mark.parametrize('ret_type', [[OrderedDict, OrderedDict, OrderedDict]])
def test_movies_class_type_error(movies_file_name, n, ret_type):
	movies_class = Movies(movies_file_name)
	method_ret_list = []
	method_ret_list.append(type(movies_class.dist_by_release()))
	method_ret_list.append(type(movies_class.dist_by_genres()))
	method_ret_list.append(type(movies_class.most_genres(n)))
	print(method_ret_list)
	assert len(set(method_ret_list) ^ set(ret_type)) == 0

@pytest.mark.parametrize('links_file_name', ['links.csv'])
@pytest.mark.parametrize('list_of_fields', ['movieId', 'field1', 'field2', 'field3'])
@pytest.mark.parametrize('n', [10])
@pytest.mark.parametrize('ret_type', [[list, dict, dict, dict, dict, dict]])
#@pytest.mark.parametrize('ret_type', [[list, OrderedDict, OrderedDict, OrderedDict, OrderedDict, OrderedDict]])
def test_links_class_type_error(links_file_name, list_of_fields, n, ret_type):
	links_class = Links(links_file_name)
	method_ret_list = []
	method_ret_list.append(type(links_class.get_imdb(list_of_fields)))
	method_ret_list.append(type(links_class.top_directors(n)))
	method_ret_list.append(type(links_class.most_expensive(n)))
	method_ret_list.append(type(links_class.most_profitable(n)))
	method_ret_list.append(type(links_class.longest(n)))
	method_ret_list.append(type(links_class.top_cost_per_minute(n)))
#	print(method_ret_list)
	assert len(set(method_ret_list) ^ set(ret_type)) == 0
"""
