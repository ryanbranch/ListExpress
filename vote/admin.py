from django.contrib import admin
from .models import ItemList, ItemComparison, Item

admin.site.register(ItemList)
admin.site.register(ItemComparison)
admin.site.register(Item)