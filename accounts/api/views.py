from rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticatedOrReadOnly, 
                                        IsAuthenticated, 
                                        IsAdminUser)
from rest_framework.settings import api_settings
from core.mixin import MyPaginationMixin
from .permissions import IsUserOrReadOnly, IsAdminUserOrReadOnly
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.utils import send_email_confirmation
from allauth.account.admin import EmailAddress
from rest_framework.exceptions import APIException
from rest_auth.registration.views import SocialLoginView
from django.http import HttpResponseRedirect
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import filters as filtr
from .serializers import (CustomUserDetailsSerializer,
                          UserSerializer,
                          ProfileSerializer,
                          ProfileDetailedSerializer,
                          ProfileSkillEditSerializer,
                          ProfilePhotoSerializer,
                          SkillSerializer,
                          FollowerSerializer,
                          FollowingSerializer)
from showcase.api.serializers import ShowcaseSerializer, CollaboratorSerializer
from showcase.models import Showcase, Collaborator
from accounts.models import Profile, Skill, FollowLog


############################### user authentication section ###############################
User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class CustomRegisterView(RegisterView):
    '''
    a custom register view that overrides the rest-auth's default 
    '''
    permission_classes = [AllowAny]
    queryset = User.objects.all()


############################### confirm email view ###############################
# class CustomConfirmEmailView(ConfirmEmailView):
#     def get(self, *args, **kwargs):
#         try:
#             self.object = self.get_object()
#         except Http404:
#             self.object = None
#         user = User.objects.get(email=self.object.email_address.email)
#         redirect_url = reverse('user', args=(user.id,))
#         return redirect(redirect_url)


############################# request new confirmation email #############################
class EmailConfirmation(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response({'message': 'This email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                send_email_confirmation(request, user=user)
                return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
            except APIException:
                return Response({'message': 'This email does not exist, please create a new account'}, status=status.HTTP_403_FORBIDDEN)


############################## Email verification success or failure ##############################
class EmailVerifiedView(APIView):
    '''
    Gets my user from the database
    '''
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "Your email has been successfully verified."}, status=status.HTTP_200_OK)


class EmailFailureVerifiedView(APIView):
    '''
    Gets my user from the database
    '''
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "This e-mail confirmation link expired or is invalid. Please issue a new e-mail confirmation request."}, status=status.HTTP_403_FORBIDDEN)


############################## Listing users in the database ##############################
class MyUserView(APIView):
    '''
    Gets my user from the database
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_slug = request.user.slug
        return Response({"slug": user_slug}, status=status.HTTP_200_OK)


class ListUsersView(APIView, MyPaginationMixin):
    '''
    Gets all the users in the database
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('email', 'name', 'profiles__skills')
    # filter_backends = [filtr.SearchFilter]
    search_fields = ['email', 'name', 'profiles__skills']

    def get(self, request):
        page = self.paginate_queryset(self.queryset)

        if page is not None:
            serializer_context = {"request": request}
            serializer = self.serializer_class(page, context=serializer_context, many=True)
            return self.get_paginated_response(serializer.data)


class UserRetriveAPIView(APIView):
    '''
    Gets a particular user in the database using the slug as the lookup
    '''
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]

    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)

        serializer_context = {"request": request}
        serializer = self.serializer_class(user, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


############################### following and unfollowing users ###############################
class FollowAUserView(APIView):
    '''
    Follow a user
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        response = {
            'status':None,
            'detail':None
        }
        response['status'],response['detail'] = request.user.follow_a_user(slug)
        return Response(response, status=status.HTTP_201_CREATED)


class UnFollowAUserView(APIView):
    '''
    unfollow a user
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        response = {
            'status':None,
            'detail':None
        }
        response['status'],response['detail'] = request.user.unfollow_a_user(slug)
        return Response(response, status=status.HTTP_202_ACCEPTED)


############################### Get followers and following ###############################
class UserFollowerView(APIView):
    '''
    Gets all the followers to a user
    '''
    permission_classes = [AllowAny]

    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        followers = user.followers.all().filter(status='following').order_by("-followed_on")
        data = FollowerSerializer(followers, many=True).data
        data_to_return = list(map(lambda item: item['followed_by'], data))
        return Response(data_to_return, status=status.HTTP_200_OK)


class UserFollowingView(APIView):
    '''
    Gets all the following of a user
    '''
    permission_classes = [AllowAny]

    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        following = user.following.all().filter(status='following').order_by("-followed_on")
        data = FollowingSerializer(following, many=True).data
        data_to_return = list(map(lambda item: item['user'], data))
        return Response(data_to_return, status=status.HTTP_200_OK)


############################### profile section ###############################
# Note: can get the profile PK from the user view and can edit the profile, or get
# a users detailed profile.

class ProfileRetriveUpdateAPIView(generics.RetrieveUpdateAPIView):
    '''
    gets a particular profile in the database and can edit
    if owned by the user
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailedSerializer
    permission_classes = [IsUserOrReadOnly]


class ProfileSkillRUAPIView(generics.RetrieveUpdateAPIView):
    '''
    to edit the skills of the user alone
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileSkillEditSerializer
    permission_classes = [IsUserOrReadOnly]

class ProfilePhotoRUAPIView(generics.RetrieveUpdateAPIView):
    '''
    to edit the photo of the user alone
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfilePhotoSerializer
    permission_classes = [IsUserOrReadOnly]


############################### skill section ###############################
# Note: to be able to add a skill by the superuser/AdminUser
# to also be able to get all skills in the data base

class SkillListAPIView(generics.ListAPIView):
    '''
    gets all skills in the database
    '''
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    filter_backends = [filtr.SearchFilter]
    search_fields = ['name', 'subcategory']

    def get_queryset(self):
        return Skill.objects.all().order_by("subcategory")


class SkillCreateAPIView(generics.CreateAPIView):
    '''
    create a new skill in the database
    '''
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUser]
    

class SkillUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    update and delete a particular skill in the database
    '''
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUser]


############################### get a users showcases ###############################
class ListAUsersShowcasesViewSet(generics.ListAPIView):
    '''
    List all the showcases of a user
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        user = get_object_or_404(User, slug=kwarg_slug)
        return Showcase.objects.filter(user=user)


class ListCollaborationShowcasesViewSet(generics.ListAPIView):
    '''
    List all the collabrations of a user
    '''
    serializer_class = CollaboratorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        user = get_object_or_404(User, slug=kwarg_slug)

        return Collaborator.objects.filter(user=user)


class AdminShowcasesViewSet(generics.ListAPIView):
    '''
    List all the showcases that a user is an administrator of
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        user = get_object_or_404(User, slug=kwarg_slug)
        return Showcase.objects.filter(administrator=user)