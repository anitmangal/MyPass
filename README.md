# MyPass
This project was undetaken by [Anit Mangal](https://github.com/anitmangal) and Rahul Rohatgi as a CBSE Computer Science (New) terminal project.

## Objective
It is an offline terminal-based Password Manager. It uses MySQL connectivity to store and maintain databases.

## Run Instructions
- Make sure that the MySQL service is running on your system.
- Make sure that there a user is created and the password is known. (Will be required during runtime)
- Run MyPass.exe
  
## Build Instructions
- Have the MySQL service running along with a login known.
- Install the required libraries.
```
pip install -r requirements.txt
```
- Run the Python program.
```
python MyPass.py
```

## Features
- Capable of supporting login details for multiple people as different user accounts with password strength checking.
- Intuitive menus to support actions.
- Able to add Website Name, Username and Password for any website. The password is stored in an encrypted form in the MySQL database.
- Able to retrieve login details for any website and decrypt the password and display it.
- Able to modify stored Username or Password for any website.
- Able to delete login details for any website.
