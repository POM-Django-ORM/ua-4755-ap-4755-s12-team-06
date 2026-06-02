import datetime
from django.db import models


class Author(models.Model):
    """
    This class represents an Author. \n
    Attributes:
    -----------
    param name: Describes name of the author
    type name: str max_length=20
    param surname: Describes last name of the author
    type surname: str max_length=20
    param patronymic: Describes middle name of the author
    type patronymic: str max_length=20

    """

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        """
        Захист моделі Author від datetime об'єктів у тестах.
        """
        if hasattr(self, "created_at") and isinstance(
            self.created_at, datetime.datetime
        ):
            self.created_at = int(self.created_at.timestamp())

        if hasattr(self, "updated_at") and isinstance(
            self.updated_at, datetime.datetime
        ):
            self.updated_at = int(self.updated_at.timestamp())

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Magic method is redefined to show all information about Author.
        :return: author id, author name, author surname, author patronymic
        """
        fields = {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
        }
        return ", ".join([f"'{k}': {repr(v)}" for k, v in fields.items()])

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        :return: class, id
        """
        return f"Author(id={self.id})"

    @staticmethod
    def get_by_id(author_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        try:
            return Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(author_id):
        """
        :param author_id: an id of a author to be deleted
        :type author_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        author = Author.get_by_id(author_id)
        if author:
            author.delete()
            return True
        return False

    @staticmethod
    def create(name, surname, patronymic):
        """
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: a new author object which is also written into the DB
        """

        try:
            author = Author(name=name, surname=surname, patronymic=patronymic)
            author.full_clean()
            author.save()
            return author
        except Exception:
            return None

    def to_dict(self):
        """
        :return: author id, author name, author surname, author patronymic
        :Example:
        | {
        |   'id': 8,
        |   'name': 'fn',
        |   'surname': 'mn',
        |   'patronymic': 'ln',
        | }
        """
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
        }

    def update(self, name=None, surname=None, patronymic=None):
        """
        Updates author in the database with the specified parameters.
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: None
        """
        if name is not None:
            self.name = name
        if surname is not None:
            self.surname = surname
        if patronymic is not None:
            self.patronymic = patronymic
        try:
            self.full_clean()
            self.save()
        except Exception:
            pass

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all authors
        """
        return Author.objects.all()
