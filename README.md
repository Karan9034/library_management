# Library Management App

## About

Library management system built using Flask for Librarian to maintain books, register members, issue books, charge the members on returning the books, and help them record transactions. This app abides and follows the guidelines mentioned at <a href="https://frappe.io/dev-hiring-test">Frappe Dev Hiring Test</a>. Built using Flask, Bootstrap 4, Jinja2 and SQLite.

## Instructions

1. Set up the .env file by renaming `.env.example` file to `.env` and adding a SECRET_KEY for the Flask application.
2. Create a virtual environment using:
```
python -m venv env
```
3. Install the dependencies using:
```
pip install -r requirements.txt
```
4. Set up the database using:
```
python setupDB.py
```
5. Run the application on `http://localhost:5000` by using:
```
python run.py
```

Check out the deployed version of this app on Heroku:
[https://library-management-flask.herokuapp.com/](https://library-management-flask.herokuapp.com/)

## Screenshots

![Home](screenshots/Home.png "Home")

<br>

![Books](screenshots/Books.png "Books")

<br>

![Members](screenshots/Members.png "Members")

<br>

![Transactions](screenshots/Transactions.png "Transactions")

<br>

![Register Member](screenshots/Register_Member.png "Home")

<br>

![Member_Registered](screenshots/Member_Registered.png "Member_Registered")

<br>

![Edit_Member_Details](screenshots/Edit_Member_Details.png "Edit_Member_Details")

<br>

![Import_Books](screenshots/Import_Books.png "Import_Books")

<br>

![Books_Imported](screenshots/Books_Imported.png "Books_Imported")

<br>

![Issue_Book](screenshots/Issue_Book.png "Issue_Book")

<br>

![Issue_Successful](screenshots/Issue_Successful.png "Issue_Successful")

<br>

![Book_Returned](screenshots/Book_Returned.png "Book_Returned")

<br>

![Reports](screenshots/Reports.png "Reports")

<br>

![Reports_2](screenshots/Reports_2.png "Reports_2")