# <center >People connect</center>
This service will allow you to create a user and profile, upload photos, follow someone's profile and see who is following yours. You will also be able to create messages and add photos to them and find the message you need by text, title, and who created it.

---
           

## <center >Manual Build</center>
1. In Pycharm, open the folder where the project will be stored.
2. Cloning the project.  
    ```shell
    git clone https://github.com/AnatoliyPilipey/PeopleConnect.git
    ```
3. Go to the folder with the project.  
    ```shell 
    cd chat
    ```
4. Creating a virtual environment.  
    ```shell 
    python -m venv venv
    ```
5. Activating the virtual environment.  
    * For Apple 
    ```shell     
    source env/bin/activate
    ```
    * For Windows  
    ```shell 
    venv\Scripts\activate
    ```
6. Install the required modules from the specified list.  
    ```shell 
    pip install -r requirements.txt
    ```
7. Create an .env file and put the secret key in it.  
    ```shell 
    DJANGO_SECRET_KEY = django-insecure-c46_n6!jh7fmu06qh%b3_gjyu89zn-2blq7xck#p+m3y7m56=b
    PERMISSIONS_STATUS = on
    ```
8. Perform database creation migrations.  
    ```shell 
    python manage.py migrate
    ```
9. Using the fixture with test data, we fill the database.  
    In settings.py set:
    ```shell 
    USE_TZ = True
    ``` 
    Load db
    ```shell 
    python manage.py loaddata db.json
    ```  
    In settings.py set:
    ```shell 
    USE_TZ = False
    ```  
10. Disabling authentication. Specify in the .env
    ```shell 
    PERMISSIONS_STATUS = off
    ```
11. To use JWT authentication.  
    Specify in the .env
    ```shell 
    PERMISSIONS_STATUS = on
    ```  
    Run server
    ```shell 
    python manage.py runserver
    ```  
    Token Obtain Pair
    ```shell 
    http://127.0.0.1:8000/api/user/token/
    ```  
    Use next login & password
    ```shell 
    admin@admin.com
    ```  
    ```shell 
    password
    ```
    ![Access Token](access%20token.jpg)  
    Use ModHeader by specifying 
    ```shell 
    Bearer you_access_Token_time_life_30_min
    ```  
    ![ModHeader](ModHeader.jpg)
12. Running the server  
    ```shell 
    python manage.py runserver
    ```
13. At this point, the app runs at  
    ```shell 
    http://127.0.0.1:8000/api/chat/
    ```
14. Register new User  
    ```shell 
    http://127.0.0.1:8000/api/user/create/
    ```
15. Swagger  
    ```shell 
    http://127.0.0.1:8000/api/swagger/
    ```
16. Redoc
    ```shell 
    http://127.0.0.1:8000/api/redoc/
    ```

#### Note  
Set PERMISSIONS_STATUS = on when you run the python manage.py test

_Thank you for familiarizing yourself with my work._

