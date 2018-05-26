from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.password_validation import validate_password
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from apps_base.custom_auth.models import User
from apps_base.custom_auth.constants import INFLUENCER
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserInfluencerJSONWebTokenSerializer(JSONWebTokenSerializer):

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if user.type_user == INFLUENCER:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    first_name = serializers.CharField(max_length=120)
    last_name = serializers.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UserChangePassSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=120)
    new_password = serializers.CharField(max_length=120)
    confirm_password = serializers.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['password', 'new_password', 'confirm_password']

    def validate_new_password(self, attr):
        validate_password(attr)
        return attr

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']
        if new_password != confirm_password:
            msg = _('Passwords do not match')
            raise serializers.ValidationError(msg)
        return attrs