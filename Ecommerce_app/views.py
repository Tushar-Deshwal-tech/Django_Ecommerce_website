from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import UserData, OrderData, OrderItem, ReviewData
from django.utils import timezone
from django.db import IntegrityError
import pytz
import re
import json

with open('products_data.json', 'r') as file:
    products_data = json.load(file)

def format_currency(amount):
    return "₹{:,.2f}".format(amount)

def index(request):
    username = request.session.get('user_firstname')
    return render(request, "index.html", {"username": username})

def products(request, category):
    usercategory = choice_category(category)
    username = request.session.get('user_firstname')
    if category == "all":
        return render(request, "products.html", {"detail": products_data, "username": username})
    else:
        return render(request, "products.html", {"detail": usercategory, "username": username})

def choice_category(option):
    filtered_products = [item for item in products_data if option == item["category"]]
    return filtered_products
 
def item(request, category, id):
    selected_item = None
    username = request.session.get('user_firstname')
    for category_data in products_data:
        for item in category_data['data']:
            if item['category'] == category and item['id'] == id:
                selected_item = item
                break
    return render(request, "item.html", {"selected_item": selected_item, "username": username})

def cart(request):
    username = request.session.get('user_firstname')
    cart_list = request.session.get('cart_list', [])
    return render(request, "cart.html", {"cart": cart_list, "username": username})

def add_to_cart(request, category, id):
    if request.method == 'POST':
        final_size = request.POST.get('final_size')
        final_color = request.POST.get('final_color')
        selected_item = None
        if not request.session.get('user_firstname'):
            messages.error(request, "Uh-oh! You need to log in first to add items to your cart. Let's get you logged in!")
            return redirect('login_page')
        else:
            for category_data in products_data:
                for item in category_data['data']:
                    if item['category'] == category and item['id'] == id:
                        item['size'] = final_size
                        item['color'] = final_color
                        selected_item = item
                        break
            if selected_item:
                cart_list = request.session.get('cart_list', [])
                if selected_item not in cart_list:
                    cart_list.append(selected_item)
                    messages.success(request, "Success! Your item has been added to the cart. Ready to proceed to checkout?")
                else:
                    messages.error(request, "Oops! It seems this item is already in your cart. Double-check before adding.")
                request.session['cart_list'] = cart_list
            else:
                messages.error(request, "Sorry, we couldn't find the selected item.")
        return redirect('item', category=selected_item['category'], id=selected_item['id'])


def remove_from_cart(request, category, id):
    cart_list = request.session.get('cart_list', [])
    selected_item = None
    for category_data in products_data:
        for item in category_data['data']:
            if item['category'] == category and item['id'] == id:
                selected_item = item
                break
    if selected_item in cart_list:
        cart_list.remove(selected_item)
        request.session['cart_list'] = cart_list
        messages.warning(request, "Success! The item has been removed from your cart. Keep shopping!")
    else:
        messages.error(request, "Oops! It seems this item is not in your cart. Double-check your selection.")
    return redirect('cart')


def wishlist(request):
    username = request.session.get('user_firstname')
    wishlist_list = request.session.get('wishlist_list', [])
    return render(request, "wishlist.html", {"wishlist": wishlist_list, "username": username})

def add_to_wishlist(request, category, id):
    selected_item = None
    if not request.session.get('user_firstname'):
            messages.error(request, "Uh-oh! You need to log in first to add items to your Wishlist. Let's get you logged in!")
            return redirect('login_page')
    else:
        for category_data in products_data:
            for item in category_data['data']:
                if item['category'] == category and item['id'] == id:
                    selected_item = item
                    break
        wishlist_list = request.session.get('wishlist_list', [])
        if selected_item not in wishlist_list:
            wishlist_list.append(selected_item)
            messages.success(request, "Success! Your item has been added to the Wishlist!")
        else:
            messages.error(request, "Oops! It seems this item is already in your cart.")
        request.session['wishlist_list'] = wishlist_list
    return redirect('item',category=selected_item['category'],id=selected_item['id'])

