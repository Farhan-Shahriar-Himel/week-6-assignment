from typing import Any
from django.shortcuts import render, redirect
from books import models
from account import forms
from django.views.generic import DetailView, FormView
import borrowings
from django.contrib import messages
import borrowings.models
from reviews.models import ReviewModel
from reviews.forms import ReviewForm
from account.views import send_transaction_email
# Create your views here.



def home(request, slug=None):
    catagories = models.CategoryClass.objects.all()
    books = models.BookClass.objects.all()
    if slug is not None:
        cat = models.CategoryClass.objects.get(slug=slug)
        books = models.BookClass.objects.filter(category=cat)
    return render(request, 'core/homepage.html', {'categories': catagories, 'books': books})


def detailsShow(request, pk):
    book = models.BookClass.objects.get(id=pk)
    users = borrowings.models.BorrowingClass.objects.filter(book=book)
    reviews = ReviewModel.objects.filter(book=book)
    bought = False
    form = ""

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.book = book
            new_form.name = request.user.first_name
            new_form.email = request.user.email
            new_form.save()
        return redirect('details', pk)

    if request.user.is_authenticated:
        for user in users:
            if user.account == request.user.account:
                bought = True
    if bought == True:
        form = ReviewForm()

    return render(request, 'core/detailspage.html', {'book' : book, 'form': form, 'reviews': reviews, 'bought': bought})





def borrowed(request, id):
    acc = request.user.account
    obj = models.BookClass.objects.get(id = id)
    price = obj.price
    balance = acc.balance
    remain = acc.balance - obj.price
    
    if remain < 0:
        messages.warning(request, "You do not have enough Money")
        return redirect('homepage')

    new_model = borrowings.models.BorrowingClass.objects.create(
        account=acc,
        book=obj,
        balance_after_borrowing=remain,
    )
    print(acc)
    print(new_model)
    acc.balance -= price
    acc.save()
    messages.success(request, "You have successfully borrowed this book")
    send_transaction_email(request.user, price, 'Borrowed Book', 'core/borrow_email.html', obj.title)
    return redirect('homepage')


