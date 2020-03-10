from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views as qv


urlpatterns = [
    path("create/", qv.CollaborationCreateView.as_view(), name="collaboration-create"),
    path("", qv.CollaborationListView.as_view(), name="collaboration-list"),
    path("<slug:slug>/", qv.CollaborationRetrieveView.as_view(), name="collaboration-retrive"),
    path("<slug:slug>/edit/", qv.CollaborationEditDeleteView.as_view(), name="collaboration-edit-delete"),
    path("<slug:slug>/admin/", qv.CollaborationListAdminAPIView.as_view(), name="collaboration-list-admin"),
    path("<slug:slug>/admin/add/", qv.CollaborationAddAdminAPIView.as_view(), name="collaboration-add-admin"),
    path("<slug:slug>/like/", qv.CollaborationLikeAPIView.as_view(), name="collaboration-like-unlike"),
    path("<slug:slug>/likers/", qv.CollaborationListVotersAPIView.as_view(), name="collaboration-likers"),
    path("<slug:slug>/comment/", qv.CommentCreateAPIView.as_view(), name="collaboration-comment-create"),
    path("<slug:slug>/comments/", qv.CommentListAPIView.as_view(), name="comment-list"),
    path("<slug:slug>/interest/", qv.ListInterestAPIView.as_view(), name="List-interests"),
    path("<slug:slug>/interest/show/", qv.ShowInterestAPIView.as_view(), name="show-interest"),
    path("comments/<int:pk>/", qv.CommentRUDAPIView.as_view(), name="comment-detail"),
    path("comments/<int:pk>/like/", qv.CommentLikeAPIView.as_view(), name="comment-like"),
    path("comments/<int:pk>/reply/", qv.ReplyCreateAPIView.as_view(), name="reply-create"),
    path("comments/<int:pk>/replies/", qv.ReplyListAPIView.as_view(), name="reply-list"),
    path("replies/<int:pk>/", qv.ReplyRUDAPIView.as_view(), name="reply-detail"),
    path("replies/<int:pk>/like/", qv.ReplyLikeAPIView.as_view(), name="reply-like"),
]
