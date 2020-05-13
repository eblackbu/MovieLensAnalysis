import os
import collections
import re
import requests
import bs4


class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, path):
        try:
            self.data = []
            with open(path, "r") as ratings_file:
                ratings_file.readline()
                for line in ratings_file:
                    self.data.append([x for x in line.split(',')])  # поставить генератор
        except IOError:
            print(f"There is no file {path}")

    class Movies:
        def __init__(self, outer):
            self.outer = outer

        def dist_by_year(self):
            """
            This method returns a dict where the keys are years and the values are counts.
            Sorted by years in ascending order.
            """
            ratings_by_year = collections.Counter([int(record[3]) // 31536000 + 1970 for record in self.outer.data])
            return dict(ratings_by_year.most_common())

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sorted by ratings in ascending order.
            """
            ratings_distribution = collections.Counter([record[2] for record in self.outer.data])
            return dict(ratings_distribution)

        def top_by_num_ratings(self, n):
            """
            The method returns top n movies by the number of ratings.
            It is a dict where the keys are movie and the values are numbers.
            Sorted by numbers in descending order.
            """
            top_movies = collections.Counter([record[1] for record in self.outer.data])
            return dict(top_movies.most_common(n))

        def top_by_ratings(self, n, metric="average"):
            """
            The method returns top n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sorted by metric in descending order.
            """
            pass

        def top_controversial(self, n):
            """
            The method returns top n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are variances.
            Sorted by variances in descending order.
            """

            def get_variance(movie_id):
                movie_ratings = [float(x[2]) for x in list(filter(lambda x: x[1] == movie_id, self.outer.data))]
                mean = sum(movie_ratings) / len(movie_ratings)
                return sum([(x - mean) ** 2 for x in movie_ratings]) / len(movie_ratings)

            set_movies = set(map(lambda x: x[1], self.outer.data))
            top_movies = collections.Counter({movie: get_variance(movie) for movie in set_movies})
            return dict(top_movies.most_common(n))

    class Users:
        def __init__(self, outer):
            self.outer = outer

        def top_valuers(self):
            """
            The method returns the distribution of users by the number of ratings made by them.
            It is a dict where the keys are users and the values are number of ratings
            """
            valuers = collections.Counter(map(lambda x: x[0], self.outer.data))
            return dict(valuers)

        def valuers_with_ratings(self, metric="average"):
            """
            The method returns the distribution of users by average or median ratings made by them.
            It is a dict where the keys are users and the values are metric values.
            """

            pass

        def top_controversial_valuers(self, n):
            """
            The method returns top n users with the biggest variance of their ratings.
            It is a dict where the keys are users and the values are variances
            """

            def get_variance(user_id):
                user_ratings = [float(x[2]) for x in list(filter(lambda x: x[0] == user_id, self.outer.data))]
                mean = sum(user_ratings) / len(user_ratings)
                return sum([(x - mean) ** 2 for x in user_ratings]) / len(user_ratings)

            set_users = set(map(lambda x: x[0], self.outer.data))
            top_users = collections.Counter({user: get_variance(user) for user in set_users})
            return dict(top_users.most_common(n))


class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path):
        pass

    def most_words(self, ):
        """
        The method returns top n tags with words inside.
        It is a dict where the keys are tags and the values re the number of words inside the tag.
        Sorted by numbers in descending order.
        """
        pass

    def longest(self, n):
        """
        The method returns top n longest tags in terms of the number of characters.
        It is a list of the tags. Sort it by numbers in descending order.
        """
        pass

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top n tags with most words inside and top n longest tags in terms of the number of characters.
        It is a liist of the tags.
        """
        pass

    def tags_with(self, word):
        """
        The method returns all the tags that include the word given as the argument.
        It is a list of the tags.
        Sorted by tag name alphabetically.
        """
        pass


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path):
        try:
            with open(path, "r") as tags_file:
                self.data = []
                tags_file.readline()
                for line in tags_file:
                    new_elem = list(map(lambda x: x, line.split(',')))
                    new_elem[2] = list(map(lambda x: x, new_elem[2][:-1].split('|')))
                    self.data.append(new_elem)
        except IOError:
            print("file error")

    def dist_by_release(self):
        release_years = collections.Counter(map(lambda x: re.search(r'\(\d{4}\)', x[1]), self.data))
        return dict(release_years.most_common(len(release_years)))

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sorted by counts in descending order.
        """
        pass

    def most_genres(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        pass


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
                runtime = details.find("h4", text=re.compile('Runtime:'), attrs={"class": "inline"}).findParent().find(
                    "time").text
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
        self.data.sort(key=lambda x:x[0])
        return self.data

    def top_directors(self, n):
        """
        The method returns a dict where the keys are directors and the values are numbers movies created by them
        Sorted by numbers in descending order.
        """
        directors = collections.Counter(map(lambda x: x[2], self.data))
        return dict(directors.most_common(n))

    def most_expensive(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are their budgets.
        Sorted by budgets in descending order.
        """
        budgets = {x[1]: x[3] for x in sorted(self.data, key=lambda x: -int(x[3]))[:n]}
        return budgets

    def most_profitable(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are their budgets.
        Sorted by budgets in descending order.
        """
        profits = {x[1]: int(x[4]) - int(x[3]) for x in sorted(self.data, key=lambda x: int(x[3])-int(x[4]))[:n]}
        return profits

    def longest(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are their runtime.
        Sorted by runtime in descending order.
        """
        a = self.data[0][5][:self.data[0][5].find(' ')]
        runtimes = {x[1]: x[5] for x in sorted(self.data, key=lambda x: -int(x[5][:-4]))[:n]}
        return runtimes

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top n movies where the keys are movie titles and the values are the budgets divided by their runtime.
        Sorted by the division in descending order.
        """
        costs = {x[1]: int(x[3]) / int(x[5][:-4]) for x in sorted(self.data, key=lambda x: -(int(x[3]) / int(x[5][:-4])))[:n]}
        return costs


if __name__ == "__main__":
    """
    test = Ratings("test.csv")
    m = test.Movies(test)
    u = test.Users(test)
    print(m.dist_by_year())
    print(m.dist_by_rating())
    print(m.top_by_num_ratings(5))
    print(m.top_controversial(5))
    print(u.top_valuers())
    print(u.top_controversial_valuers(5))
    """

    test = Links("test_links.csv")
    #print(test.get_imdb())
    #print(test.top_directors(5))
    print(test.most_expensive(5))
    print(test.most_profitable(5))
    print(test.longest(5))
    print(test.top_cost_per_minute(5))

