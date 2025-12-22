from django.shortcuts import render, redirect
from django.utils import timezone
from .models import PantryItem

def dashboard(request):
    quick_list = ["Milk", "Eggs", "Bread", "Butter", "Apples"]
    today_date = timezone.now().date()
    
    # POST LOGIC: Save directly without checking for a user
    if request.method == "POST":
        name = request.POST.get('name')
        expiry = request.POST.get('expiry_date')
        quick_item = request.POST.get('quick_item')

        if name and expiry:
            # We removed 'user=request.user' so it saves directly
            PantryItem.objects.create(name=name, expiry_date=expiry)
            return redirect('dashboard')
        elif quick_item:
            PantryItem.objects.create(name=quick_item, expiry_date=today_date)
            return redirect('dashboard')

    # GET LOGIC: Show all items in the database to everyone
    items = PantryItem.objects.all().order_by('expiry_date')
    
    return render(request, 'tracker/dashboard.html', {
        'items': items,
        'quick_items': quick_list,
        'today': today_date,
    })


