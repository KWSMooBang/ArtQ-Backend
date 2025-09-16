from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer

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
            400: OpenApiResponse(description="Invalid input data."),
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
        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True}, status=status.HTTP_201_CREATED)
        return Response({"ok": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({"ok": False, "error": "refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            return Response({"ok": False, "error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"ok": True}, status=status.HTTP_205_RESET_CONTENT)