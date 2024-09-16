from django.contrib import admin
from .models import Student, Room, Seat,StudentSeatHistory

admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Seat)
admin.site.register(StudentSeatHistory)

