from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PantryItem

def dashboard(request):
    quick_list = ["Milk", "Eggs", "Bread", "Butter", "Apples"]
    today_date = timezone.now().date()
    
    if not request.user.is_authenticated:
        return render(request, 'tracker/dashboard.html', {
            'items': [], 
            'quick_items': quick_list,
            'today': today_date
        })

    if request.method == "POST":
        name = request.POST.get('name')
        expiry = request.POST.get('expiry_date')
        quick_item = request.POST.get('quick_item')

        if name and expiry:
            PantryItem.objects.create(user=request.user, name=name, expiry_date=expiry)
            return redirect('dashboard')
        elif quick_item:
            PantryItem.objects.create(user=request.user, name=quick_item, expiry_date=today_date)
            return redirect('dashboard')

    items = PantryItem.objects.filter(user=request.user).order_by('expiry_date')
    return render(request, 'tracker/dashboard.html', {
        'items': items,
        'quick_items': quick_list,
        'today': today_date,
    })

