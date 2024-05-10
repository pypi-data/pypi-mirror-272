from django.contrib import admin
from .models import PersonalDetails, BusinessProfile, ContributionCode, ContributionGroup


@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(ContributionCode)
class ContributionCodeAdmin(admin.ModelAdmin):
    list_display = ['owner', 'code']


@admin.register(ContributionGroup)
class ContributionGroupAdmin(admin.ModelAdmin):
    list_display = ['code', 'member']
