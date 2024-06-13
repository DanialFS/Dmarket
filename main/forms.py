from django.contrib.auth.models import User
from django import forms
from .models import Brand, Color


class ProductFilterForm(forms.Form):
    SORT_CHOICES = [
        ('price_asc', 'Цена: по возрастанию'),
        ('price_desc', 'Цена: по убыванию'),
        ('newest', 'Новизне'),
    ]

    search = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'placeholder': 'Поиск...'}))
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, empty_label="Бренд:")
    color = forms.ModelChoiceField(queryset=Color.objects.all(), required=False, empty_label="Цвет:")
    min_price = forms.DecimalField(
        required=False, min_value=0, label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Цена от:'})
    )
    max_price = forms.DecimalField(
        required=False, min_value=0, label='',
        widget=forms.NumberInput(attrs={'placeholder': 'Цена до:'})
    )
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Сортировка')
    discount = forms.BooleanField(required=False, label='Скидка:')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


