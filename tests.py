from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
import pytest

class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # Параметризация для тестов с разной длиной имени
    @pytest.mark.parametrize('name, expected', [
        ('A' * 40, True),    # Максимальная длина
        ('Тест', True),      # Корректное имя
        ('', False),         # Пустое имя
        ('B' * 41, False)    # Слишком длинное
    ])
    def test_add_new_book(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.books_genre) == expected

    def test_add_duplicate_book(self, collector):
        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize('name, genre, expected', [
        ('Дюна', 'Фантастика', True),        # Корректные данные
        ('Несуществующая', 'Ужасы', False),  # Книги нет в словаре
        ('Дюна', 'Роман', False)             # Неверный жанр
    ])
    def test_set_book_genre(self, collector, name, genre, expected):
        collector.add_new_book('Дюна')
        collector.set_book_genre(name, genre)
        assert (collector.books_genre.get(name) == genre) == expected

    def test_get_book_genre(self, collector):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        assert collector.get_book_genre('Оно') == 'Ужасы'
        assert collector.get_book_genre('Неизвестная') is None

    @pytest.mark.parametrize('genre, expected', [
        ('Ужасы', ['Оно', 'Сияние']),
        ('Комедии', []),
        ('Фантастика', ['Дюна'])
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected):
        books = {'Оно': 'Ужасы', 'Сияние': 'Ужасы', 'Дюна': 'Фантастика'}
        for name, g in books.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, g)
        assert collector.get_books_with_specific_genre(genre) == expected

    def test_get_books_genre(self, collector):
        collector.add_new_book('Шерлок')
        assert collector.get_books_genre() == collector.books_genre

    def test_get_books_for_children(self, collector):
        test_books = {
            'Ну погоди!': 'Мультфильмы',
            'Оно': 'Ужасы',
            'Шерлок': 'Детективы'
        }
        for name, genre in test_books.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert 'Ну погоди!' in collector.get_books_for_children()
        assert 'Оно' not in collector.get_books_for_children()
        assert 'Шерлок' not in collector.get_books_for_children()

    @pytest.mark.parametrize('name, expected', [
        ('Дюна', True),
        ('Несуществующая', False)
    ])
    def test_add_book_in_favorites(self, collector, name, expected):
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites(name)
        assert (name in collector.favorites) == expected

    def test_add_duplicate_to_favorites(self, collector):
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Дюна')
        assert len(collector.favorites) == 1

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.delete_book_from_favorites('Дюна')
        assert 'Дюна' not in collector.favorites

    def test_get_favorites_list(self, collector):
        collector.add_new_book('Книга1')
        collector.add_new_book('Книга2')
        collector.add_book_in_favorites('Книга1')
        assert collector.get_list_of_favorites_books() == ['Книга1']
