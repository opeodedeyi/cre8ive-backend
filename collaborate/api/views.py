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
                          IsAdminOrReadOnly)
from .serializers import (CollaborateSerializer,
                          CollaborateAdminSerializer,
                          CollaborationLikeSerializer,
                          CommentSerializer,
                          ReplySerializer,
                          InterestSerializer)
from ..models import (Collaborate,
                      Interest,
                      Comment,
                      ReplyComment)


User = get_user_model()

# Collaborate APIView
class CollaborationListView(generics.ListAPIView):
    '''
    Create list and showcases view. user must be logged in to do this
    '''
    queryset = Collaborate.objects.all()
    serializer_class = CollaborateSerializer
    permission_classes = [AllowAny]


class CollaborationCreateView(generics.CreateAPIView):
    '''
    Create collaborations for people to show interests for it
    '''
    queryset = Collaborate.objects.all()
    serializer_class = CollaborateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer_context = {"request": request}
        serializer = self.serializer_class(
            data=request.data, 
            context=serializer_context
        )
        if serializer.is_valid():
            collaborate = serializer.save(user=request.user)
            if collaborate:
                collaborate.administrator.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollaborationRetrieveView(generics.RetrieveAPIView):
    '''
    Retrieve Collaborate view.
    '''
    queryset = Collaborate.objects.all()
    lookup_field = "slug"
    serializer_class = CollaborateSerializer
    permission_classes = [AllowAny]


class CollaborationEditDeleteView(APIView):
    '''
    Retrieve Collaborate view.
    '''
    serializer_class = CollaborateSerializer
    permission_classes = [IsAdmin]

    def get(self, request, slug):
        collaboration = get_object_or_404(Collaborate, slug=slug)

        serializer_context = {"request": request}
        serializer = self.serializer_class(collaboration, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        collaboration = get_object_or_404(Collaborate, slug=slug)

        try:
            self.check_object_permissions(request, collaboration)
            serializer_context = {"request": request}
            serializer = self.serializer_class(collaboration, data=request.data, context=serializer_context)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, slug):
        collaboration = get_object_or_404(Collaborate, slug=slug)

        try:
            self.check_object_permissions(request, collaboration)
            collaboration.delete()
            return Response({'message': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except APIException:
            return Response({'message': 'You are not allowed to delete this at the moment. Please contact us if you feel something is wrong'}, status=status.HTTP_403_FORBIDDEN)


class CollaborationAddAdminAPIView(APIView):
    '''
    Add a user as an administrator to a collaborate
    '''
    serializer_class = CollaborateAdminSerializer
    permission_classes = [IsAdmin]

    def put(self, request, slug):
        collaborate = get_object_or_404(Collaborate, slug=slug)
        try:
            self.check_object_permissions(request, collaborate)
            serializer = self.serializer_class(collaborate, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except APIException:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CollaborationListAdminAPIView(generics.RetrieveAPIView):
    '''
    List all the administrators to a collaboration
    '''
    queryset = Collaborate.objects.all()
    lookup_field = "slug"
    serializer_class = CollaborateAdminSerializer
    permission_classes = [AllowAny]


class CollaborationLikeAPIView(APIView):
    '''
    Can like(post) and unlike(delete) the Collaboration, must be 
    authenticated to do this
    '''
    serializer_class = CollaborationLikeSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        collaborate = get_object_or_404(Collaborate, slug=slug)
        user = self.request.user

        collaborate.voters.remove(user)
        collaborate.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(collaborate, context=serializer_context)

        return Response({'message': 'Successfully Unliked'}, status=status.HTTP_200_OK)

    def post(self, request, slug):
        collaborate = get_object_or_404(Collaborate, slug=slug)
        user = self.request.user

        collaborate.voters.add(user)
        collaborate.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(collaborate, context=serializer_context)

        return Response({'message': 'Successfully liked'}, status=status.HTTP_200_OK)


class CollaborationListVotersAPIView(generics.RetrieveAPIView):
    '''
    List all the likes to a Collaboration
    '''
    queryset = Collaborate.objects.all()
    lookup_field = "slug"
    serializer_class = CollaborationLikeSerializer
    permission_classes = [AllowAny]


# COMMENT APIView
class CommentCreateAPIView(generics.CreateAPIView):
    '''
    Can comment on Collaboration view. user must be 
    authenticated to do this
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwargs_slug = self.kwargs.get("slug")
        collaborate = get_object_or_404(Collaborate, slug=kwargs_slug)

        serializer.save(user=request_user, post=collaborate)


class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Can read, edit and delete  the comment on Collaboration, the user 
    must be owner of the object to do this
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


class CommentListAPIView(generics.ListAPIView):
    '''
    Can see all the comments related to a particular Collaboration, 
    the user must be authenticated to do this
    '''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Comment.objects.filter(post__slug=kwarg_slug).order_by("-created_at")


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


class ShowInterestAPIView(APIView):
    '''
    show interest to a collaboration 
    '''
    serializer_class = InterestSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        collaboration = get_object_or_404(Collaborate, slug=slug)
        user = request.user

        if Interest.objects.filter(post=collaboration).filter(user=user).exists():
            interest = Interest.objects.get(
                post=collaboration,
                user=user
            )
            interest.delete()
            return Response({'message': 'Successfully removed interest'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You have no interest here to delete'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, slug):
        collaboration = get_object_or_404(Collaborate, slug=slug)
        user = request.user

        if collaboration.user==user:
            return Response({'message': 'You cannot show interest in your post'}, status=status.HTTP_400_BAD_REQUEST)
        elif Interest.objects.filter(post=collaboration).filter(user=user).exists():
            return Response({'message': 'You have already shown interest'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Interest.objects.create(
                post=collaboration,
                user=user
            )
            return Response({'message': 'Successfully shown interest'}, status=status.HTTP_201_CREATED)


class ListInterestAPIView(APIView):
    '''
    show all users that have shown interests to a collaboration 
    '''
    serializer_class = InterestSerializer
    permission_classes = [AllowAny]

    def get(self, request, slug):
        collaboration = get_object_or_404(Collaborate, slug=slug)
        interests = Interest.objects.filter(post=collaboration)

        serializer_context = {"request": request}
        serializer = self.serializer_class(interests, many=True, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

