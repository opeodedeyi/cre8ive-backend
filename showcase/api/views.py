from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,
                                        AllowAny)
from .permissions import (IsUserOrReadOnly, 
                          IsAdmin, 
                          IsUser, 
                          IsAdminOrOwner,
                          IsAdminOrReadOnly)
from .serializers import (ShowcaseSerializer,
                          CommentSerializer,
                          ShowcaseDetaiedSerializer,
                          ShowcaseAdminSerializer,
                          ReplySerializer,
                          CollaboratorSerializer,
                          CollaboratorUpdateSerializer,
                          ShowcaseLikeSerializer)
from ..models import (Showcase,
                      Comment,
                      ReplyComment,
                      Collaborator)
from accounts.models import FollowLog
from django.db.models import Count
import datetime


User = get_user_model()
# SHOWCASE APIView
class showcaseListViewSet(generics.ListAPIView):
    '''
    Create list and showcases view. user must be logged in to do this
    '''
    queryset = Showcase.objects.all()
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]


class showcaseCreateViewSet(generics.CreateAPIView):
    '''
    Create list and showcases view. user must be logged in to do this
    '''
    queryset = Showcase.objects.all()
    serializer_class = ShowcaseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer_context = {"request": request}
        serializer = self.serializer_class(
            data=request.data, 
            context=serializer_context
        )
        if serializer.is_valid():
            showcase = serializer.save(user=request.user)
            if showcase:
                showcase.administrator.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class showcaseAddAdminAPIView(APIView):
    '''
    Add a user as an administrator to a showcase
    '''
    serializer_class = ShowcaseAdminSerializer
    permission_classes = [IsAdmin]

    def put(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)
        try:
            self.check_object_permissions(request, showcase)
            serializer = self.serializer_class(showcase, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN)


class showcaseListAdminAPIView(generics.RetrieveAPIView):
    '''
    List all the administrators to a showcase
    '''
    queryset = Showcase.objects.all()
    lookup_field = "slug"
    serializer_class = ShowcaseAdminSerializer
    permission_classes = [AllowAny]


class showcaseListVotersAPIView(generics.RetrieveAPIView):
    '''
    List all the likes to a showcase
    '''
    queryset = Showcase.objects.all()
    lookup_field = "slug"
    serializer_class = ShowcaseLikeSerializer
    permission_classes = [AllowAny]


class showcaseRetrieveView(generics.RetrieveAPIView):
    '''
    Retrieve showcases view
    '''
    queryset = Showcase.objects.all()
    lookup_field = "slug"
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]


class showcaseEditDeleteView(APIView):
    '''
    edit, delete Showcase view.
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [IsAdmin]

    def get(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)

        serializer_context = {"request": request}
        serializer = self.serializer_class(showcase, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)

        try:
            self.check_object_permissions(request, showcase)
            serializer_context = {"request": request}
            serializer = self.serializer_class(showcase, data=request.data, context=serializer_context)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            return Response({'message': 'You are not allowed to make the edit at the moment'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)

        try:
            self.check_object_permissions(request, showcase)
            showcase.delete()
            return Response({'message': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except APIException:
            return Response({'message': 'You are not allowed to delete this at the moment. Please contact us if you feel something is wrong'}, status=status.HTTP_403_FORBIDDEN)


class ShowcaseLikeAPIView(APIView):
    '''
    Can like(post) and unlike(delete) the showcases, must be 
    authenticated to do this
    '''
    serializer_class = ShowcaseDetaiedSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)
        user = self.request.user

        showcase.voters.remove(user)
        showcase.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(showcase, context=serializer_context)

        return Response({'message': 'Successfully Unliked'}, status=status.HTTP_200_OK)

    def post(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)
        user = self.request.user

        showcase.voters.add(user)
        showcase.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(showcase, context=serializer_context)

        return Response({'message': 'Successfully liked'}, status=status.HTTP_200_OK)


# COMMENT APIView
class CommentCreateAPIView(generics.CreateAPIView):
    '''
    Can comment on showcases view. user must be 
    authenticated to do this
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwargs_slug = self.kwargs.get("slug")
        showcase = get_object_or_404(Showcase, slug=kwargs_slug)

        serializer.save(user=request_user, showcase=showcase)


class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Can edit and delete  the comment, the user must be owner of 
    the object to do this
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


class ShowcaseCommentListAPIView(generics.ListAPIView):
    '''
    Can see all the comments related to a particular showcase, 
    the user must be authenticated to do this
    '''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Comment.objects.filter(showcase__slug=kwarg_slug).order_by("-created_at")


