from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from homefinder_app.serializers.users import UserCreateSerializer
from homefinder_app.utils import set_jwt_cookies



class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = UserCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()

        response = Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

        set_jwt_cookies(response, user)

        return response



class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = authenticate(
                request=request,
                email=email,
                password=password
            )

            if user:
                response = Response(status=status.HTTP_200_OK)

                set_jwt_cookies(response, user)

                return response
            else:
                return Response(
                    data={
                        "message": "Invalid username or password"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as exc:
            return Response(
                data={
                    "message": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogOutUser(APIView):
    def post(self, request: Request) -> Response:
        try:
            refresh = request.COOKIES.get('refresh_token')

            if refresh:
                token = RefreshToken(refresh)
                token.blacklist()

        except Exception as exc:
            return Response(
                data={
                    "message": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response