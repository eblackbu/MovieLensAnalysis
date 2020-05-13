from collections import OrderedDict
import pytest
from movielens_analysis import Ratings, Tags, Movies, Links

# to check if the methods return the correct data types
# -----------------------------------------------------

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

# to check if the returned values are sorted
# -----------------------------------------------------

def check_sort_data(data_list, sort_type=1, data_type=1):
	if len(data_list) == 0:
		return True
	value_prev = data_list[0]
	for value in data_list:
		if value_prev > value and sort_type == 1 or \
			value_prev < value and sort_type != 1:
			return False
		value_prev = value
	return True

def check_sort_data_by_len(data_list, sort_type=1):
	if (len(list(data_list))) == 0:
		return True
	value_prev = len(data_list[0])
	for word in data_list:
		if value_prev > len(word) and sort_type == 1 or \
			value_prev < len(word) and sort_type != 1:
			return False
		value_prev = len(word)
	return True


@pytest.mark.parametrize('ratings_file_name', ['ratings.csv'])
@pytest.mark.parametrize('n', [10])
def test_ratings_class_sorted_error(ratings_file_name, n):
	parent_class = Ratings(ratings_file_name)
	movies_class = parent_class.Movies(parent_class)
	users_class = parent_class.Users(parent_class)
	if not check_sort_data(list(movies_class.dist_by_year().keys())):
		assert False
	if not check_sort_data(list(movies_class.dist_by_rating().keys())):
		assert False
	if not check_sort_data(list(movies_class.top_by_num_of_ratings(n).values()), sort_type=2):
		assert False
	if not check_sort_data(list(movies_class.top_by_ratings(n).values()), sort_type=2):
		assert False
	if not check_sort_data(list(movies_class.top_controversial(n).values()), sort_type=2):
		assert False
	assert True

@pytest.mark.parametrize('tags_file_name', ['tags.csv'])
@pytest.mark.parametrize('n', [10])
@pytest.mark.parametrize('word', ['Osc'])
def test_tags_class_sorted_error(tags_file_name, n, word):
	tags_class = Tags(tags_file_name)
	if not check_sort_data(list(tags_class.most_words(n).values()), sort_type=2):
		assert False
	if not check_sort_data_by_len(tags_class.longest(n), sort_type=2):
		assert False
	if not check_sort_data(list(tags_class.most_popular(n).values()), sort_type=2):
		assert False
	if not check_sort_data(tags_class.tags_with(word)):
		assert False
	assert True

@pytest.mark.parametrize('movies_file_name', ['movies.csv'])
@pytest.mark.parametrize('n', [10])
def test_movies_class_sorted_error(movies_file_name, n):
	movies_class = Movies(movies_file_name)
	if not check_sort_data(list(movies_class.dist_by_release().values()), sort_type=2):
		assert False
	if not check_sort_data_by_len(list(movies_class.dist_by_genres().values()), sort_type=2):
		assert False
	if not check_sort_data(list(movies_class.most_genres(n).values()), sort_type=2):
		assert False
	assert True

@pytest.mark.parametrize('links_file_name', ['links.csv'])
@pytest.mark.parametrize('n', [10])
@pytest.mark.parametrize('list_of_fields', [['', '', '' '',]])
def test_movies_class_sorted_error(links_file_name, n, list_of_fields):
	links_class = Links(links_file_name)
	# todo: get_imdb() возвращает список списков, нужно сортировать по первому подэлементу - проверить!!!
	if not check_sort_data(links_class.get_imdb(list_of_fields), sort_type=2):
		assert False
	if not check_sort_data_by_len(list(links_class.top_directors(n).values()), sort_type=2):
		assert False
	if not check_sort_data(list(links_class.most_expensive(n).values()), sort_type=2):
		assert False
	if not check_sort_data(list(links_class.most_profitable(n).values()), sort_type=2):
		assert False
	if not check_sort_data(list(links_class.longest(n).values()), sort_type=2):
		assert False
	if not check_sort_data(list(links_class.top_cost_per_minute(n).values()), sort_type=2):
		assert False
	assert True

# to check if the list are corrected
# -----------------------------------------------------

## User - что возвращает?

def check_correct_data_type(data_list, data_type):
	if len(data_list) == 0:
		return True
	for value in data_list:
		if not isinstance(value, data_type):
			return False
	return True

@pytest.mark.parametrize('tags_file_name', ['tags.csv'])
@pytest.mark.parametrize('n', [10])
@pytest.mark.parametrize('word', ['Osc'])
def test_tags_class_correct_list_error(tags_file_name, n, word):
	tags_class = Tags(tags_file_name)
	if not check_correct_data_type(tags_class.longest(n), int):
		assert False
	if not check_correct_data_type(tags_class.most_words_and_longest(n), int):
		assert False
	if not check_correct_data_type(tags_class.tags_with(word), str):
		assert False
	assert True

@pytest.mark.parametrize('links_file_name', ['links.csv'])
@pytest.mark.parametrize('n', [10])
@pytest.mark.parametrize('list_of_fields', [['', '', '' '',]])
def test_movies_class_correct_list_error(links_file_name, n, list_of_fields):
	links_class = Links(links_file_name)
	if not check_sort_data(links_class.get_imdb(list_of_fields), list):
		assert False

	assert True
