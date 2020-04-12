# class ListUsersView(APIView, MyPaginationMixin):
#     '''
#     This is a replacement for the "ListUsersAPIView" in the
#     accounts/api/views
#     '''
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
#     pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_fields = ('email', 'name', 'profiles__skills')
#     # filter_backends = [filtr.SearchFilter]
#     search_fields = ['email', 'name', 'profiles__skills']

#     def get(self, request):
#         page = self.paginate_queryset(self.queryset)

#         if page is not None:
#             serializer_context = {"request": request}
#             serializer = self.serializer_class(page, context=serializer_context, many=True)
#             return self.get_paginated_response(serializer.data)