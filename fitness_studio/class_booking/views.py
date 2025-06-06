from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from datetime import datetime
import pytz
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsUser
from .models import ClassBooking
from fitness_class.models import ClassSlot
from .serializers import ClassBookingSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([IsUser])
def book_slot(request, slot_id):
    '''
    Create a new record in ClassBooking table for the logged in user.

    The user must include their access token in the request 
    headers to authenticate the request. The id of the slot to be booked
    should be passed with the url.

    HTTP Method:
        POST
    
    Responses:
        - Success: If the slot is booked successfully, returns a status of "Success" 
          along with the message.
        - Error: If the class is filled or the class has past current date or time, 
          returns a status of "Error" along with error message.
        - Exception: In case of an unexpected error, returns a status of "Error" 
          with the exception message.
    '''
    try:
        # IST timezone
        ist = pytz.timezone('Asia/Kolkata')
        # Current datetime in IST
        today_ist = datetime.now(ist)
        today_date_ist = today_ist.date()
        today_time_ist = today_ist.time()

        slot = ClassSlot.objects.select_related('fitness_class').get(id=slot_id)
        if (slot.fitness_class.date == today_date_ist and slot.start_time > today_time_ist) or (slot.fitness_class.date > today_date_ist):
            slot_booking_count = ClassBooking.objects.filter(class_slot=slot).count()
            if slot.fitness_class.member_max_count > slot_booking_count:
                ClassBooking.objects.create(class_slot=slot, user=request.user)
                return Response({"status":"Success", "message":"Slot Booked"}, status=status.HTTP_201_CREATED)
            return Response({"status":"Error", "message":"This Class has already been filled"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status":"Error", "message":"This Class has already been finished or ongoing"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booking_details(request):
    '''
    Get the details of booked slots.

    The user must include their access token in the request 
    headers to authenticate the request. If the user is logging 
    from different timezone, then that timezone is passed as 
    query param.

    HTTP Method:
        GET
    
    Request Data:
        - email (str): The email of the user (not mandatory).

    Responses:
        - Success: If an email_id is provided in the request data, the response 
          will return a status of Success along with the corresponding booking 
          details of that email user. If no email_id is provided, the response 
          will return a status of 'Success' with the booking details of the 
          currently signed-in user.
        - Exception: In case of an unexpected error, returns a status of "Error" 
          with the exception message.
    '''
    try:
        if request.data.get('email'):
            bookings = ClassBooking.objects.filter(user__email=request.data.get('email'))
        else:
            bookings = ClassBooking.objects.filter(user__id=request.user.id)

        # For checking the entered timezone is valid.
        try:
            pytz.timezone(request.query_params.get('timezone'))
            serializer = ClassBookingSerializer(bookings, many=True, target_timezone=request.query_params.get('timezone'))
        except pytz.UnknownTimeZoneError:     
            serializer = ClassBookingSerializer(bookings, many=True)
            
        return Response({"status":"Success", "data":serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)