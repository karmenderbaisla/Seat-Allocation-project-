from django.urls import path
from .views import StudentAPI,RoomAPI,StudentSeatHistoryAPI,RoomChangeAPI

urlpatterns = [
    path('student/', StudentAPI.as_view()),
    path('room/', RoomAPI.as_view()),
    path('StudentSeatHistory/', StudentSeatHistoryAPI.as_view()),
    path('RoomChange/', RoomChangeAPI.as_view()),
    

 
]