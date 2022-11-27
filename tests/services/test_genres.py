from unittest.mock import MagicMock
import pytest
from DAO.model.genre import Genre
from DAO.genre import GenreDAO
from service.genre import GenreService


@pytest.fixture()
def test_genres():
    d1 = Genre(id=1, name='Genre1')
    d2 = Genre(id=2, name='Genre2')
    d3 = Genre(id=3, name='Genre3')

    return {1: d1, 2: d2, 3: d3}


@pytest.fixture()
def genres_dao(test_genres):
    genres_d = GenreDAO(None)

    genres_d.get_one = MagicMock(side_effect=test_genres.get)
    genres_d.get_all = MagicMock(return_value=test_genres.values())
    genres_d.create = MagicMock(return_value=Genre(id=4))
    genres_d.update = MagicMock()
    genres_d.delete = MagicMock()

    return genres_d


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genres_dao):
        self.genre_service = GenreService(dao=genres_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        directors = self.genre_service.get_all()

        assert len(directors) > 0

    def test_create(self):
        genre_d = {"name": "Genre4"}

        genre = self.genre_service.create(genre_d)
        assert genre.id is not None

    def test_update(self):
        genre_d = {"name": "New Genre"}

        genre = self.genre_service.update(genre_d)
        assert genre.name is not None
        assert genre.id is not None

    def test_partially_update(self):
        genre_d = {"name": "New Genre"}
        genre = self.genre_service.update(genre_d)
        assert genre.name is not None

    def test_delete(self):
        self.genre_service.delete(1)
