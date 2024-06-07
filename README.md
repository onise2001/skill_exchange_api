# Skill exchange api
Welcome to the Skill Exchange API ! This project provides a backend service for a skill exchange platform where users can teach and learn various skills. The API is built using Django and Django REST Framework (DRF), providing endpoints to manage users and courses.


## Installation 

To get a local copy up and running, follow these steps:

- Clone the repository:
```
git clone https://github.com/onise2001/skill_exchange_api.git
```
- Navigate to project directory:
```
cd skill_exchange_api
```
- Create virtual environment with the following coomand (python3 if on linux):
```
python -m venv venv
```
- Install required modules by running the following command:
```
pip install -r requirements.txt
```
- Create and connect a PostgreSQL database in settings.py

- Run migrations (python3 if on linux):
```
python manage.py migrate
```


## Usage

- Run server (python3 if on linux):
```
python manage.py runserver
```

#### Authentication
This project uses django's JSON Web Tokens for registration and login purposes. 

- **Registration:** By sending a POST request to this api endpoint, ```/auth/signup/``` , with correct request body, a new User will be created and added to the database.


- **Login:** By sending a POST request to this api endpoint, ```/auth/login/``` , with correct request body, you will get a pair of access and refresh tokens.

#### Regular Users have following fields:
- Username
- Email
- Password
- Role (Student, Tutor, Admin)


#### API endpoints
## Endpoints
- **List courses:** By sending a GET request to this api endpoint, ```/course/```, you will get a list of all courses currently in the database.

- **View course:** By sending a GET request to this api endpoint, ```/recipe/{id}```, you will get an instance of the course with that id.

- **View courses you are enrolled in:** By sending a GET request to this api endpoint, ```/my_courses/```, you will get a list of all courses you are currently enrolled in.

- **View courses you created:** By sending a GET request to this api endpoint, ```/created_courses/```, you will get a list of all courses you created.

- **View all student on a course:** By sending a GET request to this api endpoint, ```/students_on_course/```, with correct request body. you will get a list of all student on a course you requested in request body if you are that course's tutor or an admin user.

- **Create course:** By sending a POST request to this api endpoint, ```/course/``` , with correct request body, a new course will be created and added to the database if you have the permission to do so.

- **Edit course:** By sending a PUT request to this api endpoint, ```/course/{id}``` , with correct request body, a course with that id will be edited with the information you provided in the request body if you have the permission to do so.

- **Delete recipe:** By sending a DELETE request to this api endpoint, ```/course/{id}``` ,  a recipe with that id will be deleted from the database if you have the permission to do so.

- **Enroll in a course:** By sending a PUT request to this api endpoint, ```/enroll/{id}``` , with correct request body, you will be added to that course's list of students, if, you are authenticated as a student, you are not already enrolled and course is available.

- **Leave a course:** By sending a DELETE request to this api endpoint, ```/leave_course/{id}```, you will be removed form that course's list of students, if you are authenticated as a student and you were enrolled in that course.

- **Review a course:** By sending a PUT request to this api endpoint, ```/review/{id}``` , with correct request body, a review will be added to that course's list of review if you are enrolled in that course.

- **Rate tutor:** By sending a PUT request to this api endpoint, ```/rate_tutor/{id}``` , with correct request body, a tutor of the course with that id will get rated by you if you are enrolled in said course.

- **Admin add student to course:** By sending a PUT request to this api endpoint, ```/add_student/{pk}/{id}``` , with correct request body, a student with that id will be added to a course with that pk, with a status of admin_added=True,  even if the course is already full.

- **Give tutor permission to add a student to a course:** By sending a POST request to this api endpoint, ```/tutor_admin/``` , with correct request body, a tutor will recive a permission to add a student they specified in the request body to a course they also specified in request body, even if that course is full.

- **Tutor adds student to a course:** By sending a POST request to this api endpoint, ```/tutor_add_student/``` , with correct request body, a tutor will add a student they specified in the request body to a course they also specified in request body, even if that course is full.

##### For more detailed information about API endpoint see the swagger documentaion at /swagger or /redoc


#### Filters

- **Name:** By sending a GET request to this api endpoint, ```/course?name={course_name}```, you will get a list of all courses that have name fields that contain the name provided.

- **Tutor rating:**By sending a GET request to this api endpoint, ```/course?tutor_rating={rating}```, you will get a list of all courses that have tutor who have rating greater or equal to the rating provided.

- **Available:**By sending a GET request to this api endpoint, ```/course?available={True or False}```, you will get a list of all courses that are either available or not available depending on your input.



