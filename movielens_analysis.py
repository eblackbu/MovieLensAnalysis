import os
import sys
import collections
import requests
import bs4
import re


class Ratings(object):
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, spath):
        def get_generator_list_lines(file_name):
            with open(file_name, 'r') as f:
                f.readline()
                for line in f:
                    yield line
                    
        try:
            self.data = []
            for line in get_generator_list_lines(spath):
                self.data.append([x for x in line.split(',')])
        except IOError:
            print(f"There is no file {spath}")
        except Exception:
            print(sys.info())

    class Movies(object):
        def __init__(self, path, ratings):
            
            def get_generator_list_lines(file_name):
                with open(file_name, 'r') as f:
                    f.readline()
                    for line in f:
                        yield line
                        
            self.ratings = ratings
            try:
                self.movies = {}
                for line in get_generator_list_lines(path):
                    self.movies[line[:line.index(',')]] = line[line.index(',') + 1:line.rindex(',')]
            except IOError:
                print(f"There is no file {path}")
            except Exception:
                print(sys.int_info)

        def dist_by_year(self):
            """
            This method returns a dict where the keys are years and the values are counts.
            Sorted by years ascendigly.
            """
            ratings_by_year = collections.Counter([int(record[3]) // 31536000 + 1970 for record in self.ratings.data])
            return collections.OrderedDict(ratings_by_year.most_common())

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sorted by ratings ascendingly.
            """
            ratings_distribution = collections.Counter([record[2] for record in self.ratings.data]).most_common()
            return collections.OrderedDict(sorted(list(ratings_distribution), key=lambda x: x[0]))

        def top_by_num_of_ratings(self, n):
            """
            The method returns top n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
            Sorted by numbers descendingly.
            """
            top_movies = collections.Counter([record[1] for record in self.ratings.data]).most_common(n)
            ordered_top_movies = []
            for x in top_movies:
                try:
                    ordered_top_movies.append((self.movies[x[0]], x[1]))
                except KeyError:
                    continue
            #top_movies = collections.OrderedDict(map(lambda x: (self.movies[x[0]], x[1]), top_movies))
            return collections.OrderedDict(ordered_top_movies)

        def top_by_ratings(self, n, metric="average"):
            """
            The method returns top n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sorted by metric descendingly.
            """
            dist_movies = {}
            for x in self.ratings.data:
                try:
                    dist_movies[self.movies[x[1]]] = dist_movies.setdefault(self.movies[x[1]], []) + [float(x[2])]
                except KeyError:
                    continue

            if metric == "average":
                average_ratings = sorted(map(lambda x: (x[0], sum(x[1]) / len(x[1])), dist_movies.items()),
                                         key=lambda y: -y[1])[:n]
                return collections.OrderedDict(average_ratings)
            else:

                def get_median(x: list):
                    if len(x) % 2:
                        return x[len(x) // 2]
                    else:
                        return (x[len(x) // 2] + x[(len(x) + 1) // 2]) / 2

                median_ratings = sorted(list(map(lambda x: (x[0], get_median(x[1])), dict(
                    map(lambda x: (x[0], list(sorted(x[1]))), dist_movies.items())).items())), key=lambda x: -x[1])[:n]
                return collections.OrderedDict(median_ratings)

        def top_controversial(self, n):
            """
            The method returns top n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are variances.
            Sorted by variances descendingly.
            """

            def get_variance(ratings: list):
                mean = sum(ratings) / len(ratings)
                if len(ratings) > 1:
                    return sum(map(lambda x: (x - mean) * (x - mean), ratings)) / (len(ratings) - 1)
                else:
                    return ratings[0]

            dist_movies = {}
            for x in self.ratings.data:
                try:
                    dist_movies[self.movies[x[1]]] = dist_movies.setdefault(self.movies[x[1]], []) + [float(x[2])]
                except KeyError:
                    continue
            movie_variances = sorted(map(lambda x: (x[0], get_variance(x[1])), dist_movies.items()),
                                         key=lambda y: -y[1])[:n]
            return collections.OrderedDict(movie_variances)

    class Users(object):
        def __init__(self, ratings):
            self.ratings = ratings

        def top_valuers(self):
            """
            The method returns the distribution of users by the number of ratings made by them.
            It is a dict where the keys are users and the values are number of ratings
            Sorted by descending order
            """
            valuers = collections.Counter(map(lambda x: x[0], self.ratings.data)).most_common()
            return collections.OrderedDict(valuers)

        def valuers_with_ratings(self, metric="average"):
            """
            The method returns the distribution of users by average or median ratings made by them.
            It is a dict where the keys are users and the values are metric values.
            Sorted by descending order
            """
            dist_valuers = {}
            for x in self.ratings.data:
                dist_valuers[x[0]] = dist_valuers.setdefault(x[0], []) + [float(x[2])]

            if metric == "average":
                average_ratings = sorted(map(lambda x: (x[0], sum(x[1]) / len(x[1])), dist_valuers.items()), key=lambda y: -y[1])
                return collections.OrderedDict(average_ratings)
            else:

                def get_median(x: list):
                    if len(x) % 2:
                        return x[len(x) // 2]
                    else:
                        return (x[len(x) // 2] + x[(len(x) + 1) // 2]) / 2

                median_ratings = sorted(list(map(lambda x: (x[0], get_median(x[1])), dict(map(lambda x: (x[0], list(sorted(x[1]))), dist_valuers.items())).items())), key=lambda x: -x[1])
                return collections.OrderedDict(median_ratings)

        def top_controversial_valuers(self, n):
            """
            The method returns top n users with the biggest variance of their ratings.
            It is a dict where the keys are users and the values are variances
            Sorted by descending order
            """

            def get_variance(ratings: list):
                mean = sum(ratings) / len(ratings)
                if len(ratings) > 1:
                    return sum(map(lambda x: (x - mean) * (x - mean), ratings)) / (len(ratings) - 1)
                else:
                    return ratings[0]

            dist_movies = {}
            for x in self.ratings.data:
                dist_movies[x[0]] = dist_movies.setdefault(x[0], []) + [float(x[2])]
            movie_variances = sorted(map(lambda x: (x[0], get_variance(x[1])), dist_movies.items()),
                                     key=lambda y: -y[1])[:n]
            return collections.OrderedDict(movie_variances)


class Tags(object):
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path):
        try:
            self.data = []
            with open(path, "r") as tags_file:
                tags_file.readline()
                for line in tags_file:
                    self.data.append([x for x in line.split(',')])
        except IOError:
            print(f"There is no file {path}")
        except Exception:
            print(sys.info())

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
        where the keys are tags and the values are the number of words inside the tag.
        Sort it by numbers descendingly.
        """
        big_tags = [[x[2], len(x[2].split(' '))] for x in self.data]
        big_tags = sorted(big_tags, key=lambda x: -int(x[1]))[:n]
        return collections.OrderedDict(big_tags)

    def longest(self, n):
        """
        The method returns top n longest tags in terms of the number of characters.
        It is a list of the tags. Sort it by numbers descendingly.
        """
        big_tags = set(map(lambda x: x[2], self.data))
        big_tags = sorted(big_tags, key=lambda x: -len(x))[:n]
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top n tags with most words inside and top n longest tags in terms of the number of characters.
        It is a list of the tags.
        """
        longest_tags = list(sorted(set(map(lambda x: x[2], self.data)), key=lambda x: -len(x)))[:n]
        most_words_tags = list(self.most_words(n))[:n]
        return list(set(longest_tags) & set(most_words_tags))

    def most_popular(self, n) -> collections.OrderedDict:
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Sorted by counts in descending order
        """
        popular_tags = collections.Counter(map(lambda x: x[2], self.data))
        return collections.OrderedDict(popular_tags.most_common(n))

    def tags_with(self, word) -> list:
        """
        The method returns all the tags that include the word given as the argument.
        It is a list of the tags.
        Sorted by tag name alphabetically.
        """
        tags_with_word = list(map(lambda x: x[2], filter(lambda x: word in x[2], self.data)))
        tags_with_word.sort()
        return list(set(tags_with_word))


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path):
        def get_replaced_line(line, sep_old, sep_new, beg_count, end_count):
            words = line.split(sep_old)
            l_new = ""
            for w_count in range(len(words)):
                l_new += words[w_count]
                if w_count != len(words) - 1:
                    if (w_count < beg_count) or (w_count + 1 >= len(words) - end_count):
                        l_new += sep_new
                    else:
                        l_new += sep_old
            return l_new

        def get_generator_list_lines(file_name):
            with open(file_name, 'r') as f:
                f.readline()
                for line in f:
                    yield line

        try:
            self.data = []
            for line in get_generator_list_lines(path):
                ss = get_replaced_line(line, ',', '\t', 1, 1)
                new_elem = list(map(lambda x: x, ss.split('\t')))
                new_elem[2] = list(map(lambda x: x.strip(), new_elem[2].split('|')))
                self.data.append(new_elem)
        except IOError:
            print(f"There is no file {path}")
        except Exception:
            print(sys.int_info)

    def dist_by_release(self):
        """
        The method returns a dict where the keys are years and the values are counts.
        Sorted by counts in descending order.
        """
        release_years = []
        for x in self.data:
            try:
                release_years.append(re.search(r'\((\d{4})\)', x[1]).group(1))
            except:
                release_years.append('(year not specified)')
        return collections.OrderedDict(collections.Counter(release_years).most_common(len(release_years)))

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sorted by counts descendingly.
        """
        genres = {}
        for record in self.data:
            for genre in record[2]:
                genres[genre] = genres.setdefault(genre, 0) + 1
        tmp_genres = [[x, genres[x]] for x in genres]
        tmp_genres.sort(key=lambda x: -int(x[1]))
        return collections.OrderedDict(tmp_genres)

    def most_genres(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        movies = [[x[1], len(x[2])] for x in self.data]
        movies = sorted(movies, key=lambda elem: -int(elem[1]))[:n]
        return collections.OrderedDict(movies)


class Links:
    """
    Analyzing data from Links.csv
    """

    def __init__(self, path):

        def generate_line(path):
            with open(path, "r") as links_file:
                links_file.readline()
                for line in links_file:
                    yield line

        try:
            self.data = []
            for line in generate_line(path):
                movie_id, imdb_id, unused = line.split(',')
                req = requests.get(f'http://imdb.com/title/tt{imdb_id}/')
                soup = bs4.BeautifulSoup(req.text, 'html.parser')
                details = soup.find("div", attrs={"id": "titleDetails"})
                title = soup.find("div", attrs={"class": "title_wrapper"}).find("h1").text
                try:
                    director = soup.find("div", attrs={"class": "rec-jaw-lower"}).find("div", attrs={
                        "class": "rec-director"}).text
                except AttributeError:
                    director = ''
                try:
                    budget = str(details.find("h4", text=re.compile('Budget:'), attrs={"class": "inline"}).next_sibling)
                except AttributeError:
                    budget = '0'
                try:
                    gross = str(details.find("h4", text=re.compile('Cumulative Worldwide Gross:'),
                                             attrs={"class": "inline"}).next_sibling)
                except AttributeError:
                    gross = '0'
                try:
                    runtime = details.find("h4", text=re.compile('Runtime:'), attrs={"class": "inline"}).findParent().find(
                        "time").text
                except AttributeError:
                    runtime = '1 min'
                self.data.append([movie_id,
                                  title[:title.find('\xa0')],
                                  director[director.rfind('\n'):].strip(),
                                  budget[budget.find('$') + 1:].replace(',', '').strip(),
                                  gross[gross.find('$') + 1:].replace(',', '').strip(),
                                  runtime])
        except IOError:
            print("file error")

    def get_imdb(self):
        """
        The method returns a lst of lists with fields:
        [movieId, movie Title, Director, Budget, Cumulative Worldwide Gross, Runtime]
        Sorted by movieId
        """
        return list(sorted(self.data, key=lambda x: int(x[0])))

    def top_directors(self, n):
        """
        The method returns a dict where the keys are directors and the values are numbers movies created by them
        Sorted by numbers in descending order.
        """
        directors = collections.Counter(map(lambda x: x[2], self.data))
        return collections.OrderedDict(directors.most_common(n))

    def most_expensive(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are their budgets.
        Sorted by budgets in descending order.
        """
        budgets = collections.OrderedDict({x[1]: x[3] for x in sorted(self.data, key=lambda x: -int(x[3]))[:n]})
        return budgets

    def most_profitable(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are their budgets.
        Sorted by budgets in descending order.
        """
        profits = collections.OrderedDict({x[1]: int(x[4]) - int(x[3]) for x in sorted(self.data, key=lambda x: int(x[3]) - int(x[4]))[:n]})
        return profits

    def longest(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are their runtime.
        Sorted by runtime in descending order.
        """
        a = self.data[0][5][:self.data[0][5].find(' ')]
        runtimes = collections.OrderedDict({x[1]: x[5] for x in sorted(self.data, key=lambda x: -int(x[5][:-4]))[:n]})
        return runtimes

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are the budgets divided by their runtime.
        Sorted by the division in descending order.
        """
        costs = collections.OrderedDict({x[1]: int(x[3]) / int(x[5][:-4]) for x in
                 sorted(self.data, key=lambda x: -(int(x[3]) / int(x[5][:-4])))[:n]})
        return costs


if __name__ == "__main__":
   print("All is OK!") 
