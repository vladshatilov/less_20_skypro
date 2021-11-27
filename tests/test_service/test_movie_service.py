from unittest.mock import MagicMock

import pytest as pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)
    m1 = Movie(title="Омерзительная восьмерка",
               id=1,
               year=2015,
               trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
               description="США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество= генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.",
               rating=7.8)
    m2 = Movie(title="Дюна",
               id=2,
               year=2015,
               trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
               description="Это история любви старлетки, которая между прослушиваниями подает кофе состоявшимся кинозвездам, и фанатичного джазового музыканта, вынужденного подрабатывать в заштатных барах. Но пришедший к влюбленным успех начинает подтачивать их отношения.",
               rating=8.8)
    m3 = Movie(title="Душа",
               id=3,
               year=2021,
               trailer="https=//www.youtube.com/watch?v=lmB9VWm0okU",
               description="Париж. 1910 год. Ужасный монстр, напоминающий гигантское насекомое, нагоняет страх на всю Францию. Застенчивый киномеханик и неутомимый изобретатель начинают охоту на него. В этой погоне они знакомятся со звездой кабаре, сумасшедшим ученым и его умной обезьянкой и, наконец, самим монстром, который оказывается совсем не страшным. Теперь безобидное, как блоха, чудовище ищет у своих новых друзей защиты от вредного начальника городской полиции.",
               rating=4.8)

    movie_dao.get_one = MagicMock(return_value=m1)
    movie_dao.get_all = MagicMock(return_value=[m1, m2, m3])
    movie_dao.create = MagicMock(return_value=Movie(id=1))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService():
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie_one = self.movie_service.get_one(1)
        assert movie_one is not None
        assert movie_one.year == 2015
        assert movie_one.title == 'Омерзительная восьмерка'

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) == 3

    def test_create(self):
        movie_one = {
            "title": "Чикаго",
            "id": 7,
            "year": 2002,
            "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
            "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
            "rating": 7.2
        }
        user = self.movie_service.create(movie_one)
        assert movie_one['id'] is not None
        assert movie_one['rating'] == 7.2

    def test_update(self):
        movie_one = {
            "title": "Чикаго",
            "id": 1,
            "year": 2002,
            "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
            "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
            "rating": 7.2
        }
        self.movie_service.update(movie_one)

    def test_partially_update(self):
        movie_one = {
            "title": "Чикаго",
            "id": 1,
            "year": 2002,
            "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
            "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
            "rating": 7.2
        }
        self.movie_service.update(movie_one)

    def test_delete(self):
        self.movie_service.delete(1)
