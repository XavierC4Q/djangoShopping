from rest_framework import serializers
from .models import (
    User,
    Product,
    ProductDetail,
    Order
)
from .choices import STATES
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class RegisterSerializer(serializers.Serializer):
    display_name = serializers.CharField(
        max_length=14,
        allow_blank=False,
        min_length=6
    )
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    state = serializers.ChoiceField(allow_blank=False, choices=STATES)

    def validate_display_name(self, display_name):
        display_name = get_adapter().clean_display_name(display_name)
        return display_name

    def validate_state(self, state):
        state = get_adapter().clean_state(state)
        return state

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ('A user is already registered with this e-mail address.'))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(('The two password fields didn\'t match.'))
        return data

    def get_cleaned_data(self):
        return {
            'display_name': self.validated_data.get('display_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'state': self.validated_data.get('state', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'id',
            'display_name',
            'state',
            'email',
            'date_joined',
            'last_login'
        )
        ordering = ['-id']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'
        depth = 1
        ordering = ['id']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1

