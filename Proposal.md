
## CMSC 388J Final Project Proposal

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

Spotify Tracker. In a nutshell, it's an IMDB for Spotify (but much, much simpler). The core features of this app include.
1. Allow users to search for albums/tracks (we will refer to the collection of albums and tracks as "players").
2. Allow users to keep track of players they are currently listening to or want to listen to or already listened to, and number of tracks listened to.
3. Allow users to rate and review players.
```



## Requirements

Note that some of these requirements overlap with each other so some features may satisfy multiple requirements.  

**Registration and Login:**



* There needs to be some sort of user control: logging in, registering, logging out.
* Certain features should only be available to logged-in users.

```
Describe what functionality will only be available to logged-in users:

There will be two features restricted to logged-in users.
1. Maintain a library of players and track status (plan to listen to, currently listening to, already listened to).
2. Rate and review players (as well as view ratings and reviews).
```



**Forms:**



* At least 4 forms (can include registration and login forms)
* Must be CSRF protected

```
List and describe at least 4 forms:

1. Login user: need username and password
2. Register user: need email, username, password
3. Search for players: just a search query
4. Review (includes rating) for players: need rating (1-10) and comment
5. Add player to library
6. Edit player status in library: edit number of tracks listened to and overall status
7. Remove player from library
```



**Blueprints:**



* Must have at least 2 blueprints 
* Each blueprint should have at least 2 visible and accessible routes

```
List and describe your routes/blueprints (don't need to list all routes/blueprints you may have–just enough for the requirement):

1. Users
  a. GET/POST "/register"
  b. GET/POST "/login"
  c. POST "/logout"
  d. GET "/user/<user_id>" (user detail, includes library and reviews)
2. Players
  a. GET/POST "/" (for searching players)
  b. GET "/search" (display the results for player search)
  c. GET/POST "/player/<player_id>" (player detail, includes the forms to add rating/review for players and add/edit/remove from collection, and if it is an ALBUM, include the list of TRACKS)
  d. GET "/library" (display the players in the library, clicking on each goes to /player/<player_id>)
```



**Database:**



* Must use MongoDB

```
Describe what will be stored/retrieved from MongoDB:

1. User: username, email, password (hashed), library (list of references to players), reviews (list of references to player reviews)
2. Player: spotify_id (from Spotify), tracks_listened, status, type (album or track)
3. Review: spotify_id (from Spotify), rating, comment, type (album or track)
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

Spotify Web API. Core functionalities include search feature and detail results for players (album/track). Check it out here: https://developer.spotify.com/documentation/web-api.
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
