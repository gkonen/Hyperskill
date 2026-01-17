
from typing import Literal

class Movie:
    def __init__(self, title: str, rating: float):
        self.title: str = title
        self.rating: float = rating

    def __str__(self):
        return f"{self.title} - {self.rating}"

    def __lt__(self, other):
        return self.rating < other.rating

    def __gt__(self, other):
        return self.rating > other.rating

    def __le__(self, other):
        return self.rating <= other.rating

    def __ge__(self, other):
        return self.rating >= other.rating

class MovieCollection:

    def __init__(self, movies: list[Movie] ):
        self.movies: list[Movie] = movies

    @staticmethod
    def from_csv(path: str) -> "MovieCollection":
        list_movie = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line:
                    try:
                        title, rating = line.strip().rsplit(",", 1)
                        title = title.strip('"')
                    except ValueError:
                        print(line)
                    else:
                        list_movie.append(Movie(title, float(rating)))
        return MovieCollection(list_movie)

    def linear_search(self, rating: float) -> "MovieCollection":
        searched_movies = []
        for movie in self.movies:
            if movie.rating == rating:
                searched_movies.append(movie)
        return MovieCollection(searched_movies)

    def binary_search_boundary(self, rating: float, bound : Literal["start", "end"]):
        low = 0
        high = len(self.movies) - 1
        index_first = -1
        step = 0
        while low <= high:
            middle = (low + high) // 2
            middle_movie = self.movies[middle]
            if middle_movie.rating == rating:
                index_first = middle
                match bound:
                    case "start":
                        high = middle - 1
                    case "end":
                        low = middle + 1
            elif middle_movie.rating > rating:
                high = middle - 1
            else:
                low = middle + 1
            step += 1
        return index_first

    def binary_search(self, rating: float) -> "MovieCollection":
        start = self.binary_search_boundary(rating, bound="start")
        end = self.binary_search_boundary(rating, bound="end")
        return MovieCollection(self.movies[start:end+1])


    def bubblesort(self):
        n = len(self.movies)
        for _ in range(n):
            for ind_a in range(n-1):
                ind_b = ind_a + 1
                movie_a, movie_b = self.movies[ind_a], self.movies[ind_b]
                if movie_a > movie_b:
                    self.movies[ind_a], self.movies[ind_b] = movie_b, movie_a

    def __merge(self, left: list[Movie], right: list[Movie]) -> list[Movie]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def __mergesort(self, collection: list[Movie]):
        if len(collection) <= 1:
            return collection
        else:
            middle = len(collection) // 2
            sorted_right = self.__mergesort(collection[middle:])
            sorted_left = self.__mergesort(collection[:middle])

            return self.__merge(sorted_left, sorted_right)

    def sort_by_merge(self):
        sorted_movies = self.__mergesort(self.movies)
        self.movies = sorted_movies

    def __str__(self):
        return "\n".join(str(movie) for movie in self.movies)

if __name__ == "__main__":
    show_time = False
    collection = MovieCollection.from_csv("movies.csv")

    collection.sort_by_merge()
    print(collection.binary_search(6))
