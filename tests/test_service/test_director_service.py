from unittest.mock import MagicMock

import pytest as pytest

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    dir_dao = DirectorDAO(None)
    d1 = Director(id=1, name='Dddao')
    d2 = Director(id=2, name='MsX')
    d3 = Director(id=3, name='MrD')

    dir_dao.get_one = MagicMock(return_value=d1)
    dir_dao.get_all = MagicMock(return_value=[d1, d2, d3])
    dir_dao.create = MagicMock(return_value=Director(id=1))
    dir_dao.delete = MagicMock()
    dir_dao.update = MagicMock()
    return dir_dao

def test_one():
    assert 1==1

class TestDirectorService():
    @pytest.fixture(autouse=True)
    def dir_service(self, director_dao):
        self.dir_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        dir_one = self.dir_service.get_one(1)
        assert dir_one is not None
        assert dir_one.id == 1
        assert dir_one.name == 'Dddao'

    def test_get_all(self):
        dirs = self.dir_service.get_all()
        assert len(dirs)>0

    def test_create(self):
        dir_d ={"id":1,"name":"ss"}
        user = self.dir_service.create(dir_d)
        assert dir_d['id'] is not None

    def test_update(self):
        dir_d = {"id": 1, "name": "ss"}
        self.dir_service.update(dir_d)

    def test_partially_update(self):
        dir_d = {"id": 1, "name": "ss"}
        self.dir_service.update(dir_d)

    def test_delete(self):
        self.dir_service.delete(1)
