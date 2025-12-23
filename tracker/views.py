from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta # Required for adding days
from .models import PantryItem

def dashboard(request):
    # 1. Define items and their shelf life (in days)
    quick_add_config = {
        "Milk": 7,
        "Eggs": 14,
        "Bread": 7,
        "Butter": 30,
        "Apples": 10
    }
    
    quick_list = list(quick_add_config.keys())
    today_date = timezone.now().date()
    
    if request.method == "POST":
        name = request.POST.get('name')
        expiry = request.POST.get('expiry_date')
        quick_item = request.POST.get('quick_item')

        # Handle Custom Add
        if name and expiry:
            PantryItem.objects.create(name=name, expiry_date=expiry)
            return redirect('dashboard')

        # Handle Quick Add with varied expiry dates
        elif quick_item:
            # Get the days from our config, default to 1 if not found
            days_to_add = quick_add_config.get(quick_item, 1)
            calculated_expiry = today_date + timedelta(days=days_to_add)
            
            PantryItem.objects.create(
                name=quick_item, 
                expiry_date=calculated_expiry
            )
            return redirect('dashboard')

    items = PantryItem.objects.all().order_by('expiry_date')
    return render(request, 'tracker/dashboard.html', {
        'items': items,
        'quick_items': quick_list,
        'today': today_date,
    })

def finish_item(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)
    item.delete()
    return redirect('dashboard')

