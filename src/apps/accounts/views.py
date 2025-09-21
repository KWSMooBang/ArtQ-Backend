from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer, ShowProfileSerializer, UpdateProfileSerializer

class RegistrationView(APIView):
    @extend_schema(
        tags=["auth"],
        operation_id="registration",
        description=(
            "Create a new user account.",
            "first_name, last_name, username, password, nickname are required fields.",
            "email or phone number are required for verification.",
            "birth_date is optional.",
        ),
        request=RegistrationSerializer,
        responses={
            201: OpenApiResponse(description="Register new user successfully."),
            400: OpenApiResponse(description="Bad Request"),
        },
        examples=[
            OpenApiExample(
                "Request example (email)",
                value={
                    'first_name': 'Gildong',
                    'last_name': 'Hong',
                    'username': 'loginID',
                    'password': 'loginPW',
                    'nickname': '홍길동',
                    'email': 'honggildong@example.com',
                    'birth_date': '1990-01-01',
                }
            ),
            OpenApiExample(
                "Request example (phone)",
                value={
                    'first_name': 'Gildong',
                    'last_name': 'Hong',
                    'username': 'loginID',
                    'password': 'loginPW',
                    'nickname': '홍길동',
                    'phone': '01012345678',
                }
            )
        ]
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   # if fail, DRF throw ValidationError
        serializer.save()
        return Response({"ok": True}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    @extend_schema(
        tags=["auth"],
        operation_id="login",
        description="Obtain JWT token pair (access and refresh) by providing username and password.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Login successful, returns JWT tokens."),
            400: OpenApiResponse(description="Invalid credentials."),
        },
        examples=[
            OpenApiExample(
                "Request example",
                value={
                    'username': 'loginID',
                    'password': 'loginPW',
                }
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class LogoutView(APIView):
    @extend_schema(
        tags=["auth"],
        operation_id="logout",
        description="Logout the user (client-side token discard).",
        request=LogoutSerializer,
        responses={
            205: OpenApiResponse(description="Logout successful."),
            400: OpenApiResponse(description="Refresh token error."),
        },
        examples=[
            OpenApiExample(
                "Request example",
                value={
                    'refresh': 'your_refresh_token_here',
                }
            )
        ]
    )
    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            raise ValidationError({"refresh": "Refresh token is required."})
        try: 
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            raise ValidationError({"refresh": "Invalid refresh token."})
        
        return Response({"ok": True}, status=status.HTTP_205_RESET_CONTENT)
    
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["profile"],
        operation_id="show_profile",
        description="Retrieve the profile of the authenticated user.",
        request=ShowProfileSerializer,
        responses={
            200: OpenApiResponse(description="Returns the user's profile information.", response=ShowProfileSerializer),
            401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
        }
    )
    def get(self, request):
        profile = ShowProfileSerializer(request.user)
        return Response(profile.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=["profile"],
        operation_id="update_profile",
        description="Update the profile of the authenticated user. Partial updates are allowed.",
        request=UpdateProfileSerializer,
        responses={
            200: OpenApiResponse(description="Profile updated successfully.", response=ShowProfileSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
        }
    )
    def patch(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(ShowProfileSerializer(profile).data, status=status.HTTP_200_OK)