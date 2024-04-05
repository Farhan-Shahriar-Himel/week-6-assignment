from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from . import forms
from .models import User, AccountModel
from django.views.generic import FormView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from borrowings.models import BorrowingClass
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# Create your views here.


def send_transaction_email(user, amount, subject, template, book=None):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
            'book': book,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class registrationClass(FormView):
    template_name = 'account/registration.html'
    success_url = reverse_lazy('login')
    form_class = forms.RegistrationForm

    def form_valid(self, form):
        user = form.save()
        print(user)
        messages.success(self.request, "The acount has been created successfully")
        send_transaction_email(user, 0, 'Create New Account', 'account/create_account_mail.html')
        return super().form_valid(form)



class LoginClass(LoginView):
    template_name = 'account/registration.html'

    def get_success_url(self) -> str:
        return reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        kwargs['heading'] = 'Log in'
        return super().get_context_data(**kwargs)


class ProfileClass(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'user': self.request.user}
        borrowed_books = BorrowingClass.objects.filter(account=self.request.user.account)
        context['borrowing_details'] = borrowed_books
        return context
    


class EditProfileClass(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account/registration.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('profile')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('homepage')


class ChangePassClass(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/registration.html'
    success_url = reverse_lazy('profile')


class deposit(LoginRequiredMixin, FormView):
    form_class = forms.DepositFrom
    template_name = 'account/transaction.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        acc = self.request.user.account
        acc.balance += amount
        acc.save()
        send_transaction_email(self.request.user, amount, 'Deposit Money', 'account/deposit_money.html')
        return super().form_valid(form)
    

class withdraw(LoginRequiredMixin, FormView):
    form_class = forms.WithdrawForm
    template_name = 'account/transaction.html'
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        acc = self.request.user.account
        acc.balance -= amount
        acc.save()
        send_transaction_email(self.request.user, amount, 'Withdraw Money', 'account/withdraw_money.html')
        return super().form_valid(form)
    

def return_book(request, id):
    data = BorrowingClass.objects.get(id=id)
    price = data.book.price
    acc = request.user.account
    acc.balance += price 
    acc.save()
    data.delete()
    send_transaction_email(request.user, price, 'Return Book', 'account/return_book.html', data.book.title)
    return redirect('profile')