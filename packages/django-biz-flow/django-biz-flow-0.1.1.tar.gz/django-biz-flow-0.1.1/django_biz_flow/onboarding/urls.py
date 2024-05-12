from django.urls import path
from .views.common import CreateUserAccount, CreatePersonalDetails
from .views.owner import CreateBusinessProfile, OnboardingSuccess
from .views.customer import JoinContributionGroup

app_name = 'onboarding'

urlpatterns = [
    # common authentication/onboarding
    path('create-user/', CreateUserAccount.as_view()),
    path('create/profile/personal-details/', CreatePersonalDetails.as_view()),

    # business owner profile
    path('create/profile/business/', CreateBusinessProfile.as_view()),
    path('success/owner/', OnboardingSuccess.as_view()),

    # customer profile
    path('customer/join-group/', JoinContributionGroup.as_view()),
]