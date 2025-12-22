from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PantryItem
from django.contrib.auth.models import User

def dashboard(request):
    # 1. Setup basic data
    quick_list = ["Milk", "Eggs", "Bread", "Butter", "Apples"]
    
    # 2. LOGIN CHECK: If not logged in, show an empty list
    if not request.user.is_authenticated:
        return render(request, 'tracker/dashboard.html', {
            'items': [], 
            'quick_items': quick_list,
            'today': timezone.now().date()
        })

    # 3. POST LOGIC: Capture data from your HTML forms
    if request.method == "POST":
        # 'name' matches your input name="name"
        name = request.POST.get('name') 
        # 'expiry_date' MUST match your HTML name="expiry_date"
        expiry = request.POST.get('expiry_date') 
        quick_item = request.POST.get('quick_item')

        # Logic for Custom Entry Box
        if name and expiry:
            PantryItem.objects.create(
                user=request.user,
                name=name,
                expiry_date=expiry
            )
            return redirect('dashboard')

        # Logic for Quick Add Buttons
        elif quick_item:
            PantryItem.objects.create(
                user=request.user,
                name=quick_item,
                expiry_date=timezone.now().date()
            )
            return redirect('dashboard')

    # 4. GET LOGIC: Fetch items specifically for USER1
    items = PantryItem.objects.filter(user=request.user).order_by('expiry_date')
    
    context = {
        'items': items,
        'quick_items': quick_list,
        'today': timezone.now().date(),
    }
    return render(request, 'tracker/dashboard.html', context)

def finish_item(request, pk):
    item = get_object_or_404(PantryItem, pk=pk, user=request.user)
    item.delete() # Or item.is_consumed = True if you have that field
    return redirect('dashboard')
