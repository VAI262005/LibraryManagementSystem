from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# =========================
# USER ROLE SYSTEM
# =========================

class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='student')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# =========================
# BOOK MODEL
# =========================

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


# =========================
# MEMBER MODEL
# =========================

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# =========================
# ISSUE BOOK MODEL
# =========================

class IssueBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    # Optional: future enhancement
    due_date = models.DateField(null=True, blank=True)
    fine_amount = models.IntegerField(default=0)

    def fine(self):
        """
        First 14 days free
        ₹5 per day after that
        """

        if self.return_date:
            days = (self.return_date - self.issue_date).days
        else:
            days = (timezone.now().date() - self.issue_date).days

        if days > 14:
            return (days - 14) * 5

        return 0

    def status(self):
        if self.return_date:
            return "Returned"
        return "Issued"

    def __str__(self):
        return f"{self.book.title} - {self.member.name}"