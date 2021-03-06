# cre8ive-backend
cre8ive-mart backend api

## Table of contents
* [Setup](#Setup)
* [Accounts app](#Accounts-app)
* [Showcase app](#Showcase-app)
* [Collaborate app](#Collaborate-app)
* [Notes](#Notes)

## Setup
To run this project, install it locally using pip:

```
$ python -m venv ./venv
$ source ./venv/Scripts/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## Accounts app
The accounts app handles the authentication (Login, signup, change password, reset password, email authentication, google login) of the app

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


21. users/<slug:slug>/cadministrator/

    This shows all the collaborations that the current user whose slug is passed in the url is an administrator to


## Showcase app
The Showcase app handles the uploading/showcasing of works, admin administrators to a showcase so they can manage the project, and comments, replies and likes to showcases.

### urls for the Showcase related app that you need to know about
Before each of these routes, add api/

1. showcase/create/

    This creates a new showcase, and muste be logged in to do this
    ```
    {
        "title": "example title",
        "description": "example description",
        "content": null,
        "skill_type": [
            1,2,3
        ]
    }
    ```
    The **content** is the images, videos, audio of the showcase and it is supposed to be gotten from AWS or Cloudnairy. The **skill_type** also receives an list of the skills **id**. The route also has a get method and this can be useful to show the fields already selected by the user.



2. showcase/

    This shows all of the showcases in the database


3. showcase/mostliked/

    This route lists the most liked showcaases of all time


4. showcase/mostlikedy/

    This route lists the most liked showcaases of the year


5. showcase/mostlikedm/

    This route lists the most liked showcaases of the month


6. showcase/mostlikedw/

    This route lists the most liked showcaases of the week


7. showcase/followingshowcases/

    Shows all the showcases that a logged in user follows.


8. showcase/<slug:slug>/

    This gets a particular showcase through the slug


9. showcase/<slug:slug>/edit/

    This allows administrators to a particular showcase to edit that showcase
    ```
    {
        "title": "The Gods Must Be Crazy",
        "description": "",
        "content": null,
        "skill_type": [
            1,2,3
        ]
    }
    ```
    * The **content** is the images, videos, audio of the showcase and it is supposed to be gotten from AWS or Cloudnairy. 
    * The **skill_type** also receives an list of the skills **id** that you want to add. 
    * The route also has a get method and this can be useful to show the fields already selected by the user.


10. showcase/<slug:slug>/like/

    Here two requests can be made here, An empty **POST** request to like and a **DELETE** request to unlike a particular showcase, which is the showcase of the slug in the URL. The user has to be logged in to do this.


11. showcase/<slug:slug>/likers/

    This lists all the likers to the showcase of the slug in the URL.


12. showcase/<slug:slug>/admin/

    This shows all of the administrators of a particular showcase. This showcase is of the slug passed in the URL.


13. showcase/<slug:slug>/admin/add/

    This allows administrators to add other administrators to the showcase, and you can add more than one user at a time as an admin.
    ```
    {
        "administrator": [
            "slug of user", "slug of user"
        ]
    }
    ```


14. showcase/<slug:slug>/collaborator/

    This shows all  the collaborators to a particular showcase


15. showcase/<slug:slug>/collaborator/add/

    This allows an administrator to add a collaborator to a showcase he is an admin of
    ```
    {
        "user": "user-slug",
        "role": "",
        "skill": [
            2,1
        ]
    }
    ```


16. showcase/collaborator/<int:pk>/

    This shows the details of a particular collaborator


17. showcase/collaborator/<int:pk>/update/

    Allows administrators and the person added as a collaborator to edit the related collaborator's profile
    ```
    {
        "role": "danced throughout the movie",
        "skill": [
            3
        ]
    }
    ```


18. showcase/collaborator/<int:pk>/delete/

    Allows administrators and the person added as a collaborator to delete the related collaborator's profile


19. showcase/<slug:slug>/comment/

    Allows authenticated users to make a comment on a showcase
    ```
    {
        "body": ""
    }
    ```


20. showcase/<slug:slug>/comments/

    lists all the comments to a particular showcase


21. showcase/comments/<int:pk>/

    Allows the owner of the comment to edit using a **PUT** or **PATCH** method and to delete the comment with the **DELETE** method, and must be authenticated to perform the action.
    ```
    {
        "body": "hello there"
    }
    ```


22. showcase/comments/<int:pk>/like/

    An empty **POST** request to like and a **DELETE** request to unlike a particular comment


23. showcase/comments/<int:pk>/reply/

    A **POST** request to reply a particular comment
    ```
    {
        "body": ""
    }
    ```


24. showcase/comments/<int:pk>/replies/

    This lists all the replies to a particular comment. The comment whose *id* is passed into the URL


25. showcase/replies/<int:pk>/

    This allows a **POST** and **PATCH** request to edit a particular reply, and a **DELETE** request to delete a particular reply. The reply whose *id* is passed into the URL
    ```
    {
        "body": ""
    }
    ```


26. showcase/replies/<int:pk>/like/

    An empty **POST** request to like and a **DELETE** request to unlike a particular reply



## Collaborate app
The Collaborate app handles the collaboration on projects requests with other people, add administrators to a collaboration so they can manage it, and comments, replies and likes to a collaboration.

### urls for the Collaborate related app that you need to know about
Before each of these routes, add api/

1. collaboration/

    Shows al the collaboration requests in the database


2. collaboration/create/

    This is to create a collaboration request for a project. expects a **POST** request.
    ```
    {
        "title": "",
        "description": "",
        "media": "",
        "location": "",
        "looking_for": [1,2]
    }
    ```


3. collaboration/<slug:slug>/

    This is to retrieve a particular collaboration


4. collaboration/<slug:slug>/edit/

    Allows administrators to edit a collaboration (i.e. to change the title, description, media files, location, and skills that are searched for)
    ```
    {
        "title": "",
        "description": "",
        "media": "",
        "location": "",
        "looking_for": [1,2]
    }
    ```


5. collaboration/<slug:slug>/admin/

    This is to view all administrators to a collaboration.


6. collaboration/<slug:slug>/admin/add/

    This is for adding more administrators to the collaboration.
    ```
    {
        "administrator": [
            "ope-doe-kaunts1p0unp6bx",
            "odedeyi-david-9xgp9xo1jjiqlpk"
        ]
    }
    ```


7. collaboration/<slug:slug>/like/

    An empty **POST** request to like and a **DELETE** request to unlike a particular collaboration.


8. collaboration/<slug:slug>/likers/

    This lists all the likers to the collaboration of the slug in the URL.


9. collaboration/<slug:slug>/comment/

    Allows authenticated users to make a comment on a collaboration.
    ```
    {
        "body": ""
    }
    ```


10. collaboration/<slug:slug>/comments/

    lists all the comments to a particular collaboration.


11. collaboration/<slug:slug>/interest/

    This shows all the interests shown to a collaboration.


12. collaboration/<slug:slug>/interest/show/

    An empty **POST** and **DELETE** request to show interest and remove interest.


13. collaboration/comments/<int:pk>/

    Allows the owner of the comment to edit using a **PUT** or **PATCH** method and to delete the comment with the **DELETE** method, and must be authenticated to perform the action.
    ```
    {
        "body": "hello there"
    }
    ```


14. collaboration/comments/<int:pk>/like/

    An empty **POST** request to like and a **DELETE** request to unlike a particular comment


15. collaboration/comments/<int:pk>/reply/

    A **POST** request to reply a particular comment
    ```
    {
        "body": ""
    }
    ```


16. collaboration/comments/<int:pk>/replies/

    This lists all the replies to a particular comment. The comment whose *id* is passed into the URL


17. collaboration/replies/<int:pk>/

    This allows a **POST** and **PATCH** request to edit a particular reply, and a **DELETE** request to delete a particular reply. The reply whose *id* is passed into the URL
    ```
    {
        "body": ""
    }
    ```


18. collaboration/replies/<int:pk>/like/

    An empty **POST** request to like and a **DELETE** request to unlike a particular reply


## Notes

* Pagination is automatically done by the app for 20 results per page
* For sign in and sign up, the major packages used were [Django allauth](https://django-allauth.readthedocs.io/en/latest/index.html#) and [Django rest auth](https://django-rest-auth.readthedocs.io/en/latest/#)
* Need to fix
    1. Token authentication (JWT)
    2. image fields as an object
