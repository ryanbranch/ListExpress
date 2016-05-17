from django import forms

from .models import ItemList

class ItemListForm(forms.ModelForm):

    class Meta:
        model = ItemList
        fields = ('title', 'items',)