ud858
=====

Course code for Building Scalable Apps with Google App Engine in Python class


# Running the App

* Add your API key to the following files

>`static/js/app.js` -> line 89

> `settings.py` -> line 15


* Add the application ID

> `app.yaml` -> line 1

* Launch Google App Engine
* Go to File -> Add existing application
* Select the app folder and import
* Run the app at localhost:[port number]


## Design choices

The session is implemented as being a child of Conference. This makes it easier to retrieve sessions from a
specific conference. Each session has a field which holds the speaker name (String) and we can do a simple
query to retrieve sessions of a particular speaker:

`sessions = sessions.filter(Session.speaker == request.speaker)`


## Additional queries

1) GetConferencesByCity

  Returns all conferences taking place in a specific city. Useful to
  find conferences in your city.

2) getConferencesAvailable

  Returns all conferences that have seats available.


## Solving a query issue

>Let’s say that you don't like workshops and you don't like sessions after 7 pm. How would you handle a query for all
non-workshop sessions before 7 pm? What is the problem for implementing this query? What ways to solve it did you
think of?"

Datastore has query restrictions: It can't have inequality filters in two or more properties and when you have an
inequality filter, it must be sorted first. In this case as we don't have too many session types, we could use ndb.OR
and query for lectures OR talks OR [any other session type excluding workshops]. This way we could exclude an inequality.
Now we just have one inequality startTime > 19.

