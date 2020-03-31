from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from . models import Book, BookLoan, Magazine, MagazineLoan
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    books = Book.objects.filter(is_available = True)
    magazines = Magazine.objects.filter(is_available = True)
    context = {"books": books, "magazines": magazines}
    return render(request, "library_app/index.html", context)
