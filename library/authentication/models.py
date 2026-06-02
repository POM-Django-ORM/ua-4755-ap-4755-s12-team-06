import time
import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

ROLE_CHOICES = (
    (0, "visitor"),
    (1, "admin"),
)


def get_current_timestamp():
    return int(time.time())


class CustomUser(AbstractBaseUser):
    """
    This class represents a basic user. \n
    Attributes:
    -----------
    param first_name: Describes first name of the user
    type first_name: str max length=20
    param last_name: Describes last name of the user
    type last_name: str max length=20
    param middle_name: Describes middle name of the user
    type middle_name: str max length=20
    param email: Describes the email of the user
    type email: str, unique, max length=100
    param password: Describes the password of the user
    type password: str
    param created_at: Describes the date when the user was created. Can't be changed.
    type created_at: int (timestamp)
    param updated_at: Describes the date when the user was modified
    type updated_at: int (timestamp)
    param role: user role, default role (0, 'visitor')
    type updated_at: int (choices)
    param is_active: user role, default value False
    type updated_at: bool

    """

    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    role = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    # --- СИСТЕМНІ НАЛАШТУВАННЯ DJANGO AUTH ---
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    # ----------------------------------------

    def save(self, *args, **kwargs):
        #  datetime  в timestamp
        if isinstance(self.created_at, (int, float)):
            self.created_at = datetime.datetime.fromtimestamp(
                self.created_at, tz=datetime.timezone.utc
            )
        if isinstance(self.updated_at, (int, float)):
            self.updated_at = datetime.datetime.fromtimestamp(
                self.updated_at, tz=datetime.timezone.utc
            )
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at,
                 user role, user is_active
        """
        d = self.to_dict()
        return ", ".join([f"'{k}': {repr(v)}" for k, v in d.items()])

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f"CustomUser(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        user = CustomUser.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        """
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :return: a new user object which is also written into the DB
        """
        if not email or "@" not in email:
            return None
        try:
            user = CustomUser(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
            )
            user.full_clean()
            user.save()
            return user
        except Exception:
            return None

    def to_dict(self):
        """
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at, user is_active
        :Example:
        | {
        |   'id': 8,
        |   'first_name': 'fn',
        |   'middle_name': 'mn',
        |   'last_name': 'ln',
        |   'email': 'ln@mail.com',
        |   'created_at': 1509393504,
        |   'updated_at': 1509402866,
        |   'role': 0
        |   'is_active:' True
        | }
        """
        c_at = (
            int(self.created_at.timestamp())
            if isinstance(self.created_at, datetime.datetime)
            else int(self.created_at)
        )
        u_at = (
            int(self.updated_at.timestamp())
            if isinstance(self.updated_at, datetime.datetime)
            else int(self.updated_at)
        )

        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": c_at,
            "updated_at": u_at,
            "role": self.role,
            "is_active": self.is_active,
        }

    def update(
        self,
        first_name=None,
        last_name=None,
        middle_name=None,
        password=None,
        role=None,
        is_active=None,
    ):
        """
        Updates user profile in the database with the specified parameters.\n
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param password: password of a user
        :type password: str
        :param role: role id
        :type role: int
        :param is_active: activation state
        :type is_active: bool
        :return: None
        """
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if middle_name is not None:
            self.middle_name = middle_name
        if password is not None:
            self.password = password
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active

        self.updated_at = int(timezone.now().timestamp())
        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all users
        """
        return CustomUser.objects.all()

    def get_role_name(self):
        """
        returns str role name
        """
        return dict(ROLE_CHOICES).get(self.role)
