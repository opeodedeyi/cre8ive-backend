# cre8ive-backend
cre8ive-mart backend api

## accounts app
the accounts app handles the authentication (Login, signup, change password, reset password, email authentication, google login) of the app

### urls for the account related app that you need to know about
1. verify-email/again/
    This expects an email to be provided then it sends a verification email to the user to verify their email. This is necessary when the verification email has expired and they didnt verify their email
    ```
    {
        "email": ""
    }
    ```

2. signup/
    This is to sign up the user into their account
    ```
    {
        "email": "",
        "password1": "",
        "password2": "",
        "name": ""
    }
    ```

3. google/
4. password/reset/
5. me/
6. users/
7. users/<slug:slug>/
8. users/<slug:slug>/follow/
9. users/<slug:slug>/unfollow/
10. users/<slug:slug>/followers/
11. users/<slug:slug>/following/
12. profile/<int:pk>/
13. profile/<int:pk>/skills/
14. skills/
15. skills/create/
16. skills/<int:pk>/
17. users/<slug:slug>/showcases/
18. users/<slug:slug>/collaboration/
19. users/<slug:slug>/administrator/

