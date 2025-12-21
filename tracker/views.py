from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PantryItem
from django.utils import timezone
from datetime import timedelta

RECIPES = {
    "Milk": "Make a milkshake or pancakes.",
    "Eggs": "Try a quick omelette or boiled eggs.",
    "Bread": "Make french toast or croutons.",
    "Chicken": "Roast it with herbs or make a stir-fry.",
    "Spinach": "Add to a smoothie or sauté with garlic.",
    "Default": "Check for a simple 15-minute recipe online!"
}

#@login_required
def dashboard(request):
    if request.method == "POST":
        # Capture inputs from both the custom form and quick buttons
        name = request.POST.get('name')
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
                expiry_date=timezone.now().date() + timedelta(days=7)
            )
            return redirect('dashboard')

    # --- GET request logic (Loading the page) ---
    items = PantryItem.objects.filter(user=request.user, is_consumed=False).order_by('expiry_date')
    
    # Recipe Logic: Suggests recipes for items that are RED (expiring soon)
    for item in items:
        if item.status_category() == "RED":
            item.recipe = RECIPES.get(item.name, RECIPES['Default'])
        else:
            item.recipe = None

    quick_list = ["Milk", "Eggs", "Bread", "Chicken", "Spinach", "Apples", "Bananas", "Cheese", "Butter", "Tomato"]

    context = {
        'items': items,
        'quick_items': quick_list,
        'today': timezone.now().date().isoformat(),
    }
    return render(request, 'tracker/dashboard.html', context)

#@login_required
def finish_item(request, pk):
    item = get_object_or_404(PantryItem, pk=pk, user=request.user)
    item.is_consumed = True
    item.save()
    return redirect('dashboard')
