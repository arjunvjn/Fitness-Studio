from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import CustomUser
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    '''
    Create a refresh token and a access token for the user.

    HTTP Method:
        POST

    Request Data:
        - email (str): The email address of the user (must be unique).
        - password (str): The password for the new account.

    Responses:
        - Success: If the user is found in the database, returns the access 
          and refresh token.
        - Error: In case of any issues (such as invalid email or password), 
          returns with a detailed error message.
    '''
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def create_account(request):
    '''
    Create a new user account for users and instructors.

    HTTP Method:
        POST
    
    Request Data:
        - name (str): The name of the user.
        - email (str): The email address of the user (must be unique).
        - password (str): The password for the new account.
        - role (str): The role of the user (e.g., "user" or "instructor").

    Responses:
        - Success: If the user is created successfully, returns a status of "Success" 
          along with the serialized user data.
        - Error: If validation fails, returns a status of "Error" along with validation 
          errors.
        - Exception: In case of an unexpected error, returns a status of "Error" 
          with the exception message.
    '''
    try:
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            CustomUser.objects.create_user(**serializer.validated_data)
            user_data = serializer.data
            user_data.pop('password')
            return Response({"status":"Success", "data":user_data}, status=status.HTTP_201_CREATED)
        return Response({"status":"Error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    '''
    Log out the user by blacklisting the refresh token.
    
    This view allows an authenticated user to log out by blacklisting their 
    refresh token. The user must include their access token in the request 
    headers to authenticate the request.

    HTTP Method:
        POST

    Request Data:
        - refresh_token (str): The refresh token of the signed in user.

    Responses:
        - Success: Returns a status of "Success" and a message confirming 
          the user is logged out.
        - Error: In case of any issues (such as missing or invalid refresh 
          token), returns a status of "Error" with a detailed error message.
    '''
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"status":"Success", "message":"User is logged out"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status":"Error", "data":str(e)}, status=status.HTTP_400_BAD_REQUEST)