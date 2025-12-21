from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PantryItem

# Mock/Import your RECIPES dictionary if it's in another file
# from .constants import RECIPES 

def dashboard(request):
    # 1. GATEKEEPER: Setup basic data for everyone (logged in or not)
    quick_list = ["Milk", "Eggs", "Bread", "Butter", "Apples"]
    
    # 2. CHECK LOGIN: If not logged in, show an empty dashboard safely
    if not request.user.is_authenticated:
        context = {
            'items': [], # No items for anonymous users
            'quick_items': quick_list,
            'today': timezone.now().date(),
        }
        return render(request, 'tracker/dashboard.html', context)

    # 3. POST LOGIC: Handle adding items (Only for logged-in users)
    if request.method == "POST":
        name = request.POST.get('name')
        expiry = request.POST.get('expiry')
        quick_item = request.POST.get('quick_item')

        if name and expiry:
            PantryItem.objects.create(
                user=request.user,
                name=name,
                expiry_date=expiry
            )
            return redirect('dashboard')

        elif quick_item:
            PantryItem.objects.create(
                user=request.user,
                name=quick_item,
                expiry_date=timezone.now()
            )
            return redirect('dashboard')

    # 4. GET LOGIC: Loading items & Recipe Logic
    items = PantryItem.objects.filter(user=request.user, is_consumed=False)

    # Your Recipe Suggestion Logic
    for item in items:
        # This assumes status_category() is a method in your Model
        if hasattr(item, 'status_category') and item.status_category() == "Expired":
            # Replace 'RECIPES.get' with your actual recipe logic
            item.recipe = "Suggestion: Use in compost or check safety." 
        else:
            item.recipe = None

    context = {
        'items': items,
        'quick_items': quick_list,
        'today': timezone.now().date(),
    }
    
    return render(request, 'tracker/dashboard.html', context)

def finish_item(request, pk):
    # Security: Ensure you only finish your own items
    item = get_object_or_404(PantryItem, pk=pk, user=request.user)
    item.is_consumed = True
    item.save()
    return redirect('dashboard')

