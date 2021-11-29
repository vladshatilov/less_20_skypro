from random import randint
from unittest.mock import MagicMock, patch

import pytest
from dao.model.director import Director
from service.director import DirectorService


class TestDirectorService:

    @pytest.fixture
    def director_1(self):
        return Director(id=1, name='director_1')

    @pytest.fixture
    def director_2(self):
        return Director(id=2, name='director_2')

    @pytest.fixture()
    def dao(self):
        with patch('service.director.DirectorDAO') as mock:
            mock = MagicMock(
                get_one=MagicMock(),
                get_all=MagicMock(),
                create=MagicMock(),
                delete=MagicMock(),
                update=MagicMock(),
            )
            return mock

    def test_get_one(self, dao, director_1):
        dao.get_one.return_value = director_1
        assert DirectorService(dao).get_one(1) == director_1

    def test_get_one_not_exists(self, dao):
        dao.get_one.return_value = None
        assert DirectorService(dao).get_one(1) is None

    @pytest.mark.parametrize('objects', [
        [director_1, director_2],
        []
    ])
    def test_get_all(self, objects, dao):
        assert isinstance(objects, list)
        dao.get_all.return_value = objects
        assert DirectorService(dao).get_all() == objects

    def test_create(self, dao, director_1):
        dao.create.return_value = director_1
        assert DirectorService(dao).create({'name': director_1.name}) == director_1

    def test_update(self, dao, director_1):
        dao.update.return_value = director_1
        assert DirectorService(dao).update({'id': director_1.id, 'name': director_1.name}) == director_1

    @pytest.mark.parametrize('data, get_one_response, update_called', [
        [{'id': 1, 'name': 'some_name'}, director_1, True],
        [{'id': 1}, director_1, True],
        [{'id': 2}, None, False],

    ])
    def test_partially_update(self, data, get_one_response, update_called, dao):
        dao.get_one.return_value = get_one_response
        DirectorService(dao).partially_update(data)
        assert dao.update.called is update_called

    def test_partially_update_bad_request(self, dao):
        with pytest.raises(KeyError):
            DirectorService(dao).partially_update({'pk': 1, 'name': 'some_name'})

    @pytest.mark.parametrize('get_one_response', [
        director_1,
        None
    ])
    def test_delete(self, get_one_response, dao):
        """
        Посмотри на свою функцию delete - в dao она упадет на самом деле,
        т.к. self.session.delete(None) сделать нельзя.
        Чтобы проверить это поведение, нужно по-хорошему мокать подключение к базе, но раз мы этого не делаем
        поправь код в любом случае
        """
        dao.delete.return_value = get_one_response
        DirectorService(dao).delete(randint(1, 10))
