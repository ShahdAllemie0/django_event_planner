from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView,RetrieveUpdateAPIView
from events.models import Event,EventGuest
from .serializers import (SignUpSerializer,EventSerializer,CreateEventSerializer,
OrganizerSerializer,BookingSerializer,EventUpdateSerializer,GuestEventSerializer,GuestSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from datetime import datetime
from .permissions import IsGuest, IsOwner


class SignUp(CreateAPIView):
	serializer_class = SignUpSerializer


class EventView(ListAPIView):
	queryset =  Event.objects.filter(date__gt=datetime.today())
	serializer_class = EventSerializer
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields = ['title', 'description','organizer__username']


class CreateEventView(CreateAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = CreateEventSerializer
	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)


class GuestEvent(ListAPIView):
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated, IsGuest]

	def get_queryset(self):
		query = EventGuest.objects.filter(guest=self.request.user)
		return query


class UpdateEventView(RetrieveUpdateAPIView):
	queryset =  Event.objects.all()
	serializer_class = EventUpdateSerializer
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'


class OrganizerView(ListAPIView):
	serializer_class = OrganizerSerializer
	queryset= Event.objects.all()
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields = ['title', 'description','organizer__username']


class BookView(CreateAPIView):
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated,]
	def perform_create(self,serializer):
		serializer.save(guest=self.request.user, event_id=self.kwargs['event_id'])


class GuestView(RetrieveAPIView):
	serializer_class = GuestEventSerializer
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	queryset=Event.objects.all()
