from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import User, UserInfluencer
from .constants import ADMIN, ECOMMERCE, INFLUENCER
from apps_base.influencer.models import Influencer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    influencer = serializers.IntegerField(write_only=True, max_value=None, min_value=None, required=False)
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    # user_influencer = serializers.SerializerMethodField()
    user_influencer_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
            'is_active', 'influencer', 'password', 'id',
            'user_influencer_id']

    # def get_user_influencer(self, obj):
    #     try:
    #         user_influencer = obj.user_user_influencer.influencer.name
    #     except UserInfluencer.DoesNotExist as e:
    #         user_influencer = 'MASTER'
    #     return user_influencer

    def get_user_influencer_id(self, obj):
        try:
            user_influencer_id = obj.user_user_influencer.influencer.id
        except UserInfluencer.DoesNotExist as e:
            user_influencer_id = None
        return user_influencer_id

    def create(self, validated_data):

        # create user
        user = User.objects.create(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        if validated_data.get('influencer'):
            user.type_user = INFLUENCER
            influencer = Influencer.objects.get(id=validated_data.get('influencer'))
            UserInfluencer.objects.create(user=user, influencer=influencer)
        else:
            user.type_user = ADMIN
        user.save()
        return user