def remove_from_wishlist(request, category, id):
    wishlist_list = request.session.get('wishlist_list', [])
    selected_item = None
    for category_data in products_data:
        for item in category_data['data']:
            if item['category'] == category and item['id'] == id:
                selected_item = item
                break
    if selected_item in wishlist_list:
        wishlist_list.remove(selected_item)
        request.session['wishlist_list'] = wishlist_list
        messages.warning(request, "Success! The item has been removed from your wishlist.")
    else:
        messages.error(request, "Oops! It seems this item is not in your Wishlist.")
    return redirect('wishlist')

def add_cart_from_wishlist(request, category, id):
    cart_list = request.session.get('cart_list', [])
    wishlist_list = request.session.get('wishlist_list', [])
    selected_item = None
    for category_data in products_data:
        for item in category_data['data']:
            if item['category'] == category and item['id'] == id:
                selected_item = item
                break
    if selected_item not in cart_list:
        cart_list.append(selected_item)
        wishlist_list.remove(selected_item)
        request.session['cart_list'] = cart_list
        request.session['wishlist_list'] = wishlist_list
        messages.success(request, "Item successfully moved from wishlist to cart!")
        return redirect("cart")
    else:
        messages.error(request, "Item is already in your cart. You can proceed to the cart.")
        return redirect("wishlist")

def orders(request):
    username = request.session.get('user_firstname')
    database_orders = OrderData.objects.filter(order_by=username)
    order_data = []
    for order in database_orders:
        order_items = order.order_items.all()
        order_data.append({'order': order, 'order_items': order_items})
    return render(request, "orders.html", {"order_data": order_data, "username": username})

def order_confirmation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('order_data'))
            old_order_number = OrderData.objects.last()
            order_items = []
            # Create order items
            for item_data in data['allItemsDetails']:
                order_item = OrderItem(
                    order_id=None,  # Initialize order_id to None
                    item_name=item_data['itemName'],
                    item_price=item_data['itemPrice'],
                    item_quantity=item_data['itemQuantity'],
                    item_size=item_data['itemSize'],
                    item_color=item_data['itemColor'])
                order_items.append(order_item)
            try:
                order_time = timezone.now()
                new_orderdata = OrderData.objects.create(
                    order_by=request.session.get('user_firstname'),
                    order_number=old_order_number.order_number + 1 if old_order_number else 1,
                    order_status="order_placed",
                    total_item=len(data['allItemsDetails']),
                    payment_method=data['payment_method'],
                    total_price=data['total'],
                    order_time=order_time)
                for order_item in order_items:
                    order_item.order_id = new_orderdata.id
                    order_item.save()
                    request.session['cart_list'] = []
                messages.success(request, "Success! Your order has been placed successfully. Thank you for shopping with us!")
                return redirect('orders')
            except Exception as e:
                messages.error(request, "Oops! Something went wrong while processing your order. Please try again later.")
                return redirect('cart')
        except Exception as e: 
            messages.error(request, "Oops! Something went wrong while processing your order. Please try again later.")
            return redirect('cart')
    return redirect('index')


def login_page(request):
 return render(request, "login.html")

def login_verify(request):
    if request.method == 'POST':
        login_email = request.POST.get('login-email')
        login_password = request.POST.get('login-password')
        # Check if the user is an admin
        admin = authenticate(request, username=login_email, password=login_password)
        if admin is not None and admin.is_superuser:
           messages.success(request, "Admin login successful.")
           return redirect('admin_page')
        # Check if the user is a normal user
        user = authenticate(request, email=login_email, password=login_password)
        if user is not None:
            messages.success(request, 'Welcome back! You have successfully logged in.')
            request.session['user_firstname'] = user.first_name
            return redirect('index')
        if UserData.objects.filter(email=login_email).exists(): 
            try:
                user = UserData.objects.get(email=login_email)
                if user.password != login_password:
                    messages.error(request, 'Incorrect password. Please try again.')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred! Please try again later.')
        else:
            messages.error(request, 'Account not found. Please sign up first.')
    return redirect('login_page')

