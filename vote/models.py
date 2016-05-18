from django.db import models
from django.utils import timezone


class ItemList(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    list_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    madeItemDict = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
    def makeItemDict(self):
        if not self.madeItemDict:
            listOfItems = self.list_text.split('\n')
            numItems = len(listOfItems)
            
            #Creates the Item objects from list_text
            for i in range(numItems):
                self.item_set.create(item_text=listOfItems[i], item_id=i)
                print("Created item: " + str(self.item_set.all().last()))
                
            #Creates the ItemComparison objects from items
            for i, itemOne in enumerate(self.item_set.all()):
                for j, itemTwo in enumerate(self.item_set.all()):
                    if j > i:
                        self.itemcomparison_set.create(item1=itemOne, item2=itemTwo)
            self.madeItemDict = True
            self.save()
            
            #NOTE: Some temporary print statements
            for theItem in self.item_set.all():
                print(theItem)
            for theComparison in self.itemcomparison_set.all():
                print(theComparison)

class Item(models.Model):
    itemlist = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    item_text = models.CharField(max_length=200, default="UNNAMED ITEM")
    item_id = models.IntegerField(default=-1)
    item_rank = models.IntegerField(default=-1)
    
    def __str__(self):
        return (self.item_text + ": " + str(self.item_id))
                
class ItemComparison(models.Model):
    itemlist = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    
    #NOTE: Keep in mind that the default values are -1, so could cause index issues
    #NOTE: As long as no ItemComparisons exist on first run, I can remove the "null=True"
    item1 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemcomparison_item1s')
    item2 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemcomparison_item2s')
    
    #Comparisons are true if item1 > item2, or false if item1 <= item2
    trueVotes = models.IntegerField(default=0)
    falseVotes = models.IntegerField(default=0)
    
    def __str__(self):
        return (
            self.item1.item_text +
            " vs. " +
            self.item2.item_text +
            ": (" +
            str(self.item1.item_id) +
            "," +
            str(self.item2.item_id) +
            ")"
        )
        