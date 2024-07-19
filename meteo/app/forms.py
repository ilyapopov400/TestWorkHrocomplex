from django import forms


class City(forms.Form):
    """
    - форма для ввода города
    """
    city = forms.CharField(min_length=2, max_length=20,
                           label="Имя", help_text="Введите название города")
