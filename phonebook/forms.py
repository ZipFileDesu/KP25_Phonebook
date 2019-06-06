from django import forms


# Форма поиска (просто строка с текстом)
class SearchForm(forms.Form):
    q = forms.CharField(required=False, label="", max_length=100,
                        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder': 'Найти',
                                                      'data-toggle':'tooltip', 'title': 'Поиск осуществляется по всем '
                                                                                        'выводимым полям в таблице'}))

    def clean_q(self):
        data = self.cleaned_data['q'].strip()
        if not data:
            return False
        else:
            return True
