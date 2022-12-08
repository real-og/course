This is course project "Resource for studing English via Song-texts".

To run application locally follow these steps:

1. Make sure you have installed python and MySQL
[I had python3.10, MySQL 8]

2. CLone or download this repository to your PC.

3. Make sure you have pip installed and run "pip install pipenv" in the directory
[we are installing virtual enviroment manager]

4. Create file named ".env" and put there credentials for your database and some secret key like this:
database=nameofmydb
user=myuser
password=mypassword
host=localhost
port=3306
secret_key=mysecret

5. Open MySQL shell and make database structure. 
[You may complete this step by inserting content from structure.sql to the shell.]

6. Run "pipenv shell" and "pipenv install"
[these two will create virtual enviroment and download libs]

7. Run "python app.py" and open "http://localhost"

Congrats!
