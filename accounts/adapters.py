from allauth.account.adapter import DefaultAccountAdapter


class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form. The default all-auth only provides some fields like:
        username, email and password. This function allows you to add other
        fields like the name added in this field. assuming you are trying 
        to add other fields, you would have to add it in a user_field function

        user_field(user, '#field', request.data.get('#field', ''))
        where #field is the name of the field you want to add, which in the case 
        below is the name
        """
        from allauth.account.utils import user_field

        user = super().save_user(request, user, form, False)
        user_field(user, 'name', request.data.get('name', ''))
        user.save()
        return user

    def get_login_redirect_url(self, request):
        path = "/api/users/{slug}/"
        return path.format(slug=request.user.slug)

    def get_logout_redirect_url(self, request):
        path = "/api/login/"
        return path

    def get_email_confirmation_redirect_url(self, request):
        path = "/api/emailverified/"
        return path
