# Project Title

This Project is a Parking management & reservation system.

This system is developed to help individuals book vehicle parking space online and also offer their parking space for rent.

Customers can reserve car parking spaces, access additional services and even pay online.

Parking owners can register their parking lot in our system and offer their parking spaces for rent.

## Screenshots
![Screenshot from 2022-05-06 15-57-01](https://user-images.githubusercontent.com/46793124/167123039-6c41ba3d-41e3-4907-a926-4c88fd42b1f2.png)

![Screenshot from 2022-05-06 15-59-52](https://user-images.githubusercontent.com/46793124/167123399-b60c5b07-dec1-4084-8a90-f781bedcc8bd.png)

## Installation

To run this project you must have python 3.8 (or newer version) & pip & postgresql installed on your device.

Install the requirements:
```bash
  pip install -r requirements.txt
```

If you encounter errors during installation of psycopg2 package try:
```bash
  pip install psycopg2-binary
```

Connect the project to your desired postgresql database in settings.py:
```bash
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'NAMEOFDB',
        'USER': 'postgres',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
```
Create database tables and migrations:
```bash
  python manage.py makemigrations
  python manage.py migrate
```

Run the project:
```bash
  python manage.py runserver
```

