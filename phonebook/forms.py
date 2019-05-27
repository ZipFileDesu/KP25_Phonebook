from django import forms

#Форма поиска (просто строка с текстом)
class SearchForm(forms.Form):
    search = forms.CharField(help_text="Поиск", required=False, label="Поиск", max_length=100)
