# Private Limited Companies Registration App for Estonian RIK
### Test Work

## Short technical preview
#### Used programming languages:
Python v3.10.5  
HTML  
JS  
#### Used frameworks:
Django v4.0.5

#### Database:
PostgreSQL  
Driver psycopg2 v2.9.3

#### Additional libraries:
Bootstrap v5.0.2 beta  
Faker v13.13.0 - fake data population library  
Whitenoise v6.2.0 - library for deployment of static files with Microsoft Azure

#### Programming software:
JetBrains PyCharm Community Edition v.2022.2EAP

#### Deployment:
GitHub - Azure pipeline for automatic deployment with Microsoft Azure Services  
(F1 free plan for web apps and shared server for database)

## About app
In accordance with task, application allows to register Private Limited Companies with their shareholders,  
search for Companies in database, view details and edit Shareholders capitals.
The application usability was tested with Edge Browser in Windows 11 OS. 

## How to run application

### Working deployed demo online: https://rik-python.azurewebsites.net

### Running from source code:
1. Clone GitHub Repository: https://github.com/JevgeniF/rik_test_jfenko.git  
2. Open bash terminal in folder cloned from repository
3. Create virtual environment by running ```python -m venv venv ```  
4. Activate virtual environment by command ```venv\Scripts\activate```
5. The source code has ```requirements.txt``` file with all required frameworks and libraries.  
    Install them by ```pip install -r requirements.txt  ```
6. Run app on local python server with command ```python manage.py runserver```
    By default the server address is https://127.0.0.1:8000

#### !!! In case if local server can't find bootstrap css files and UI looks ugly !!!
The source code on GitHub is used for deployment and update of online demo (please find link above), therefore the
Whitenoise library is used for proper setup of static files (including css and js) for Microsoft Azure Web App Services
Disable the Whitenoise by commenting out Whitenoise middleware from ```MIDDLEWARE = []``` section
in ```rik_test_jfenko/setup.py``` file:
~~~
'whitenoise.middleware.WhiteNoiseMiddleware'
~~~

Also comment out from static files section in ```rik_test_jfenko/setup.py```:
~~~
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
~~~
and add instead
~~~
STATICFILES_DIRS = [BASE_DIR / 'static/']
~~~

### Additional setup:
### Database
By default, the database provided by me, as developer, and stored online. The database is PostgreSQL v13.

In order to use local database or another online database service: 
1. please change database settings in
```rik_test_jfenko/setup.py``` file:
~~~
# setup for PostgreSQL:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': [database.name],
        'USER': [username],
        'PASSWORD': [password],
        'HOST': [host],
        'PORT': '5432' #default PostgreSQL port
    }
}
~~~
##### Please note, that compatibility with other DB providers, than Postgres, was not checked.

2. Delete migrations file ```0001_initial.py``` in ```register/migrations``` folder.
3. Run ```python manage.py makemigrations``` to create new migrations file.
4. Run ```python manage.py migrate``` to migrate project models to database. This operation will automatically create  
    all required database tables in accordance with ```register/models.py``` file and Django setups.

### Database fake data seeding
The root folder of cloned repository contains ```app_data_populator.py```. To seed fake data to the database, run
main method from file:
~~~
if __name__ == '__main__':
    print("Populating data")
    populate_osayhingud_with_oustajad(10)
    print("Populating completed")
~~~
or run in activated virtual environment from terminal ```python app_data_populator.py ```. 
  
The script will add 5 fake companies with 1 juridic person-shareholder and 4 physical persons-shareholders to the
database.

### Administration panel
In case if you need to use Django administration panel on your local server https://127.0.0.1:8000/admin,
you need to create first superuser by using terminal.
In the root folder of downloaded repository, run ```python manage.py createsuperuser```

## Short user guide.
### 'Avaleht'
Avaleht has 2 rows with search fields.  
1st one is with name and code filed to query Private Limited Company entities from database by part of name and/or
register code.  
  
2nd one is physical isik checkbox (which acts as a switch between queries) and field for name(and/or family name) and 
code.  
If checkbox ticked, the search returns companies linked with queried physical person, otherwise - with queried juridical
person.  

It is not necessary to use all fields or rows. Each search row returns separated table of search results if queried.
Each row in search results contains ```Lisainfo``` link, which leads to Private Limited Company details - ```'Osaühingu Andmete Vaade'```.  

### 'Osaühingu Andmete Vaade'
Shows all PLC data including shareholders.  
Additional functionality added in order to change showed PLC shareholders capitals, or add another shareholder.  
In order to use it, use link ```Muuta osakapitalide suurus või lisada osanikud```

### 'Osaühingu Osakapitali Suurendamise Worm'
The page allows to change capital of one exact shareholder at once or add another juridical person or physical person or 
both.

~~~
Please note that the app will not change anything, if total capital of company will be less than 2500 EUR in case 
of shareholder capital change... or if the new shareholder's capital will consist non-numeric character.
~~~

### 'Osaühingu Asutamise Vorm'
You can get to the page by right top corner link on Avaleht with the same name.
The form allows to add new PLC with up to five juridical persons as shareholders and/or up to five physical persons as
shareholders. It is not necessary to fill all five juridical and five physical persons, the main thing is to fill fields
right way and watch that PLC capital and sum of shareholders capitals are equal.
