from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth import authenticate, login as dj_login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from library_app.models import Book, BookLoan
from django.utils import timezone

book_limit = 2

# Create your views here.
def login(request):
    context = {}
    
    #login request
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password= request.POST["password"])

        if user: 
            #user login success
            dj_login(request, user)
            return HttpResponseRedirect(reverse("library_app:index"))
        else: 
            #user login failed
            context = {"error_message": "Invalid username or password combination"}
    
    return render(request, "user_app/login.html", context)

@login_required
def profile(request):
    user = request.user
    bookloans = BookLoan.objects.filter(user=user)
    context = {"bookloans": bookloans, "user": user}
    return render(request, "user_app/profile.html", context)

@login_required
def loan_item(request, type, id):
    if type == "book":
        book = get_object_or_404(Book, id=id)
        loaned_books_list = BookLoan.objects.filter(book = book).filter(returned_timestamp__isnull = True).count()

        if loaned_books_list == 0:
            books_loaned_amount = (BookLoan.objects.filter(user=request.user) & BookLoan.objects.filter(returned_timestamp__isnull=True)).count()
            if books_loaned_amount < book_limit:
                book.is_available = False
                book.save()
                BookLoan.objects.create(book=book, user=request.user)
         
    return HttpResponseRedirect(reverse("library_app:index"))


@login_required
def return_item(request, type, id):
    if type == "book":
        book = get_object_or_404(Book, id=id)
        books_loaned = BookLoan.objects.filter(book = book, returned_timestamp__isnull=True, user=request.user).count()

        if books_loaned == 1: 
            book.is_available = True
            book.save()
            loaned_book = BookLoan.objects.filter(book=book).get(returned_timestamp=True)
            loaned_book.returned_timestamp = timezone.now()
            loaned_book.save()

    return HttpResponseRedirect(reverse("user_app:profile"))