def logout_user(request):
    if 'user_firstname' in request.session:
        del request.session['user_firstname']
    messages.success(request, 'You have been successfully logged out. See you again soon!')
    return redirect('login_page')

def signup_page(request):
    return render(request, "signup.html")

def signup_user(request):
    if request.method == 'POST':
        signup_firstname = request.POST.get('signup-first-name').lower()
        signup_lastname = request.POST.get('signup-last-name').lower()
        signup_number = request.POST.get('signup-number')
        signup_email = request.POST.get('signup-email')
        signup_password = request.POST.get('signup-password')
        try:
            CustomPasswordValidator().validate_password(signup_password)
        except ValidationError as e:
            for error_msg in e.messages:
                messages.error(request, error_msg)
            return redirect('signup_page')
        if UserData.objects.filter(email=signup_email).exists():
            messages.warning(request, 'This email address is already in use. Please enter a different email.')
            return redirect('signup_page')
        if UserData.objects.filter(mobile_number=signup_number).exists():
            messages.warning(request, 'This phone number is already in use. Please enter a different number.')
            return redirect('signup_page')
        try:
            new_userdata = UserData(
                    first_name=signup_firstname,
                    last_name=signup_lastname,
                    mobile_number=signup_number,
                    email=signup_email,
                    password=signup_password)
            new_userdata.save()
            messages.success(request, 'Hooray! Your account has been created successfully. Happy shopping!')
            return redirect('login_page')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred. {e}: Please try again later.')
    return redirect('signup_page')

def review(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        rating = request.POST.get('rating', '').strip()
        print(rating)
        if not (message and rating):
            messages.error(request, 'Please provide both message and rating.')
            return redirect('index')
        
        if request.session.get('user_firstname'):
            try:
                existing_reviews = ReviewData.objects.filter(user_name=request.session.get('user_firstname'))
                # if existing_reviews.exists():
                #     messages.error(request, 'You have already submitted a review.')
                # else:
                new_review = ReviewData(
                    user_name=request.session.get('user_firstname'),
                    text=message,
                    star=rating
                )
                # print(new_review.start)
                new_review.save()
                messages.success(request, 'Your review has been submitted successfully. Thank you for your feedback!')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}. Please try again later.')
        else:
            messages.error(request, 'You need to log in first to submit the review!.')
        return redirect('index')

class CustomPasswordValidator:
    def validate_password(self, password, user=None):
        if len(password) < 6:
            raise ValidationError("The password must be at least 6 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("The password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("The password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise ValidationError("The password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()_+<>?/]', password):
            raise ValidationError("The password must contain at least one special character.")
    def get_help_text(self):
        return ""

user_data = UserData.objects.all()
order_details = OrderData.objects.all()
review_data = ReviewData.objects.all()

def getdata():
    total_category = len(products_data)
    total_products = sum(len(category['data']) for category in products_data)
    return total_products, total_category

def admin_page(request):
    username = request.session.get('user_firstname')
    return render(request, "admin/admin.html", {"username": username, "review_data": review_data, "order_details": order_details})

def edit_page(request):
    item_detail = getdata()
    return render(request, "admin/edit.html", {"item_detail": item_detail})

def show_products(request, category):
    admincategory = choice_category(category)
    item_detail = getdata()
    return render(request, "admin/edit.html", {"data": admincategory, "item_detail": item_detail})

def user_page(request):
    return render(request, "admin/user.html", {"user_data": user_data})

def delete_user(request, userid):
    try:
        user = UserData.objects.get(id=userid)
        user.delete()
        messages.success(request, "User Delete successfully")
    except Exception as e:
        messages.error(request, {e})
    return redirect(request, 'user_page')
