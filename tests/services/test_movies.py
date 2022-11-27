from unittest.mock import MagicMock
import pytest
from DAO.model.movie import Movie
from DAO.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def test_movies():
    m1 = Movie(id=1, title='Movie1', description='description1', trailer='trailer1', year=2000, rating=2.5)
    m2 = Movie(id=2, title='Movie2', description='description2', trailer='trailer2', year=2001, rating=3.5)
    m3 = Movie(id=3, title='Movie3', description='description3', trailer='trailer3', year=2003, rating=4.5)

    return {1: m1, 2: m2, 3: m3}


@pytest.fixture()
def movies_dao(test_movies):
    genres_d = MovieDAO(None)

    genres_d.get_one = MagicMock(side_effect=test_movies.get)
    genres_d.get_all = MagicMock(return_value=test_movies.values())
    genres_d.create = MagicMock()
    genres_d.update = MagicMock()
    genres_d.delete = MagicMock()

    return genres_d


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movies_dao):
        self.movie_service = MovieService(dao=movies_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert movies is not None
        assert len(movies) > 0, "Список фильмов не должен быть пустым"

    def test_create(self):
        movie_d = {'title': 'Movie3',
                   'description': 'description3',
                   'trailer': 'trailer3',
                   'year': 2003,
                   'rating': 4.5
                   }

        movie = self.movie_service.create(movie_d)
        assert movie.id is not None
        assert movie.title is not None


    def test_update(self):
        movie_d = {"title": "New Movie"}

        movie = self.movie_service.update(movie_d)
        assert movie.name is not None
        assert movie.id is not None

    def test_partially_update(self):
        movie_d = {"title": "New Movie"}
        movie = self.movie_service.update(movie_d)
        assert movie.name is not None

    def test_delete(self):
        assert self.movie_service.delete(1) is None
