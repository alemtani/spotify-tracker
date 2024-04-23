
## CMSC 388J Final Project Writeup

**Group Members (1-4 members):**


```
Select your group members in gradescope!!!
```

**Directions:**

Read the project specifications and fill out all the questions **in gradescope!**

> [!IMPORTANT]
> All the answers to the questions should be submitted to the gradescope submission with all
> of your group members selected


## Logistics

There are 4 things you will submit for the final project (only 1 group member has to submit, but select all members names in gradescope):

1. Proposal
2. Project code
3. Writeup (submit when you submit your project’s code)
4. Pretty Project (Extra credit due at the end of the semester)


Both the Proposal and Writeup use this document as a template (your writeup will likely be the same or similar to your proposal depending on how much has changed since your proposal document).

**Due dates (unless specified elsewhere):**

Proposal: April 12, 2024

* We **highly recommend** you complete this as early as possible so you have more time to work on the project. We will review your proposal within 1-2 days of submission.

## Overview

The final project for this class is to create a Flask app in a group of 1-4. You have a lot of freedom for this project as long as you meet the requirements. 

**You’re welcome to use Project 4 (or any other project from this course) as a base (though you’re not required to–in fact, we encourage you to try creating something from scratch)**. *If you choose to use a course project, you need to make a “substantial” change. Examples of “substantial” changes include:*

* Using a different API (instead of the OMDB API) + minor feature to demonstrate knowledge of Flask
* It’s no longer a “review site” but something else
* It’s still a “review site” but you add a major feature
* Examples: ability to reply to reviews

Use your best judgment here but reach out to course instructors if you’re unsure. 

```
Description of your final project idea:

So the Spotify Tracker is implemented. In essence, it is an IMDB for Spotify (and much, much simpler). The core features of this app include.
1. Users can search for albums and tracks (we will dub these as "players") using the Spotify API.
2. Users can add players to their library. Each player in the library is a "tracker" where users can update listening status and number of tracks listened to (if it is an album).
3. Users can also rate and review players (don't need to add to library). The app will aggregate the ratings to provide an average score for the players on a detail view, and also when viewing the tracks of an album.
```



## Requirements

Note that some of these requirements overlap with each other so some features may satisfy multiple requirements.  

**Registration and Login:**



* There needs to be some sort of user control: logging in, registering, logging out.
* Certain features should only be available to logged-in users.

```
Describe what functionality will only be available to logged-in users:

1. First of all, users have settings like username, account, profile picture, and password that by definition require being logged in to complete.
2. Only logged-in users can add players to their library, and edit/delete the trackers for those players.
3. Only logged-in users can rate and review players, and edit those ratings/reviews.
```



**Forms:**



* At least 4 forms (can include registration and login forms)
* Must be CSRF protected

```
List and describe at least 4 forms:

1. Registration: This requires users to enter a username, email, and confirm a password. The username and email must be unique.
2. Login: The user logs in using email and password. Both the email must exist and the password must match for that email.
3. Settings: There are three associated forms.
    a. Update Account: The user can update the username and about. The username must be unique.
    b. Update Profile Picture: The user can upload a JPEG or PNG file.
    c. Update Password: The user enters their old password, and confirm a new password twice.
4. Tracker Forms: There are two categories of forms, each with two forms.
    a. Add/Delete: This is pretty straightforward, it adds and removes a tracker from the player's library.
    b. Edit Album/Tracker: The user can update the listening status (added, listening, done) and the listened tracks for an album. The listened tracks must be less than the total tracks, which is passed in as a hidden field for validation purposes.
5. Review Form: The form allows users to enter a rating and an optional comment to elaborate. If the user already filled out a review, the user can edit their review directly.

A note about forms: I often used render_form from the Bootstrap-Flask library, which automatically generates the CSRF token for the form (I used "Inspect" to check). Documentation here: https://bootstrap-flask.readthedocs.io/en/stable/
```



**Blueprints:**



* Must have at least 2 blueprints 
* Each blueprint should have at least 2 visible and accessible routes

