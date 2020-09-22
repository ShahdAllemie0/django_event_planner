from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin,EventForm,EvenGuestForm,UserProfile
from django.contrib import messages
from .models import Event,EventGuest
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q


from django.shortcuts import render

def get_user_profile(request, username):
	user = User.objects.get(username=username)
	return render(request, 'user_profile.html', {"user":user})



def home(request):
	return render(request, 'home.html')
# '''''''dashboard'''''''
def dashboard(request):
	events = Event.objects.filter(organizer=request.user)
	# guests = EventGuest.objects.filter(event__id__in=events)
	context = {
		"events": events,
		# "guests":guests,
	}
	return render(request, 'dashboard.html', context)

def previous_event(request):
	guests = EventGuest.objects.filter(guest=request.user)
	context = {
		"guests":guests,
	}
	return render(request, 'previous_event.html', context)


# '''''Event stuff''''

def Events(request):
	events = Event.objects.filter(date__gt=datetime.today())
	query = request.GET.get('q')
	if query:
		events = events.filter(
				   Q(title__icontains=query)|
				   Q(description__icontains=query)|
				   Q(organizer__username__icontains=query)
					   ).distinct()


	context = {
		"events": events,
	}
	return render(request, 'event.html', context)


def EventDetail(request, event_id):
	event = Event.objects.get(id=event_id)
	guests = EventGuest.objects.filter(event=event)
	context = {
		"event": event,
		"guests":guests,
	}
	return render(request, 'event_detail.html', context)

def event_create(request):
	form = EventForm()
	if not request.user.is_authenticated:
		return redirect('signin')
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			event= form.save(commit=False)
			event.organizer = request.user
			event.save()
			messages.success(request, "Successfully Created!")
			return redirect('event')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_event.html', context)

def update_event(request, event_id):
	event = Event.objects.get(id=event_id)
	if request.user ==event.organizer:
		form = EventForm(instance=event)
		if request.method == "POST":
			form = EventForm(request.POST, request.FILES or None, instance=event)
			if form.is_valid():
				form.save()
				messages.success(request, "Successfully Edited!")
				return redirect('event')
			print (form.errors)
		context = {
		"form": form,
		"event": event,
		}
	else:
		return redirect('event')
	return render(request, 'update_event.html', context)

	# ''''''Guest staff''''''
def book_ticket(request, event_id):
	event_obj = Event.objects.get(id=event_id)
	form = EvenGuestForm()
	if not request.user.is_authenticated:
		return redirect('login')
	if request.method == "POST":
		form = EvenGuestForm(request.POST)
		if form.is_valid():
			book_from = form.save(commit=False)
			book_from.event = event_obj
			book_from.guest=request.user
			if event_obj.seats==0:
				messages.success(request, "FULL!")
				return redirect('event')
			event_obj.seats-=book_from.seats
			if event_obj.seats>=0:
				seat=event_obj.seats-book_from.seats
				event_obj.save()
				book_from.save()

				messages.success(request, "Successfully Booked!")
				return redirect('event')
			else:
				messages.success(request, "Try book less seats!!!")
				return redirect('book-ticket',event_obj.id)
			# return redirect('event-detail', event_obj.id)
		print (form.errors)
	context = {
	"form": form,
	"event": event_obj
	}
	return render(request, 'book_ticket.html', context)



# '''''Authentications'''''
class Signup(View):
	form_class = UserSignup
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully signed up.")
			login(request, user)
			return redirect("home")
		messages.warning(request, form.errors)
		return redirect("signup")


class Login(View):
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				messages.success(request, "Welcome Back!")
				events = Event.objects.filter(organizer=auth_user)
				if events:
					return redirect('dashboard')
				else:
					return redirect('event')

			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")
