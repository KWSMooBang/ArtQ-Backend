from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import RegistrationSerializer

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
