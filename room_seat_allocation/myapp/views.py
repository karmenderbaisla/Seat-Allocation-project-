from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import *
from .serializers import *
from django.db import transaction


class StudentAPI(APIView):    
    def get(self,request,pk=None):
        if pk is None:
            stu = Student.objects.all()
            serializer = StudentSerializer(stu, many=True) 
            return Response(serializer.data)# it return in dict form 
        else:
            stu = Student.objects.get(id=pk)
            serializer = StudentSerializer(stu,many=True)
            return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            slr= serializer.save()
            # room =serializer.validated_data.get('room')
            # seat =serializer.validated_data.get('seat')
            # StudentSeatHistory.objects.create(
            #     student=slr,
            #     seat=seat,
            #     room=room,
            #     start_date=timezone.now().date()

            # )

            return Response({'msg' :'Data Created'})
        return Response(serializer.errors)
    
#------------------------------------------------------------------------------------------------------------------
#revers relation 

class RoomAPI(APIView):
    def get(self,request,format=None):
        try:
            min_students = int(request.query_params.get('x',0))
        except ValueError:
            return Response({'errors':'invalid value of x ...'})
        
        Seats = Room.objects.annotate(students_count=Count('students')).filter(students_count__gte=min_students)
        serializer = RoomSerializer(Seats, many=True)
        return Response(serializer.data)
    
#---------------------------------------------------------------------------------------------------------------


class StudentSeatHistoryAPI(APIView):
    def get(self, request, format=None):
        history = StudentSeatHistory.objects.all()
        serializer = StudentSeatHistorySerializer(history, many=True)  
        return Response(serializer.data)
        
            
 #-------------------------------------------------------------------------------------------------------------
class RoomChangeAPI(APIView):
    @transaction.atomic     #ya toh puri hogi ya naa hogi , incomplete nhi rheti h ,for easy transaction 
    def patch(self,request):
        serializer = RoomChangeSerializer(data=request.data)
        if serializer.is_valid():
            student_name = serializer.validated_data.get('student_name')
            new_room=serializer.validated_data.get('new_room')
            new_seat= serializer.validated_data.get('new_seat')

            student = Student.objects.filter(name=student_name).first()
            if not student:
                return Response({'error': 'Student does not exist.'})
            
            student.room = new_room
            student.seat = new_seat
            student.save()

            return Response({'message': 'Student room updated '})
        return Response(serializer.errors)  
   