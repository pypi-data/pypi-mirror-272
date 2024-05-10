from django.db import models
from django.contrib.auth.models import User
from utils.states import STATES_IN_NG


class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user}'


class ContributionCode(models.Model):
    owner = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE)
    code = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.code}'


class ContributionGroup(models.Model):
    '''
    For Each Member/Customer to Identify Their Group
    '''
    code = models.ForeignKey(ContributionCode, on_delete=models.CASCADE)
    member = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code.code}/{self.code.owner}'


class PersonalDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11)
    state = models.CharField(max_length=15, choices=STATES_IN_NG)

    def __str__(self):
        return f'{self.user}'
