# cre8ive-backend
cre8ive-mart backend api

## accounts app
the accounts app handles the authentication (Login, signup, change password, reset password, email authentication, google login) of the app

### urls for the account related app that you need to know about
Before each of these routes, add api/


1. verify-email/again/

    This expects an **email** to be provided then it sends a verification email to the user to verify their email. This is necessary when the verification email has expired and they didn't verify their email.
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
    the name should be the **fullname** (firstname and lastname)


3. google/

    This just needs the **access_token** alone to be provided, and can be gotten by implementing firebase or any other method of your choice to the frontend
    ```
    {
        "access_token": "",
        "code": ""
    }
    ```


4. password/reset/

    This expects an **email** to be provided then it sends an email to the user reset their password.
    ```
    {
        "email": ""
    }
    ```

    password/reset/confirm/<uidb64>/<token>/

    This expects the new **password** of the user and **uid** and **token** which is gotten from the **link**/**url** of the current site.
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

    The fields needed are **date_of_birth**, **bio**, **sex**, **type_of_body**, **feet**, **inches**, **lives_in**.

    **Note**: Adding the skills to the user is not handled on this route
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
    **sex** accepts one of two options "Male" or "Female"

    **type_of_body** accepts one of four options "Slim", "Average", "Athletic" and "Heavyset"

    **date_of_birth** takes this format "yyyy-mm-dd" and should be put like this "1994-12-22"

    **feet** and **inches** accepts a number and the front end should do the limiting to a certain length


13. profile/<int:pk>/skills/

    This is for the user to add his **skills** to his profile.

    The skills to be added are from a foreign key
    ```
    {
        "skills": []
    }
    ```


14. skills/

    This is to list all the skills in the database


15. skills/create/

    This allows only admin users to create a new **skill** to the website

    ```
    {
        "name": "",
        "subcategory": "",
        "description": ""
    }
    ```
    the description gives people us the freedom to explain the skills to people so they can better understand what they are selecting, or explain a particular skill to a random user.


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
    It is named picture instead of display_picture for convinience on the backend, so when signing up with google, it can automatically send the picture from google to the field


18. users/<slug:slug>/showcases/

    This shows all the showcases of the current user whose slug is passed in the url


19. users/<slug:slug>/collaboration/

    This shows all the collaborations of the current user whose slug is passed in the url


20. users/<slug:slug>/sadministrator/

    This shows all the showcases that the current user whose slug is passed in the url is an administrator to


## Showcase app
The Showcase app handles the uploading/showcasing of works, admin administrators to a showcase so they can manage the project, and comments, replies and likes to showcases.

### urls for the Showcase related app that you need to know about
Before each of these routes, add api/

1. showcase/create/


2. showcase/


3. showcase/mostliked/


4. showcase/mostlikedy/


5. showcase/mostlikedm/


6. showcase/mostlikedw/


7. showcase/followingshowcases/


8. showcase/<slug:slug>/


9. showcase/<slug:slug>/edit/


10. showcase/<slug:slug>/like/


11. showcase/<slug:slug>/likers/


12. showcase/<slug:slug>/admin/


13. showcase/<slug:slug>/admin/add/


14. showcase/<slug:slug>/collaborator/


15. showcase/<slug:slug>/collaborator/add/


16. showcase/collaborator/<int:pk>/


17. showcase/collaborator/<int:pk>/update/


18. showcase/collaborator/<int:pk>/delete/


19. showcase/<slug:slug>/comment/


20. showcase/<slug:slug>/comments/


21. showcase/comments/<int:pk>/


22. showcase/comments/<int:pk>/like/


23. showcase/comments/<int:pk>/reply/


24. showcase/comments/<int:pk>/replies/


25. showcase/replies/<int:pk>/


26. showcase/replies/<int:pk>/like/

