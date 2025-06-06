from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from datetime import datetime
import pytz
from django.db.models import Q, Count

from .models import FitnessClass, ClassSlot
from core.permissions import IsInstructor, IsUser
from .serializers import FitnessClassSerializer, ClassSlotSerializer
from class_booking.models import ClassBooking

# Create your views here.
@api_view(['POST'])
@permission_classes([IsInstructor])
def create_fitness_class(request):
    '''
    Create a new class for the logged in instructor.

    The user must include their access token in the request 
    headers to authenticate the request.

    HTTP Method:
        POST
    
    Request Data:
        - name (str): The name of the class (must be unique).
        - class_type (str): The type of class (e.g., yoga, zumba or hiit).
        - date (str): The class date (must be in yyyy-mm-dd format).
        - member_max_count (int): Maximum allowed members for each slot.
        - slots (list of objects): Contains the start time and end time of 
          each slot as an object in the list.
              - start (str): The start time of slot.
               - end (str): The end time of slot.

    Responses:
        - Success: If the class is created successfully, returns a status of "Success" 
          along with the message.
        - Error: If validation fails, returns a status of "Error" along with validation 
          errors.
        - Exception: In case of an unexpected error, returns a status of "Error" 
          with the exception message.
    '''
    try:

        # IST timezone
        ist = pytz.timezone('Asia/Kolkata')
        today_date_ist = datetime.now(ist).date()
        date_obj = datetime.strptime(request.data['date'], '%Y-%m-%d').date()
        if date_obj > today_date_ist:

            serializer = FitnessClassSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(instructor=request.user)
                for slot in request.data['slots']:
                    start = datetime.strptime(slot['start'], '%H:%M').time()
                    end = datetime.strptime(slot['end'], '%H:%M').time()
                    ClassSlot.objects.create(fitness_class=serializer.instance, start_time=start, end_time=end)
                return Response({"status":"Success", "message":"Class Created"}, status=status.HTTP_201_CREATED)
            return Response({"status":"Error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status":"Error", "message":"Date must be tomorrow or later."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsUser])
def get_available_classes(request):
    '''
    Get the details of all available class slots.

    The user must include their access token in the request 
    headers to authenticate the request. If the user is logging 
    from different timezone, then that timezone is passed as 
    query param.

    HTTP Method:
        GET

    Responses:
        - Success: Returns a success status along with all available class slots 
          and their corresponding details.
        - Exception: In case of an unexpected error, returns a status of "Error" 
          with the exception message.
    '''
    try:
        # IST timezone
        ist = pytz.timezone('Asia/Kolkata')
        today_ist = datetime.now(ist)
        today_date_ist = today_ist.date()
        today_time_ist = today_ist.time()

        # For getting class id's that starts tomorrow or later.
        upcoming_classes = FitnessClass.objects.filter(date__gt=today_date_ist).values_list('id', flat=True)
        print(upcoming_classes)

        # For getting class id's that is today but not has begun.
        today_classes = FitnessClass.objects.filter(date=today_date_ist).values_list('id', flat=True)
        print(today_classes)

        # For getting slots that hasn't started yet.
        available_slots = ClassSlot.objects.select_related('fitness_class').filter(
            Q(fitness_class__id__in=upcoming_classes) |
            Q(fitness_class__id__in=today_classes, start_time__gt=today_time_ist)
        )
        print(available_slots)

        # For getting the number of bookings for each slot.
        booked_slots_count = ClassBooking.objects.values('class_slot').annotate(booked_slot_count=Count('user')).values('class_slot__id', 'booked_slot_count')
        print(booked_slots_count)

        # For checking if any of the available_slots has max bookings reached.
        new_available_slots = []
        for slot in available_slots:
            current_slot = list(filter(lambda s: s['class_slot__id'] == slot.id, booked_slots_count))
            if current_slot:
                print(current_slot[0]['booked_slot_count'])
                print(slot.fitness_class.member_max_count)
                if slot.fitness_class.member_max_count != current_slot[0]['booked_slot_count']:
                    new_available_slots.append(slot)
            else:
                new_available_slots.append(slot)

        # For checking the entered timezone is valid.
        try:
            pytz.timezone(request.query_params.get('timezone'))
            serializer = ClassSlotSerializer(new_available_slots, many=True, target_timezone=request.query_params.get('timezone'))
        except pytz.UnknownTimeZoneError:     
            serializer = ClassSlotSerializer(new_available_slots, many=True)

        return Response({"status":"Success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)