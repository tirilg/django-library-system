from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from . models import Book, BookLoan
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    #books_loaned = BookLoan.objects.filter(returned_timestamp__isnull=True)
    #books = Book.objects.all().exclude(id__in = books_loaned.book_set)
    books = Book.objects.filter(is_available = True)
    context = {"books": books}
    return render(request, "library_app/index.html", context)
