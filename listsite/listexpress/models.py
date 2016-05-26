from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Member(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class ItemList(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=200, default='UNNAMED LIST')
    num_items = models.IntegerField(default=None, blank=True, null=True)
    fully_defined = models.BooleanField(default=False)

    def __str__(self):
        return self.list_name

class Item(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    itemlist = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100, default='UNNAMED ITEM')

    def __str__(self):
        return self.item_name

class ItemComparison(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    itemlist = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    item1_index = models.IntegerField(default=0)
    item2_index = models.IntegerField(default=0)
    comparison_name = models.CharField(max_length=205, default='UNNAMED COMPARISON')
    true_votes = models.IntegerField(default=0)
    false_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.comparison_name