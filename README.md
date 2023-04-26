# MovieGram
## Backend project of a movie forum website.
This project containts full rest api for movie forum website. It handles:
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

