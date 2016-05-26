from django.contrib import admin

from .models import *

admin.site.register(Member)
admin.site.register(ItemList)
admin.site.register(Item)
admin.site.register(ItemComparison)