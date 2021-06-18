from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email',
                  'age', 'avatar', 'password', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            if field_name == 'is_staff':
                field.widget.attrs['class'] = 'form-check-input'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data


class ShopUserCreateForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1',
                  'password2', 'email', 'age', 'avatar', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'is_staff':
                field.widget.attrs['class'] = 'form-check-input'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'


class ProductCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'is_active',
                  'short_desc', 'short_desc', 'quantity',
                  'image', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'is_active',
                  'short_desc', 'short_desc', 'quantity',
                  'image', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'