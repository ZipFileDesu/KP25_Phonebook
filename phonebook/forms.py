from django import forms


# Форма поиска (просто строка с текстом)
class SearchForm(forms.Form):
    q = forms.CharField(required=False, label="", max_length=100,
                        widget=forms.TextInput(attrs={'class' : 'form-control mr-sm-2','placeholder': 'Найти',
                                                      'data-toggle':'tooltip', 'title': 'Поиск осуществляется по всем '
                                                                                        'выводимым полям в таблице'}))

    def clean_q(self):
        #Если нажата кнопка "Очистки", то возвращаем ложь, иначе, если нажата кнопка поиска, возвращаем истину
        if 'clear' in self.data:
            return 'clear'
        elif 'search' in self.data:
            data = self.cleaned_data['q'].strip()
            if not data:
                return 'clear'
            else:
                return 'search'