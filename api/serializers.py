from rest_framework import serializers
from django.contrib.auth.models import User
from events.models import Event,EventGuest


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']


class SignUpSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		new_user = User(username=username, first_name=first_name, last_name=last_name)
		new_user.set_password(password)
		new_user.save()
		return validated_data


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'


class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['title', 'date', 'time','location','description']


class EventUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['title', 'date', 'time','location','description']


class OrganizerSerializer(serializers.ModelSerializer):
	organizer= serializers.SerializerMethodField()

	class Meta:
		model= Event
		fields=['organizer','title', 'date','time','location', 'seats']

	def get_organizer(self, obj):
		return obj.organizer.username


class BookingSerializer(serializers.ModelSerializer):
	event = serializers.SerializerMethodField()

	class Meta:
		model= EventGuest
		exclude=['guest']

	def get_event(self, obj):
		return (obj.event.title)


class GuestSerializer(serializers.ModelSerializer):
	guest=serializers.SerializerMethodField()

	class Meta:
		model= EventGuest
		fields=['guest']

	def get_guest(self, obj):
		return (obj.guest.first_name+" "+obj.guest.last_name)


class GuestEventSerializer(serializers.ModelSerializer):
		guests=serializers.SerializerMethodField()
		class Meta:
			model=Event
			fields=['title', 'date', 'time', 'guests',]

		def get_guests(self,obj):
			myevent = EventGuest.objects.all()
			return GuestSerializer(myevent,many=True).data
