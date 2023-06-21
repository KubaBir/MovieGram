# MovieGram
## Backend project of a movie forum website.
### Used Technologies:
- Python
- Django
- Django Rest Framework
- Docker
- Redis
- Celery
- PostgreSQL
- BeautifulSoup
### Project handles:
- Creating custom users
- Authenticating users
- Friend system
- Posting system
- Comments on Posts
- Scraping data from a external website right into user profiles, based on the nickname provided when registering a user.
- Celery tasks 
- Redis docker image to handle celery's functionalities.

Project is fully built on docker and with PostgreSQL as a database. 

Rest Api in this project is documented and displayed with the use of drf-spectacular library and swagger.
## Available endpoints:
### User endpoints :
/api/user/
- create/ (POST)
- me/ (GET)
- me/ (PUT)
- me/ (PATCH)
- token/ (POST)
### User profiles endpoints:
/api/user_profiles/
- api/user_profiles/ (GET)
- {id}/ (GET)
- my_profile/ (GET)
- my_profile/ (PATCH)
### Movies endpoints:
/api/movies/
- api/movies/ (GET)
- {id}/ (GET)
- add_movie/ (POST)
### Main page endpoints:
/api/main_page/
- -//-(GET)
- -//- (POST)
- {id}/ (GET)
- {id}/ (PUT)
- {id}/ (PATCH)
- {id}/ (DELETE)
### Comments endpoints:
/api/comments
- -//- (GET)
- -//- (POST)
- {id}/ (GET)
### Friends Profiles endpoints:
/api/friends-profiles/ 
- -//- (GET)
- {id} (GET)
### Friend Requests endpoints:
/api/friends_requests/
- -//- (GET)
- {id}/responding_to_invs/ (GET)
- {id/invitations_sent_by_me/ (GET)
- sending_inv/ (POST)
### Directors endpoints:
/api/directors/
- -//- (GET)
- {id}/ (GET)
- {id}/ (DELETE)
### Schema endpoints:
/api/schema

Project done in collaboration to test github group working skills. 


