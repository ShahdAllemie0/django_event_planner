from rest_framework.permissions import BasePermission

class IsGuest(BasePermission):
	message="You must be an Guest"

	def has_object_permission(self,request,view,obj):
		if request.user == obj.guest:
			return True
		else:
			return False

class IsOwner(BasePermission):		
	message="You must be the Event's Organizer"

	def has_object_permission(self,request,view,obj):
		if request.user == obj.organizer:
			return True
		else:
			return False
