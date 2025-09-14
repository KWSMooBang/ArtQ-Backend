from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import SignupSerializer

class SignupView(APIView):
    @extend_schema(
        tags=["auth"],
        operation_id="signup",
        description="Create a new user account.",
        request=SignupSerializer,
        responses={
            201: OpenApiResponse(description="User created successfully."),
            400: OpenApiResponse(description="Invalid input data."),
        },
        examples=[
            OpenApiExample(
                "Request example",
                value={
                    'username': 'honggildong',
                    'email': 'honggildong@example.com',
                    'password': 'password1234',
                    'nickname': '홍길동',
                }
            )
        ]
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True}, status=status.HTTP_201_CREATED)
        return Response({"ok": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
