from django.urls import path
from .views import Login, Logout, Signup, home
from events import views


urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('events/',views.Events, name='event'),
    path('events/<int:event_id>/', views.EventDetail, name='event-detail'),
    path('events/create/', views.event_create, name='event-create'),
    path('events/update/<int:event_id>/', views.update_event, name='event-update'),
    path('events/<int:event_id>/book_ticket/', views.book_ticket, name='book-ticket'),
    path('profile/<username>/', views.get_user_profile,name='profile'),
	path('dashboard/', views.dashboard,name='dashboard'),
	path('events/previous/', views.previous_event,name='previous-event'),








]
