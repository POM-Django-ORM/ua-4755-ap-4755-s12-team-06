import datetime
from django.db import models
from django.utils import timezone

from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    end_at = models.IntegerField(null=True, blank=True)
    plated_end_at = models.IntegerField()

    def save(self, *args, **kwargs):
        if isinstance(self.created_at, (int, float)):
            self.created_at = datetime.datetime.fromtimestamp(
                self.created_at, tz=datetime.timezone.utc
            )

        if isinstance(self.end_at, datetime.datetime):
            self.end_at = int(self.end_at.timestamp())

        if isinstance(self.plated_end_at, datetime.datetime):
            self.plated_end_at = int(self.plated_end_at.timestamp())

        super().save(*args, **kwargs)

    def __str__(self):
        def fmt_date(dt):
            if not dt:
                return None
            if isinstance(dt, (int, float)):
                dt = datetime.datetime.fromtimestamp(dt, tz=datetime.timezone.utc)
            return dt.strftime("%Y-%m-%d %H:%M:%S+00:00")

        fields = {
            "id": self.id,
            "user": f"CustomUser(id={self.user.id})",
            "book": f"Book(id={self.book.id})",
            "created_at": fmt_date(self.created_at),
            "end_at": fmt_date(self.end_at),
            "plated_end_at": fmt_date(self.plated_end_at),
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
        c_at = (
            int(self.created_at.timestamp())
            if isinstance(self.created_at, datetime.datetime)
            else self.created_at
        )
        return {
            "id": self.id,
            "book": self.book.id,
            "user": self.user.id,
            "created_at": c_at,
            "end_at": self.end_at,
            "plated_end_at": self.plated_end_at,
        }

    @staticmethod
    def create(user, book, plated_end_at):
        if not user or not user.id or not book or not book.id:
            return None

        if book.count <= 0:
            return None

        try:
            # Якщо прийшов рядок (ISO-дата), перетворюємо її в timestamp
            if isinstance(plated_end_at, str):
                dt = datetime.datetime.fromisoformat(
                    plated_end_at.replace("Z", "+00:00")
                )
                plated_end_at = int(dt.timestamp())

            order = Order(user=user, book=book, plated_end_at=plated_end_at)
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
            self.plated_end_at = (
                int(plated_end_at.timestamp())
                if isinstance(plated_end_at, datetime.datetime)
                else plated_end_at
            )

        if end_at is not None:
            self.end_at = (
                int(end_at.timestamp())
                if isinstance(end_at, datetime.datetime)
                else end_at
            )

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
