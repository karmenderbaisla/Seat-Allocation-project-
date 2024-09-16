from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=55) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.name
    

class Seat(models.Model):
    
    seat_no= models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.seat_no}"
    
class Student(models.Model):
    name = models.CharField(max_length=55)
    email = models.EmailField(unique=True)
    room= models.ForeignKey(Room, related_name="students", on_delete=models.CASCADE)
    seat=models.ForeignKey(Seat, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    


class StudentSeatHistory(models.Model):
    student = models.ForeignKey(Student,related_name="seat_history", on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.start_date}"
