from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import ItemList, Item, ItemComparison
from django.contrib.auth.decorators import login_required

def index(request):
    itemlists = ItemList.objects.all()
    context = {}
    context['itemlists'] = itemlists
    return render(request, 'listexpress/index.html', context)

def listdetail(request, itemlist_id):

    #Gets the User information
    user = None
    if request.user.is_authenticated():
        user = request.user

    #Gets the ItemList and Item information
    itemlist = get_object_or_404(ItemList, pk=itemlist_id)
    items = itemlist.item_set.all()
    context = {}
    context['itemlist'] = itemlist
    context['items'] = items
    if itemlist.fully_defined:
        comparisons = itemlist.itemcomparison_set.all()
        context['comparisons'] = comparisons

    #Determines if the ItemList was created by the User
    userOwnsList = False
    if user:
        if user == itemlist.member.user:
            userOwnsList = True
    context['userOwnsList'] = userOwnsList

    return render(request, 'listexpress/listdetail.html', context)

@login_required
def buildcomparisons(request, itemlist_id):
    itemlist = get_object_or_404(ItemList, pk=itemlist_id)
    if itemlist.fully_defined:
        items = itemlist.item_set.all()
        numItems = items.count
        for i in range(numItems - 1):
            for j in range(i + 1, numItems):
                itemlist.itemcomparison_set.create(item1_index=i,
                                                   item2_index=j,
                                                   comparison_name=(items[i].item_name +
                                                                    " vs. " +
                                                                    items[j].item_name))
        itemlist.save()