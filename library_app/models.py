from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.

loan_days_limit = {
    "book": 30,
    "magazine": 7
}

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

class Magazine(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.publisher}"

class BookLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loaned_timestamp = models.DateTimeField(auto_now_add=True)
    returned_timestamp = models.DateTimeField(null=True)

    def daysLeft(self):
        date_to_return = self.loaned_timestamp + \
        timedelta(days=loan_days_limit['book'])
        days_left = (date_to_return - self.loaned_timestamp).days
        return days_left

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"

class MagazineLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    loaned_timestamp = models.DateTimeField(auto_now_add=True)
    returned_timestamp = models.DateTimeField(null=True)

    def daysLeft(self):
        date_to_return = self.loaned_timestamp + \
        timedelta(days=loan_days_limit['magazine'])
        days_left = (date_to_return - self.loaned_timestamp).days
        return days_left

    def __str__(self):
        return f"{self.magazine.title} - {self.user.username}"