# cre8ive-backend
cre8ive-mart backend api

## accounts app
the accounts app handles the authentication (Login, signup, change password, reset password, email authentication, google login) of the app

### urls for the account related app that you need to know about
* verify-email/again/
* signup/
* google/
* password/reset/
* me/
* users/
* users/<slug:slug>/
* users/<slug:slug>/follow/
* users/<slug:slug>/unfollow/
* users/<slug:slug>/followers/
* users/<slug:slug>/following/
* profile/<int:pk>/
* profile/<int:pk>/skills/
* skills/
* skills/create/
* skills/<int:pk>/
* users/<slug:slug>/showcases/
* users/<slug:slug>/collaboration/
* users/<slug:slug>/administrator/