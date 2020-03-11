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
    This just needs the accesstoken to be provided, and can be gotten by implementing firebase to the frontend
    ```
    {
        "access_token": "",
        "code": ""
    }
    ```

4. password/reset/
    This expects an email to be provided then it sends an email to the user reset their password.
    ```
    {
        "email": ""
    }
    ```

    password/reset/confirm/<uidb64>/<token>/
    This expects the new passwords of the user and uid and token which is gotten from the link/url of the current site.
    ```
    {
        "new_password1": "",
        "new_password2": "",
        "uid": "",
        "token": ""
    }
    ```

5. me/
    This just returns the current logged in user's slug

6. users/
    This returns all the users in the database

7. users/<slug:slug>/
    This returns the the user whose slug is passed to the url

8. users/<slug:slug>/follow/
    This follows the user whose slug is passed to the url

9. users/<slug:slug>/unfollow/
    This unfollows the user whose slug is passed to the url

10. users/<slug:slug>/followers/
    This this lists all the followers of the user whose slug is passed to the url

11. users/<slug:slug>/following/
    This this lists all users that the user whose slug is passed to the url is following

12. profile/<int:pk>/
    This shows a particular users profile, and if the profile is owned by the current user, then he can edit the profile with either a PUT or PATCH request.

    The fields needed are date of birth, bio, sex, type_of_body, feet, innches, lives_in. Adding the skills is not handled on this route
    ```
    {
        "date_of_birth": null,
        "bio": "",
        "sex": null,
        "type_of_body": null,
        "feet": null,
        "inches": null,
        "lives_in": ""
    }
    ```

13. profile/<int:pk>/skills/
    This is for the user to add his skills to his profile.

    The skills to be added are from a foreign key
    ```
    {
        "skills": []
    }
    ```

14. skills/
    This is to list all the skills in the database

15. skills/create/
    This allows only admin users to create a new skill to the website

    ```
    {
        "name": "",
        "subcategory": "",
        "description": ""
    }
    ```

16. skills/<int:pk>/
    This allows only admin users to update and delete a particular skill

    ```
    {
        "name": "",
        "subcategory": "",
        "description": ""
    }
    ```
17. user/
    This shows the current user logged in his details, and this will allow the user add or change his display picture

    one can make a PUT request to this route to update the picture
    ```
    {
        "picture": null
    }
    ```

18. users/<slug:slug>/showcases/
    This shows all the showcases of the current user whose slug is passed in the url

19. users/<slug:slug>/collaboration/
    This shows all the collaborations of the current user whose slug is passed in the url

20. users/<slug:slug>/sadministrator/
    This shows all the showcases that the current user whose slug is passed in the url is an administrator to
