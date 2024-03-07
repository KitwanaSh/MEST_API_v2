from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth   import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets, status
from .models import *
from .serializers import *
from API_v2.utils import *

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username =request.data.get("username")
    first_name = request.data.get("first_name")
    last_name =request.data.get("last_name")
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")

    new_user = IMUser.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
    )
    new_user.set_password(password)
    new_user.save()
    # new_user.generate_auth_token()
    serializer = AuthSerializer(new_user, many=False)
    return Response({"message": "Account successfully created", "result": serializer.data})


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    #1 Receive inputs/data from client and validate inputs
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"detail": "My friend behave yourself and send me username and password"}, status.HTTP_400_BAD_REQUEST)
    
    #2 check user existence
    try:
        user = IMUser.objects.get(username=username)

        # Check if the user is active
        if not user.is_active:
            return Response({"message": "Your account is inactive"}, status.HTTP_403_FORBIDDEN)
        #3 user authentication
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            login(request, user)
            # Reset the temporal_login_fail counter if the login was successful
            if user.temporal_login_fail > 0:
                user.temporal_login_fail = 0
                user.save()
            serializer = AuthSerializer(user, many=False)
            return Response({"Result": serializer.data})
        else:
            # Increase the temporal_login_fail counter if the login was not successful
            user.temporal_login_fail += 1
            user.save()
            return Response({"detail": "Invalid credentials"}, status.HTTP_400_BAD_REQUEST)
        #5 respond to the users request
    except IMUser.DoesNotExist:
        return Response({"detail": "Username does not exist"}, status.HTTP_400_BAD_REQUEST)
    

class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        #1. Receive the username (email)
        username = request.data.get("username")
        if not username:
            return generate_400_response("Username is required")
        #2. Check if the user exists
        try:
            user = IMUser.objects.get(username=username)
            otp_code = generate_unique_code()
            user.unique_code = otp_code
            user.save()
        
        #3. Send OTP code

        #4.. Respond to the user
            return Response({"detail": "OTP code has been sent to your email"}, status.HTTP_200_OK)
        except IMUser.DoesNotExist:
            return generate_400_response("Username is does not exist")

    