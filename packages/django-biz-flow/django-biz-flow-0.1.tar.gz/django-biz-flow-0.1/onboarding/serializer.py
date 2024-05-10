from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from core.views.utils.user_query import UserQueryMixin
from .models import (
    PersonalDetails,
    BusinessProfile,
    ContributionCode,
    ContributionGroup,
    )
from billing.models import Subscription
from utils.contribution_code_gen import contribution_code_generator
from utils.api_messages import APIMessages

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate_username(self, value):
        if value == '':
            raise serializers.ValidationError('Username Field cannot be Empty')
        return value
    
    def validate_first_name(self, value):
        if value == '':
            raise serializers.ValidationError('First name cannot be empty')
        return value
    
    def validate_last_name(self, value):
        if value == '':
            raise serializers.ValidationError('Last name cannot be empty')
        return value

    def validate_email(self, value):
        print(value)
        if value == '':
            raise serializers.ValidationError('Email field cannot be empty')
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use')
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )

        return user
    
class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        exclude = ['user',]

    def create(self, validated_data):
        user = self.context['request'].user
       
        validated_data['user'] = User.objects.get(username=user)
        
        try:
            return PersonalDetails.objects.create(
                **validated_data
            )
        except:
            raise serializers.ValidationError(
                {
                    'error': 'You have already Submitted your profile.'
                }
            )


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        exclude = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = User.objects.get(username=user)
        
        try:
            business_profile =  BusinessProfile.objects.create(
                **validated_data
            )

            # create the contribution Code
            code = contribution_code_generator()
            ContributionCode.objects.create(
                owner = business_profile,
                code=code,
            )
            Subscription.objects.create(
                business=business_profile,
                start_date=timezone.now(),
                expiration_date=timezone.now() + timedelta(days=7)
            )
            return business_profile

        except:
            raise serializers.ValidationError(
                {
                    'error': 'You have already a Business profile.'
                }
            )

class CommonMixins(UserQueryMixin, APIMessages):
    pass

class JoinContributionGroupSerializer(CommonMixins, serializers.Serializer):
    code = serializers.CharField(max_length=15)

    def create(self, validated_data):
        user = self.context['request'].user
        code = validated_data.get('code')
        self.user_inst = user
        user_inst = self.get_user()
        print(user_inst)

        try:
            contrib_code = ContributionCode.objects.get(
                code=code,
            )
        except:
            raise serializers.ValidationError(
                self.error_msg("Invalid Group Code")
            )
        
        try:
            return ContributionGroup.objects.create(
                member=user_inst,
                code=contrib_code,
            )
        except:
            raise serializers.ValidationError(
                self.error_msg("Already A Member of this group")
            )