from unittest.mock import MagicMock

import pytest as pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    g_dao = GenreDAO(None)
    g1 = Genre(id=1, name='fantastic')
    g2 = Genre(id=2, name='horror')
    g3 = Genre(id=3, name='xxx')

    g_dao.get_one = MagicMock(return_value=g1)
    g_dao.get_all = MagicMock(return_value=[g1, g2, g3])
    g_dao.create = MagicMock(return_value=Genre(id=1))
    g_dao.delete = MagicMock()
    g_dao.update = MagicMock()
    return g_dao


class TestGenreService():
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.gen_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre_one = self.gen_service.get_one(1)
        assert genre_one is not None
        assert genre_one.id == 1
        assert genre_one.name == 'fantastic'

    def test_get_all(self):
        genres = self.gen_service.get_all()
        assert len(genres)>0

    def test_create(self):
        gen_d ={"id":1,"name":"ss"}
        user = self.gen_service.create(gen_d)
        assert gen_d['id'] is not None

    def test_update(self):
        gen_d = {"id": 1, "name": "ss"}
        self.gen_service.update(gen_d)

    def test_partially_update(self):
        gen_d = {"id": 1, "name": "ss"}
        self.gen_service.update(gen_d)

    def test_delete(self):
        self.gen_service.delete(1)
