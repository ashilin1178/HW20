from unittest.mock import MagicMock
import pytest
from DAO.model.director import Director
from DAO.director import DirectorDAO
from service.director import DirectorService


@pytest.fixture()
def test_directors():
    d1 = Director(id=1, name='John')
    d2 = Director(id=2, name='Tom')
    d3 = Director(id=3, name='Kate')

    return {1: d1, 2: d2, 3: d3}


@pytest.fixture()
def directors_dao(test_directors):
    directors_d = DirectorDAO(None)

    directors_d.get_one = MagicMock(side_effect=test_directors.get)
    directors_d.get_all = MagicMock(return_value=test_directors.values())
    directors_d.create = MagicMock(return_value=Director(id=4))
    directors_d.update = MagicMock(return_value=Director(id=4, name='Dave'))
    directors_d.delete = MagicMock(return_value=None)

    return directors_d


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, directors_dao):
        self.director_service = DirectorService(dao=directors_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) > 0

    def test_create(self):
        director_d = {"name": "Pit"}

        director = self.director_service.create(director_d)
        assert director.id is not None

    def test_update(self):
        director_d = {"name": "Pit"}

        director = self.director_service.update(director_d)
        assert director.name is not None
        assert director.id is not None

    def test_partially_update(self):
        director_d = {"name": "Pit"}
        director = self.director_service.update(director_d)
        assert director.name is not None

    def test_delete(self):
        assert self.director_service.delete(1) is None
