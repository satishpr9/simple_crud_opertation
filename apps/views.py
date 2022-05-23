from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from apps.models import Category, Product, Profile
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
	obj=Category.objects.all()
	obj1=None
	categoryid=request.GET.get('category')
	if categoryid:
		obj1=Product.get_all_products_by_id(categoryid)
	else:
		obj1=Product.objects.all()
	context={
		'obj':obj,
		'obj1':obj1
	}

	
	
	return render(request,"index.html",context)



def profile(request, username):
	user = User.objects.filter(username=username)
	if user:
		user = user[0]
		profile = Profile.objects.get(user=user)
		first_name=profile.first_name
		last_name=profile.last_name
		mobile=profile.mobile_no
		data = {
            'obj':user,
			'first':first_name,
			'second':last_name,
			'mobile':mobile

            
        }
	else: 
		return HttpResponse('no such user')

	return render(request, 'profile.html', data)

@login_required
def update_profile(request):
    if request.method=="POST":
        user_form=UserUpdateForm(data=request.POST or None, instance=request.user)
        profile_form=ProfileUpdateForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form=UserUpdateForm(instance=request.user) 
        profile_form=ProfileUpdateForm(instance=request.user.profile)    
    context ={
        'u_form':user_form,
        'p_form':profile_form,
    }       

    return render(request,'update_profile.html', context)


def category(request):
	obj=Category.objects.all()
	obj1=None
	categoryid=request.GET.get('category')
	if categoryid:
		obj1=Product.get_all_products_by_id(categoryid)
	else:
		obj1=Product.objects.all()
	context={
		'obj':obj,
		'obj1':obj1
	}
	return render(request,"Category.html",context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully created for {username}! Login In Now')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				# messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"form":form})


def logout_request(request):
	logout(request)
	# messages.info(request, "You have successfully logged out.") 
	return redirect("index")


def delete(request, id):
	data=Product.objects.filter(id=id)
	data.delete()
	return redirect('category')

razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def homepage(request):
	currency = 'INR'
	amount = 10000 # Rs. 100

	
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'


	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url

	return render(request, 'paynow.html', context=context)



@csrf_exempt
def paymenthandler(request):

	
	if request.method == "POST":
		try:
		
			
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
				amount = 10000 
				try:

					
					razorpay_client.payment.capture(payment_id, amount)

					
					return render(request, 'success.html')
				except:

					
					return render(request, 'fail.html')
			else:

			
				return render(request, 'fail.html')
		except:

			
			return HttpResponseBadRequest()
	else:
	
		return HttpResponseBadRequest()