from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import ItemList
from .forms import ItemListForm

# Create your views here.
def itemlist_list(request):
    itemlists = ItemList.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'vote/itemlist_list.html', {'itemlists': itemlists})
    
def itemlist_detail(request, pk):
    itemlist = get_object_or_404(ItemList, pk=pk)
    itemlist.makeItemDict()
    return render(request, 'vote/itemlist_detail.html', {'itemlist': itemlist})
    
def itemlist_new(request):
    if request.method == "POST":
        form = ItemListForm(request.POST)
        if form.is_valid():
            itemlist = form.save(commit=False)
            itemlist.author = request.user
            itemlist.published_date = timezone.now()
            itemlist.save()
            return redirect('itemlist_detail', pk=itemlist.pk)
    else:
        form = ItemListForm()
    return render(request, 'vote/itemlist_edit.html', {'form': form})
    
def itemlist_edit(request, pk):
    itemlist = get_object_or_404(ItemList, pk=pk)
    if request.method == "POST":
        form = ItemListForm(request.POST, instance=itemlist)
        if form.is_valid():
            itemlist = form.save(commit=False)
            itemlist.author = request.user
            itemlist.published_date = timezone.now()
            itemlist.save()
            return redirect('itemlist_detail', pk=itemlist.pk)
            
            #Technically this isn't necessary unless the form is used to actually change content
            itemlist.madeItemDict = False
    else:
        form = ItemListForm(instance=itemlist)
    return render(request, 'vote/itemlist_edit.html', {'form': form})