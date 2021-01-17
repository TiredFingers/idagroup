from django import forms
from django.forms import ValidationError


class NewImageForm(forms.Form):
    url = forms.CharField(label='Ссылка', widget=forms.TextInput, required=False)
    img_file = forms.ImageField(label='Файл', required=False)
 
    def clean(self):
        cleaned_data = super().clean()

        url = cleaned_data.get('url', '')
        img_file = cleaned_data.get('img_file', '')

        if url and img_file:
            raise ValidationError('Можно указать либо url для загрузки, либо выбрать файл. Нельзя указать оба значения')

        if len(url) == 0 and img_file is None:
            raise ValidationError('Укажите url или выберите файл')


class ResizeImgForm(forms.Form):

    width = forms.DecimalField(max_value=9999.99, min_value=0, max_digits=6, decimal_places=2, required=False)
    height = forms.DecimalField(max_value=9999.99, min_value=0, max_digits=6, decimal_places=2, required=False)
    img_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super().clean()

        width = cleaned_data.get('width', None)
        height = cleaned_data.get('height', None)

        if width is None and height is None:
            raise ValidationError('Укажите ширину или высоту')
