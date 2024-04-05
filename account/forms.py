from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import User, AccountModel

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save()
            AccountModel.objects.create(user=our_user)
        return our_user
    

class DepositFrom(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=12)

    def clean_amount(self):
        min_amount = 100
        amount = self.cleaned_data.get('amount')

        if amount < min_amount:
            raise forms.ValidationError(
                "You must deposit minimum 100 tk"
            )
        return amount

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=12)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        return super().__init__(*args, **kwargs)

    def clean_amount(self):
        min_amount = 100
        max_amount = 20000
        balance = self.request.user.account.balance
        amount = self.cleaned_data.get('amount')

        if amount > balance:
            raise forms.ValidationError(
                f"You have {balance} tk in your account. You can not deposit more then this"
            )
        if amount < min_amount:
            raise forms.ValidationError(
                "You must withdraw minimum 100 tk"
            )

        if amount > max_amount:
            raise forms.ValidationError(
                "You can withdraw maximum 20000 tk"
            )
        
        return amount
