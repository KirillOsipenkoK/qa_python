import pytest
from main import BooksCollector


class TestBooksCollector:
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    @pytest.mark.parametrize('name, expected', [
        ('A' * 40, True),
        ('Тест', True),
        ('', False),
        ('B' * 41, False)
    ])
    def test_add_new_book(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    def test_add_duplicate_book(self, collector):
        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize('name, genre, expected', [
        ('Дюна', 'Фантастика', True),
        ('Несуществующая', 'Ужасы', False),
        ('Дюна', 'Роман', False)
    ])
    def test_set_book_genre(self, collector, name, genre, expected):
        collector.add_new_book('Дюна')
        collector.set_book_genre(name, genre)
        assert (collector.get_book_genre(name) == genre) == expected

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
        test_books = {'Оно': 'Ужасы', 'Сияние': 'Ужасы', 'Дюна': 'Фантастика'}
        for name, book_genre in test_books.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, book_genre)
        assert collector.get_books_with_specific_genre(genre) == expected

    def test_get_books_genre(self, collector):
        collector.add_new_book('Шерлок')
        assert 'Шерлок' in collector.get_books_genre()
        assert collector.get_book_genre('Шерлок') == ''

    def test_get_books_for_children(self, collector):
        test_books = {
            'Ну погоди!': 'Мультфильмы',
            'Оно': 'Ужасы',
            'Шерлок': 'Детективы'
        }
        for name, genre in test_books.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        children_books = collector.get_books_for_children()
        assert 'Ну погоди!' in children_books
        assert 'Оно' not in children_books
        assert 'Шерлок' not in children_books

    @pytest.mark.parametrize('name, expected', [
        ('Дюна', True),
        ('Несуществующая', False)
    ])
    def test_add_book_in_favorites(self, collector, name, expected):
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites(name)
        assert (name in collector.get_list_of_favorites_books()) == expected

    def test_add_duplicate_to_favorites(self, collector):
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Дюна')
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.delete_book_from_favorites('Дюна')
        assert 'Дюна' not in collector.get_list_of_favorites_books()

    def test_get_favorites_list(self, collector):
        collector.add_new_book('Книга1')
        collector.add_new_book('Книга2')
        collector.add_book_in_favorites('Книга1')
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ['Книга1']
        assert len(favorites) == 1
