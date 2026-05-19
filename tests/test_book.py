import pytest
from library_system.book import Book

class TestBook:
    def setup_method(self, method):
        Book.reset_counter()

    def test_attributes_correct(self):
        book1 = Book('hamnet', 'Nolan')
        book2 = Book('alice in wonderland', 'allen', status='borrowed')
        assert book1.title == 'hamnet'
        assert book1.id == 1
        assert book1.author == 'Nolan'
        assert book1.status == 'available'
        assert book2.id == 2
        assert book2.status == 'borrowed'

    @pytest.mark.parametrize('value, field', [(12, 'title'), ('', 'title'), (12,'author'), ('','author')])
    def test_invalid_title_or_author(self, value, field):
        with pytest.raises(ValueError, match=field):
            if field == 'title':
                book = Book(title=value, author='nolan')
            else:
                book = Book(title='hamnet', author=value)
        
    
    @pytest.mark.parametrize('value, error', [('string', ValueError), ('', ValueError)])
    def test_invalid_status(self, value, error):
        with pytest.raises(error):
            book = Book('hamnet', 'nolan', value)

    def test_id(self):
        book1 = Book('hamnet', 'nolan', id=5)
        book2 = Book('yellowstone', 'allen')
        book3 = Book('gravity', 'pitt', id=77)
        book4 = Book('sth', 'blunt')
        assert book1.id == 5
        assert book2.id == 6
        assert book3.id == 77
        assert book4.id == 78

    def test_equality(self):
        book1 = Book('hamnet', 'nolan')
        book2 = Book('hamnet', 'nolan', id=1)
        assert book1 == book2

        with pytest.raises(ValueError, match='Book type'):
            assert book1 == 'not a book obj'
        
        
        