class CommentLikeAPIView(APIView):
    '''
    Can like(post) and unlike(delete) the comments, must be 
    authenticated to do this
    '''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = self.request.user

        comment.voters.remove(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response({'message': 'Successfully unliked'}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = self.request.user

        comment.voters.add(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response({'message': 'Successfully liked'}, status=status.HTTP_200_OK)


# REPLY APIView
class ReplyCreateAPIView(generics.CreateAPIView):
    '''
    Can reply on comment view. user must be 
    authenticated to do this
    '''
    queryset = ReplyComment.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwargs_pk = self.kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=kwargs_pk)

        serializer.save(user=request_user, comment=comment)


class ReplyRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Can edit and delete  the reply, the user must be owner of 
    the object to do this
    '''
    queryset = ReplyComment.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


class ReplyListAPIView(generics.ListAPIView):
    '''
    Can see all the replies related to a particular comment, 
    the user must be authenticated to do this
    '''
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_pk = self.kwargs.get("pk")
        return ReplyComment.objects.filter(comment__pk=kwarg_pk).order_by("-created_at")


class ReplyLikeAPIView(APIView):
    '''
    Can like(post) and unlike(delete) the reply, must be 
    authenticated to do this
    '''
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        reply = get_object_or_404(ReplyComment, pk=pk)
        user = self.request.user

        reply.voters.remove(user)
        reply.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(reply, context=serializer_context)

        return Response({'message': 'Successfully unliked'}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        reply = get_object_or_404(ReplyComment, pk=pk)
        user = self.request.user

        reply.voters.add(user)
        reply.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(reply, context=serializer_context)

        return Response({'message': 'Successfully liked'}, status=status.HTTP_200_OK)


# Querysets
class MostLikedShowcasesView(generics.ListAPIView):
    '''
    Most liked showcases in the website
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Showcase.objects.annotate(like_count=Count('voters')).order_by('-like_count')


class MostLikedWeekShowcasesView(generics.ListAPIView):
    '''
    Most liked showcases created within the past week
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        last_7_days = datetime.datetime.today() - datetime.timedelta(7)
        return Showcase.objects.filter(created_on__range=[last_7_days,datetime.datetime.today()]).annotate(like_count=Count('voters')).order_by('-like_count')


class MostLikedMonthShowcasesView(generics.ListAPIView):
    '''
    Most liked showcases created within the past month
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        last_30_days = datetime.datetime.today() - datetime.timedelta(30)
        return Showcase.objects.filter(created_on__range=[last_30_days,datetime.datetime.today()]).annotate(like_count=Count('voters')).order_by('-like_count')


class MostLikedYearShowcasesView(generics.ListAPIView):
    '''
    Most liked showcases created within the past year
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        last_365_days = datetime.datetime.today() - datetime.timedelta(365)
        return Showcase.objects.filter(created_on__range=[last_365_days,datetime.datetime.today()]).annotate(like_count=Count('voters')).order_by('-like_count')


class FollowingShowcasesView(generics.ListAPIView):
    '''
    Showcases of people i follow
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        followed_people = FollowLog.objects.filter(followed_by=current_user).filter(status='following').values('user')
        return Showcase.objects.filter(user__in=followed_people).order_by('-created_on')


# Collaborator functionality
class CollaboratorCreateView(APIView):
    '''
    Allow Aministrator only to add a collaborator to a showcase
    '''
    serializer_class = CollaboratorSerializer
    permission_classes = [IsAdmin]

    def post(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)

        try:
            self.check_object_permissions(request, showcase)
            serializer = self.serializer_class(data=request.data, context={'post':showcase})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CollaboratorDeleteView(APIView):
    '''
    Allow Aministrator only to delete a collaborator to a showcase
    '''
    permission_classes = [IsAdminOrOwner]

    def delete(self, request, pk):
        collaborator = get_object_or_404(Collaborator, pk=pk)

        try:
            self.check_object_permissions(request, collaborator)
            collaborator.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN) 


class CollaboratorListView(APIView):
    '''
    List all the collaborators to a showcase
    '''
    serializer_class = CollaboratorSerializer
    permission_classes = [AllowAny]

    def get(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)
        collaborators = Collaborator.objects.filter(post=showcase)
        serializer = self.serializer_class(collaborators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollaboratorRetrieveView(generics.RetrieveAPIView):
    '''
    get deatails about a collaboration
    '''
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorUpdateSerializer
    permission_classes = [AllowAny]


class CollaboratorUpdateView(APIView):
    '''
    Gives a collaborator or admin the ability to edit their own collaboration detail
    They can edit their:
        -Role
        -Skill
    '''
    permission_classes = [IsAdminOrOwner]
    serializer_class = CollaboratorUpdateSerializer

    def get(self, request, pk):
        collaborator = get_object_or_404(Collaborator, pk=pk)
        serializer = self.serializer_class(collaborator)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        collaborator = get_object_or_404(Collaborator, pk=pk)

        try:
            self.check_object_permissions(request, collaborator)
            serializer = self.serializer_class(collaborator, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN)
    