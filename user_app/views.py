from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth import authenticate, update_session_auth_hash, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from library_app.models import Book, BookLoan, Magazine, MagazineLoan


# amount of books and magazines a user can loan at a time
book_limit = 10
magazine_limit = 3

####### - Sign up - ####### 

def signup(request): 
    context = {}
    
    if request.method == "POST":
        username = request.POST['user']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password: 
            if User.objects.create_user(username, email, password):
                return HttpResponseRedirect(reverse('user_app:login'))
            else:
                context = {
                    'error': 'Could not create user account - Please try again.'
                }
        else:
            context = {
                'error': 'Passwords did not match - Please try again.'
            }
    return render(request, 'user_app/signup.html', context)


####### - Log in - ####### 

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


####### - Change password - ####### 

@login_required
def change_password(request):
    context = {}

    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password_confirm = request.POST['new_password_confirm']

        # If the "old password" matches the users password
        if request.user.check_password(old_password):

            # If new passwords match 
            if new_password == new_password_confirm:
                user = get_object_or_404(User, username=request.user.username)
                user.set_password(new_password)
                user.save()

                context = {"error_message": "Password changed"}

                # Stay logged in after a password change
                update_session_auth_hash(request, user)
                return HttpResponseRedirect(reverse('user_app:profile'))

            # Passwords do not match
            else:
                context = {"error_message": "Passwords do not match"}

        # Wrong current password
        else:
            context = {"error_message": "Wrong password"}

    return render(request, 'user_app/change_password.html', context)


####### - Log out - ####### 

def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('user_app:login'))


####### - Delete account - ####### 

@login_required
def delete_account(request):
    context = {}

    if request.method == "POST":
        if request.POST['confirm_deletion'] == "YES":
            user = authenticate(request, username=request.user.username, password=request.POST['password'])
            if user:
                user.delete()
                return HttpResponseRedirect(reverse('user_app:login'))
            else:
                context = {"error_message": "Incorrect password"}
        else:
            context = {"error_message": "User could not be deleted"}

    return render(request, 'user_app/delete_account.html', context)



####### - User profile with loaned items - ####### 

@login_required
def profile(request):
    user = request.user
    bookloans = BookLoan.objects.filter(user=user).order_by("returned_timestamp")
    magazineloans = MagazineLoan.objects.filter(user=user).order_by("returned_timestamp")
    context = {"bookloans": bookloans, "magazineloans": magazineloans, "user": user}
    return render(request, "user_app/profile.html", context)


####### - Loan book or magazine - ####### 

@login_required
def loan_item(request, type, id):
    if type == "book":
        book = get_object_or_404(Book, id=id)
        loaned_books_list = BookLoan.objects.filter(book = book).filter(returned_timestamp__isnull = True).count()

        if loaned_books_list == 0:
            loaned_books_amount = (BookLoan.objects.filter(user=request.user) & BookLoan.objects.filter(returned_timestamp__isnull=True)).count()
            if loaned_books_amount < book_limit:
                book.is_available = False
                book.save()
                BookLoan.objects.create(book=book, user=request.user)

    if type == "magazine":
        magazine = get_object_or_404(Magazine, id=id)
        loaned_magazines_list = MagazineLoan.objects.filter(magazine=magazine).filter(returned_timestamp__isnull=True).count()

        if loaned_magazines_list == 0:
            loaned_magazines_amount = (MagazineLoan.objects.filter(user=request.user) & MagazineLoan.objects.filter(returned_timestamp__isnull=True)).count()
            if loaned_magazines_amount < magazine_limit:
                magazine.is_available = False
                magazine.save()
                MagazineLoan.objects.create(magazine=magazine, user=request.user)
            
    return HttpResponseRedirect(reverse("library_app:index"))



####### - Return loaned book or magazine - ####### 

@login_required
def return_item(request, type, id):
    if type == "book":
        book = get_object_or_404(Book, id=id)
        books_loaned = BookLoan.objects.filter(book=book, returned_timestamp__isnull=True, user=request.user).count()
    
        if books_loaned == 1: 
            book.is_available = True
            book.save()
            loaned_book = BookLoan.objects.filter(book=book).get(returned_timestamp__isnull=True)
            loaned_book.returned_timestamp = timezone.now()
            loaned_book.save()
    
    if type == "magazine":
        magazine = get_object_or_404(Magazine, id=id)
        magazines_loaned = MagazineLoan.objects.filter(magazine=magazine, returned_timestamp__isnull=True, user=request.user).count()

        if magazines_loaned == 1:
            magazine.is_available = True
            magazine.save()
            loaned_magazine = MagazineLoan.objects.filter(magazine=magazine).get(returned_timestamp__isnull=True)
            loaned_magazine.returned_timestamp = timezone.now()
            loaned_magazine.save()

    return HttpResponseRedirect(reverse("user_app:profile"))


####### - Admin page showing loaned items - ####### 

@login_required
def admin(request):

    context = {}
    user = request.user 
    bookloans = BookLoan.objects.filter(returned_timestamp__isnull=True).order_by("loaned_timestamp")
    magazineloans = MagazineLoan.objects.filter(returned_timestamp__isnull=True).order_by("loaned_timestamp")
    context = {"bookloans": bookloans, "magazineloans": magazineloans}
    return render(request, "user_app/admin.html", context)