```
List and describe your routes/blueprints (don't need to list all routes/blueprints you may have–just enough for the requirement):

There are 2 main blueprints.
1. Users: This handles authentication and account settings.
    a. Register (GET/POST "/register"): The user submits the registration form, and once the form is validated, the entered password is hashed, the user is created, and automatically logged in before being redirected to the search page. Now if the user was already logged in, simply redirect them.
    b. Login (GET/POST "/login"): The user submits the login form, and when the form is validated, the app checks if the user with the email exists and the password hash matches. If so, login the user and redirect to the search page, otherwise the user needs to login again. Again, if the user was logged in, redirect.
    c. Logout (GET "/logout"): Simply logout the user and redirect to search.
    d. Account (GET/POST "/account"): For all three of these forms, once they are validated, the user object is updated with the entered data and saved, before being redirected to the user profile page. Note that the password hash for the new password will be stored in lieu of the actual password for security reasons.
2. Players: This handles the primary functionality for the app, including search, library, and reviews.
    a. Search (GET "/"): For this, I decided to implement extra credit by using jQuery to implement the search functionality. So when the user toggles between searching for albums and tracks, jQuery sends a GET "/search" request to the app, which will use the Spotify API to search and return the players. Furthermore, when the user clicks "Load More...", the offset is passed and allows the API to load fresh players.
    b. User Profile (GET "/user/<user_id>"): Fetch the user with the passed id or return error if not found. Show the user image, and provide a link to the user library and reviews, and also email the user or update settings if it is the current user.
    c. User Library (GET "/user/<user_id>/library"): This is another point I used jQuery, where the user can toggle between searching for albums and tracks, and the listening status for the player. jQuery then sends a GET "/user/<user_id>/tracakers" request to the app, which will fetch the trackers.
    d. User Reviews (GET "/user/<user_id>/reviews"): Simply fetch the Review objects from the user, in descending order of last update.
    e. Edit Tracker (GET/POST "/player/<player_id>/edit"): Fetches one of two forms, either the album or the track form depending on the type of player. Some additional logic on submit: if the listening status is set to "done", listened tracks is automatically set to the total stracks, and if the listening status is set to "added", listened tracks is automatically set to 0.
    f. Player Detail (GET/POST "/player/<player_id>"): This is easily the most comprehensive route, so I will break it down into components.
        i. This show the detailed view of a player, including the name, image, and stats fetched from Spotify API. It also provides the average rating for the player. If the player is an album, it lists the tracks below, and the average rating for those tracks.
        ii. If the user is logged in, they can add the player to their library or, if it is already in, edit or delete the tracker (calling edit will go to the edit tracker form).
        iii. At the bottom are the list of reviews for the player, and if the user is logged in, they can add or edit their review. Notice that the review form is automatically populated with the current user review.
```



**Database:**



* Must use MongoDB

```
Describe what will be stored/retrieved from MongoDB:

Three models are stored/retrieved from MongoDB.
1. User: This tracks field username, email, password, about, and profile picture. Username, email, and password are required fields.
2. Tracker: This tracks the user (as a ReferenceField), last_updated, and status.
    a. I stored important fields from the Spotify object into the database, include spotify_id, title, artists, image, album, duration, release_data, total_tracks, and most importantly type. This is so that when I fetch a user library, I don't have to make a Spotify API call for the player data to render the tracker in the library.
    b. Note that some fields are only used for track types (e.g. album and duration) and others for album types (release_date, total_tracks, and listened_tracks), which is why using NoSQL is nice in this case.
3. Review: This tracks the user (as a ReferenceField), last_updated, rating, and comment. We also need the type when we make Spotify API calls to identify the type of player, and we only need to store the spotify_id and title this time for rendering reviews (without making additional API calls).
```



**Another Python Package or API:**



* Find and use another Python package or API.
* Must be a package/API we haven’t used in any of the projects (though anything mentioned in lecture material that wasn’t used in a project is fair game).
* You can use a package/API we’ve already used if you’re using it in a way that’s _very_ different from how we used it in the projects.
* Must affect the user experience in some way.

Examples (feel free to use these or come up with your own):



* Flask-Mail to send emails to users
* CalorieNinjas API with Requests package to access the API
* Spotify API
* Requests package to display data retrieved from an HTTP request
* BeautifulSoup4 to display data parsed from a website
* SciPy, NumPy, SymPy, etc
* Plotly  
* Discord OAuth
* CAS 

```
Describe what Python package or API you will use and how it will affect the user experience:

I am using the Spotify Web API: https://developer.spotify.com/documentation/web-api. There are two main operations to use with the API.
1. Search for Item: This is used in our search feature, where we use client credentials we get to fetch for players matching a query at a given offset (necessary when trying to load more).
2. Get Player by ID: This is used whenever we click on a player, where we want to get a detailed view of the player, including the name, image, album (if it's a track), artists, release, duration, popularity, list of tracks (if it's an album), etc. Again we use client credentials to fetch the player detail.
    a. Now if we fetch an album, what we do is that we want to store the list of tracks. So for each of the tracks for the album, we make an API call to fetch each of the tracks and store them.
    b. I also defined a "detailed" parameter, which we set to True whenever we want the detailed view for the player, and False otherwise (e.g. search, or even just listing tracks for an album).
```

**Presentation:**

* Doesn’t have to be pretty but it needs to be usable.
  
> [!NOTE]
> Theres going to be a EC part of the project due on the last day of the semester where you can use tailwind/react/svelte/css to make your website more pretty, up to 25%!!!

## Grading

<table>
  <tr>
   <td>Requirement
   </td>
   <td>Points
   </td>
  </tr>
  <tr>
   <td>Proposal submitted
   </td>
   <td>100
   </td>
  </tr>
  <tr>
   <td>Writeup submitted (same format as the proposal) 
   </td>
   <td>100
   </td>
  </tr>
  <tr>
   <td>Registration and Login
   </td>
   <td>75
   </td>
  </tr>
  <tr>
   <td>Forms
   </td>
   <td>50
   </td>
  </tr>
  <tr>
   <td>Blueprints
   </td>
   <td>50
   </td>
  </tr>
  <tr>
   <td>Database
   </td>
   <td>50
   </td>
  </tr>
  <tr>
   <td>Another Python package or API
   </td>
   <td>75
   </td>
  </tr>
</table>


Total: 500 points
