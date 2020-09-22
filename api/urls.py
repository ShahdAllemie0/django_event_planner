from django.urls import path
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', views.SignUp.as_view(), name='api-signup'),
    path('api/event/', views.EventView.as_view(), name='api-event'),
    path('api/create/', views.CreateEventView.as_view(), name='api-create'),
    path('api/organizer/event/', views.OrganizerView.as_view(), name='api-organizer-event'),
    path('api/update/events/<int:event_id>/', views.UpdateEventView.as_view(), name='api-update-even'),
    path('api/guest/event/', views.GuestEvent.as_view(), name='api-guest-event'),
	path('api/<int:event_id>/guest/', views.GuestView.as_view(), name='api-guest'),
	path('api/<int:event_id>/book/', views.BookView.as_view(), name='api-book-event'),
    



]
