# Practice Journal

Practice Journal is a tool that helps users log their practice sessions, record notes, and stay organized. Users can search through a preloaded database of piano works and add pieces to their current projects. Once a piece is added to the user_projects database, they can log practice sessions for that piece. 

The app includes a basic streak feature and a display of total weekly practice minutes to encourage consistency and discipline.

## How to Run

1. Make sure Python is installed
2. Install Flask:
   pip install flask
3. Run the application:
   python app.py
4. Open your browser and go to:
   http://127.0.0.1:5000

## Features

- User authentication (register, login, account management)
- Searchable database of piano works
- Add and manage practice projects
- Log and edit practice sessions
- Practice streak tracking
- Weekly practice time tracking
- Custom piece creation


## Database Design

- users: stores user credentials
- piano_works: preloaded and user-generated piano pieces
- user_projects: links users to pieces they are practicing
- practice_sessions: logs individual practice sessions, linked to user_projects via project_id

## login.html 
login.html displays a log in page, where users can enter their username and password if they have an existing account. If they do not have an account, there is a link to reroute them to the register page.

## register.html 
register.html is for users to create a new account. When they create a password, it is required that the password is at least 6 characters. The password strength increase as users add special characters, numbers, uppercase and lowercase letters. It is indicated with a strength meter beneath the password.

## index.html 
index.html displays the home page. Here users can see their streak, which tells them how many days in a row they've practiced, as well as their total weekly minutes. The home page also displays all their current projects as well as all their past practice sessions. Users can log their practice sessions here in the home page, or in /project/{{piece_id}}. By clicking on a past session, users can edit their practice notes and session minutes. They can also choose to delete the practice session entirely.

## add-piece.html and results.js:
add-piece.html will display the add-piece page, where users can use the search bar to find a piece they want to practice. When users type into the search bar, results.js listens for an input. It takes the input and sends it to the /search-pieces route in app.py, which then makes an sql query to check if the user's input exists in the existing piano_works database. If it exists, the complete title and composer name are taken from the table, and sent back to results.js in json form. The javascript updates the html to display all pieces that match the query with an "add" button. Users can click the button to add the piece to their current projects. 

If the query does not match any pieces in the piano_works database, users can manually type in the composer and title. However, when a user type a custom piece, it is added to the piano_works database and becomes visible to all other users. This design allows the database to grow organically as users add new pieces. However, it introduces potential issues such as duplicate entries, typos, or inappropriate content. Currently, the system assumes cooperative users, but future improvements may include moderation or validation mechanisms.

## projects.html
This page displays all pieces in user_projects where user_id matches the current session id. There is a filter select menu where users can find projects based on their status, such as 'in progress', 'archived', 'completed', or 'all'. Clicking on a project redirects the user to project/{{piece.id}}, which renders the project.html template. 

## project.html
is the page for the specific piece the user clicked on. The exact contents of the page are determined by the piece id in the URL. In this page, users can log a practice session. They can enter the amount of minutes spent practicing, as well as include notes and comments about their session. After the practice session is logged, it will be displayed towards the bottom of the page. If the user clicks on the practice session, a modal will pop up and they will be able to edit the notes or practice minutes of the session. They also have the option to completely delete that specific practice session. In this page, the users can also change the status of the project. They can archive it, to hide it from their list of current projects, mark it as complete, or delete the project entirely. The home page is very similar, the main difference is that users cannot delete or change the status of a project from the home page. 

## account.html

This page is for users to edit their account information.  They can change their username and password, or delete their account. Retyping their current password is required for changing any of these fields. In the future, I will likely have users sign up with an email address, so that they can get a code in case they forget their password. 

## layout.html

This file is basically just for the nav bar and styling flashed messages

## auth.js

This page is just for the password strength indicator. It requires the password to be at least 6 characters. The strength is increased as certain conditions are met, such as including capital letters, lowercase letters, special characters, and numbers.


## home.js

Home.js is responsible for resizing the practice notes textarea, triggering a delete confirmation pop up message, as well as opening up the modal for editing each individual practice session.

## app.py 

This file handles all the backend routes, sql queries, and more. 


## reflection

Building this project greatly strengthened the skills I learned in CS50, and it taught me a lot about full-stack development. The biggest thing I learned was how to connect frontend javascript and AJAX to backend Flask routes and a relational database. 

In the future, I would like to keep improving and expanding this app. I will potentially aim this product towards teachers, where they can host a classroom for their students. Students can earn XP points by practicing, and compete with thier peers for a spot on the weekly practice leaderboard. Teachers can see student's practice notes, which can provide insight into how they are structuring their practice sessions.