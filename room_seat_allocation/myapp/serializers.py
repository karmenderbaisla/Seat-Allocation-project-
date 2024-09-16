from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    seat = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())
    room_name = serializers.PrimaryKeyRelatedField(source="room.name",read_only=True)
    class Meta:
        model = Student
        fields = ['name', 'email','seat','room','room_name', 'created_at', 'updated_at','seat']

    def get_seat(self,data):
        return data.seat.seat_no   

    def create(self, validated_data):
        room = validated_data.get('room')
        seat = validated_data.get('seat') 
        student = super().create(validated_data)

        StudentSeatHistory.objects.create(
            student=student,
            seat=seat,
            room=room,
            start_date=timezone.now().date()
        )
        
        return student

class RoomSerializer(serializers.ModelSerializer):
    students_count = serializers.IntegerField(read_only=True)   
    class Meta:
        model = Room
        fields = ['name','students_count','created_at', 'updated_at']

class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = ['student', 'room', 'created_at', 'updated_at']

    # def validate(self, data):
    #     student = data.get('student')
    #     room = data.get('room')
    #     seat_id = data.get('id')


class StudentSeatHistorySerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(source='student.name', read_only=True)
    room = serializers.PrimaryKeyRelatedField(source='room.name', read_only=True)

    
    class Meta:
        model = StudentSeatHistory
        fields = ['student', 'room', 'seat_id', 'created_at','start_date']


class RoomChangeSerializer(serializers.Serializer):
    student_name=serializers.CharField(max_length=55)
    new_room=serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    new_seat=serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())    

    class Meta:
        fields=['student_name','new_room','new_seat']


    def validate(self, data):
        student_name=data.get('student_name')
        new_room=data.get('new_room')
        new_seat=data.get('new_seat')

        if not Student.objects.filter(name=student_name).exists():
            student_instance = Student.objects.get(name=student_name)

            StudentSeatHistory.objects.create(
                student=student_instance,
                seat=new_seat,
                room= new_room,
                start_date=timezone.now().date()

            )
            return data
        else:
            raise serializers.ValidationError("This Student Does not exist in the list")
        if not Room.objects.filter(id=new_room.id).exists():
            raise serializers.ValidationError(" new room does not exist")
        if not Seat.objects.filter(id=new_seat.id).exists():
            raise serializers.ValidationError("new seat Does not exist in the list")
        
        return data     