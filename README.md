<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h2 align="center">REPOSITORY: Registration, login/logout/update/reset password with English, German, French localization</h2>

</div>


<!-- ABOUT THE PROJECT -->
## About The Project

This repository hosts the code for a rest API implementation of the Users registration, change password, reset password login and logout with support for automatic translation into German and French with the ability to add other languages, also provided the ability to select the language of localization in the Django admin site.</br>
Also implemented asynchronous sending Email messages at registration , change and reset the password


Project documentation:
* [Api Endpoints (Postman collection)](docs/Google_auth_OTP_django_postman_collection.json)


### Built With

List any major frameworks/libraries used to bootstrap project.

* [Docker](https://docs.docker.com/engine/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* [Django](https://www.djangoproject.com/start/)
* [Django Rest Framework](https://www.django-rest-framework.org/)





<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

You should install following software first:
* Git
* Docker
* Docker-compose

### Installation

1.Move to existing project directory
   ```sh
   cd /home/user/project/
   ```
2.Initialize existing project directory python3
   ```sh
   git init
   ```
3.Create an environment called venv
   ```sh
   python3 -m venv ./venv
   ```
4.Activate virtual environment
   ```sh
   source venv/bin/activate
   ```
5.Clone the repo
   ```sh
   git clone 
   ```
6.Make first application build via docker-compose
   ```sh
   docker-compose up --build
   ```



### Project resources
_Run project on local machine_

   ```sh
   docker-compose up
   ```


_Finally local uri is..._

   ```sh
   http://localhost:8000/api/
   ```

### Tests running

_Connect to application container_

   ```sh
   docker exec -it {application container} /bin/bash
   ```

_Running tests on local machine_

   ```sh
  python3 manage.py test
   ```
### Flake8 running

   ```sh
   flake8 app
   ```

____
## Adding a new language or editing a translation
_To add a new language, you need to add it to the settings.py file in the root directory of the project in a similar format._


   ```sh
   LANGUAGES = [
    ('en', gettext_lazy('English')),
    ('de', gettext_lazy('German')),
    ('fr', gettext_lazy('French')),
]
   ```
   
_After that you should run this command to create "django.po" file which will contain lines that need to be translated or edited.'_

   ```sh
   django-admin makemessages -l {language code} --ignore venv
   ```

_Example:_

   ```sh
   #: app/api/serializers.py:62
msgid "Good evening, we are from Ukraine!"
msgstr "Доброго вечора, ми з України!"
   ```

_After editing the language file you need to compile the language package with the following command._

   ```sh
   django-admin compilemessages -l {language code} --ignore venv
   ```
______
_After each change of lines in code of application containing text that needs to be translated you need to run the command:_
   ```sh
   django-admin makemessages -l {language code} --ignore venv
   ```
_and:_
   ```sh
   django-admin compilemessages -l {language code} --ignore venv
   ```

[Full details are provided on Django's official website](https://docs.djangoproject.com/en/4.0/topics/i18n/translation/)


#### [Project Source]( https://github.com/sheleh/django_translations_template.git)
#### [License dependencies](LICENSE-DEPENDENCIES.md)