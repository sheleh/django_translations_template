from django.utils import translation
from django.utils.translation import gettext_lazy as _
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from app.api.serializers import (
    UserSerializer,
    UserAuthSerializer,
    UserChangePasswordSerializer,
    UserSwitchLanguageSerializer
)


class UserCreateApiView(CreateAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": _("You have successfully created account !")}, status=status.HTTP_201_CREATED)


class UserAuthenticationAPIView(APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.validated_data.get('user'))
        user = serializer.validated_data.get('user')
        response = Response()
        response.data = {"success": _("You have successfully logged in !"), "access_token": token.key}
        response.status_code = status.HTTP_200_OK
        response.set_cookie('django_language', user.language)
        return response


class UserLogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"success": _("You have successfully logged out !")}, status=status.HTTP_200_OK)


class UserChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": _("Your password has been successfully changed!")}, status=status.HTTP_200_OK)


class UserSwitchLanguageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSwitchLanguageSerializer

    def patch(self, request):
        serializer = self.serializer_class(self.request.user, data=request.data)
        translation.activate(self.request.user.language)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.data = {"success": _("Your language has been successfully changed!")}
        response.status_code = status.HTTP_200_OK
        response.set_cookie('django_language', serializer.data)
        return response
