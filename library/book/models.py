from django.db import models
from author.models import Author  
class Book(models.Model):
    """
    This class represents a Book.
    """
    # 1. Оголошуємо поля бази даних (саме на їх відсутність сварився Django)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True)
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        """
        authors_list = [f"{a.name} {a.surname}" for a in self.authors.all()]
        return f"ID: {self.id}, Name: {self.name}, Description: {self.description}, Count: {self.count}, Authors: {authors_list}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        """
        return f"{self.__class__.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        """
        :param book_id: SERIAL: the id of a Book to be found in the DB
        """
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        """
        :param book_id: an id of a book to be deleted
        """
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return True
        except Book.DoesNotExist:
            return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        """
        :return: a new book object which is also written into the DB
        """
        book = Book.objects.create(name=name, description=description, count=count)
        if authors is not None:
            book.authors.set(authors)
        return book

    def to_dict(self):
        """
        :return: book id, book name, book description, book count, book authors
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.id for author in self.authors.all()]
        }

    def update(self, name=None, description=None, count=None):
        """
        Updates book in the database with the specified parameters.
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        """
        Add authors to book in the database with the specified parameters.
        """
        if authors:
            self.authors.add(*authors)

    def remove_authors(self, authors):
        """
        Remove authors to book in the database with the specified parameters.
        """
        if authors:
            self.authors.remove(*authors)

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all books
        """
        return list(Book.objects.all())