from django.conf.urls import include
from django.urls import path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (PasswordResetView,
                             PasswordResetConfirmView)
from allauth.account.views import ConfirmEmailView
from . import views as qv


urlpatterns = [
     path('verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
     path('resend-verification-email/', qv.NewEmailConfirmation.as_view(), name='resend-email-confirmation'),
     path('signup/account-confirm-email/<key>/', qv.ConfirmEmailView.as_view(), name='account_confirm_email'),
     path('', include('rest_auth.urls')),
     path('signup/', include('rest_auth.registration.urls')),
     path('google/', qv.GoogleLogin.as_view(), name='google_login'),
     path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
     path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('emailverified/', qv.EmailVerifiedView.as_view(), name='email_verified'),
     path('emailverifiedfailure/', qv.EmailFailureVerifiedView.as_view(), name='email_verified_failure'),
     path('me/', qv.MyUserView.as_view(), name='my-user'),
     path('users/', qv.ListUsersView.as_view(), name='list-users'), # Edit mmade
     path("users/<slug:slug>/", qv.UserRetriveAPIView.as_view(), name="users-detail"),
     path("users/<slug:slug>/follow/", qv.FollowAUserView.as_view(), name="users-follow"),
     path("users/<slug:slug>/unfollow/", qv.UnFollowAUserView.as_view(), name="users-unfollow"),
     path("users/<slug:slug>/followers/", qv.UserFollowerView.as_view(), name="user-followers"),
     path("users/<slug:slug>/following/", qv.UserFollowingView.as_view(), name="user-following"),
     path("profile/<int:pk>/", qv.ProfileRetriveUpdateAPIView.as_view(), name="profile-detail"),
     path("profile/<int:pk>/skills/", qv.ProfileSkillRUAPIView.as_view(), name="profile-skill-edit"),
     path("skills/", qv.SkillListAPIView.as_view(), name="skills"),
     path("skills/create/", qv.SkillCreateAPIView.as_view(), name="skills-create"),
     path("skills/<int:pk>/", qv.SkillUpdateAPIView.as_view(), name="skills-update-destroy"),

     # Querysets for users
     path("users/<slug:slug>/showcases/", qv.ListAUsersShowcasesViewSet.as_view(), name="a-users-showcase-list"),
     path("users/<slug:slug>/collaboration/", qv.ListCollaborationShowcasesViewSet.as_view(), name="users-collaborated-showcase-list"),
     path("users/<slug:slug>/sadministrator/", qv.AdminShowcasesViewSet.as_view(), name="users-admin-showcase-list"),
     path("users/<slug:slug>/cadministrator/", qv.AdminCollaborationsViewSet.as_view(), name="users-admin-collaborations-list"),
]
