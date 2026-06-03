import datetime
from django.db import models

from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField()

    def __str__(self):
        def fmt(dt):
            if not dt:
                return None
            return dt.strftime("%Y-%m-%d %H:%M:%S+00:00")

        fields = {
            "id": self.id,
            "user": f"CustomUser(id={self.user.id})",
            "book": f"Book(id={self.book.id})",
            "created_at": fmt(self.created_at),
            "end_at": fmt(self.end_at),
            "plated_end_at": fmt(self.plated_end_at),
        }

        res = []
        for k, v in fields.items():
            if v is None:
                res.append(f"'{k}': None")
            elif "CustomUser" in str(v) or "Book" in str(v):
                res.append(f"'{k}': {v}")
            else:
                res.append(f"'{k}': '{v}'" if isinstance(v, str) else f"'{k}': {v}")

        return ", ".join(res)

    def __repr__(self):
        return f"Order(id={self.id})"

    def to_dict(self):

        return {
            "id": self.id,
            "book": self.book.id,
            "user": self.user.id,
            "created_at": self.created_at,
            "end_at": self.end_at,
            "plated_end_at": self.plated_end_at,
        }

    @staticmethod
    def create(user, book, plated_end_at):
        if not user or not user.id or not book or not book.id:
            return None
        if Order.objects.filter(book=book, end_at__isnull=True).count() >= book.count:
            return None
        try:
            if isinstance(plated_end_at, str):
                plated_end_at = datetime.datetime.fromisoformat(
                    plated_end_at.replace("Z", "+00:00")
                )
            order = Order(
                user=user,
                book=book,
                plated_end_at=plated_end_at,
            )
            order.save()
            book.count -= 1
            book.save()
            return order
        except Exception:
            return None

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            if isinstance(plated_end_at, int):
                plated_end_at = datetime.datetime.fromtimestamp(
                    plated_end_at, tz=datetime.timezone.utc
                )
            elif isinstance(plated_end_at, str):
                plated_end_at = datetime.datetime.fromisoformat(
                    plated_end_at.replace("Z", "+00:00")
                )
            self.plated_end_at = plated_end_at

        if end_at is not None:
            if isinstance(end_at, int):
                end_at = datetime.datetime.fromtimestamp(
                    end_at, tz=datetime.timezone.utc
                )
            elif isinstance(end_at, str):
                end_at = datetime.datetime.fromisoformat(end_at.replace("Z", "+00:00"))
            self.end_at = end_at

        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at__isnull=True))

    @staticmethod
    def delete_by_id(order_id):
        order = Order.get_by_id(order_id)
        if order:
            order.delete()
            return True
        return False
