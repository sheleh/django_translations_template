from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import translation
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CharField, EmailField, ChoiceField
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError, PermissionDenied
from app.api.utils.tasks import send_signup_mail, send_password_update_mail, send_language_update_mail
from app.models import User


class UserSerializer(ModelSerializer):
    email = EmailField(validators=[UniqueValidator(User.objects.all())])
    password = CharField(write_only=True)
    language = ChoiceField(
        required=False,
        choices=settings.LANGUAGES,
        allow_blank=True,
        default=settings.LANGUAGE_CODE[:2]
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'language']

    def create(self, validated_data, user=None):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        send_signup_mail.delay(recipient=validated_data.get('email'), language=validated_data.get('language'))
        translation.activate(user.language)
        return user


class UserAuthSerializer(ModelSerializer):
    email = EmailField()
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        user = authenticate(email=attrs.get('email'), password=attrs.get('password'))
        if not user:
            raise PermissionDenied({'error': 'Email or password is incorrect'})
        translation.activate(user.language)
        attrs['user'] = user

        return attrs


class UserChangePasswordSerializer(ModelSerializer):
    current_password = CharField(write_only=True)
    new_password = CharField(write_only=True)
    confirm_new_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['current_password', 'new_password', 'confirm_new_password']

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('confirm_new_password'):
            raise ValidationError({'new_password': _("These passwords do not match")})
        if not self.instance.check_password(attrs.get('current_password')):
            raise ValidationError({'current_password': _("Password is incorrect.")})
        if attrs.get('new_password') == attrs.get('current_password'):
            raise ValidationError({'new_password': _("Passwords do not have to be the same.")})

        return attrs

    def update(self, instance, validated_data):
        update_data = {'password': make_password(validated_data.get('new_password'))}
        send_password_update_mail.delay(recipient=instance.email, language=instance.language)
        return super(UserChangePasswordSerializer, self).update(instance, update_data)


class UserSwitchLanguageSerializer(ModelSerializer):
    language = CharField(min_length=2, max_length=2)

    class Meta:
        model = User
        fields = ['language']

    def validate_language(self, attrs):
        allowed_languages_keys = tuple(locale[0] for locale in settings.LANGUAGES)
        if attrs not in allowed_languages_keys:
            raise ValidationError(_('The language key is not entered correctly'))
        return attrs

    def update(self, instance, validated_data):
        setattr(instance, "language", self.validated_data.get('language'))
        instance.save()
        translation.activate(instance.language)
        send_language_update_mail.delay(recipient=instance.email, language=instance.language)
        return instance
