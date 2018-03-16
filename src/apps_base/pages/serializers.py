from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from .models import HomeBanner, FrequentQuestion, TermsConditions, PaymentMethods, Pages


class HomeBannerSerializer(serializers.ModelSerializer):
    image_crop = serializers.SerializerMethodField()
    class Meta:
        model = HomeBanner
        fields = ['id', 'name',  'position', 'image',
             'is_active', 'image_crop']

    def get_image_crop(self, obj):
        crop = get_thumbnail(obj.image, '180x60', crop='center', quality=99)
        return self.context['request'].build_absolute_uri(crop.url)


class FrequentQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrequentQuestion
        fields = ['id', 'content']


class TermsConditionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsConditions
        fields = ['id', 'content']


class PaymentMethodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethods
        fields = ['id', 'content']


class PagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pages
        fields = ['id', 'description', 'name', 'position', 'is_active',
            'slug', 'title', 'meta_description']

