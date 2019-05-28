from django import forms

#Форма поиска (просто строка с текстом)
class SearchForm(forms.Form):
    q = forms.CharField(help_text="Поиск", required=False, label="Поиск", max_length=100)

    def clean_q(self):
        data = self.cleaned_data['q']
        str = data.strip()
        if not str:
            return False
        else:
            return True
