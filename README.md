<h1>WorkHard is a Blog for technology</h1>

`WorkHard is a technology blog` that covers various topics such as mathematics, physics, and coding. It was created as the basis for my own website, but everyone is welcome to use it. We provide news and updates on these subjects. Additionally, our blog offers assistance to students with their homework, projects, labs, and exercises. You can contact us through our website. We also have a Discord server for real-time communication. Alternatively, you can send us your files, and we will provide detailed step-by-step explanations and assistance`


## Goals
- An easy way to create a simple, secure website with a blog
- Support for text-based and photo-based blog formats
- Easy authoring in HTML, Markdown (with code formatting), or JSON
- Easy customization of site layout and formatting
- Support for Windows and Linux hosting Flask
- Quick search of post content, including simple search queries
  
## Structure
- `/app.py` Entry point for the application, configures the server and static content
- `/script.js` Handles image slideshows, post dates, and dropdown menus
- `/templates/HTML` directory manages the layout of the webpage
- `/static/CSS` directory manages the styling and formatting of the HTML conten

## Instructions

1. `pip Install Flask, bcrypt, Flask-PyMongo, passlib, bson, Flask-Mail, Jinja2`
1. `cd myweb`
1. `python app.py`
1. Open <http://localhost:5000/> and verify
1. Commit changes to repository
1. Deploy repository to hosting service

# Front-End Stack
- HTML: Defines the structure and content of your web pages
- CSS: Styles HTML elements, defining layout, colors, typography, and other visual aspects to enhance presentation
- JavaScript: Adds interactivity and dynamic functionality to your web pages, including features such as image sliders, real-time timestamp updates (e.g., updateTimeAgo), dropdown menus, rating systems, pagination (showPostsForPage), and more

# Back-End Stack
- Server-side Languages (Python Flask): Handles server-side logic, data processing, and communication with databases. Flask, a Python web framework, provides a lightweight and flexible platform for building web applications, allowing you to create dynamic content, handle user requests, and manage session data effectively
- Databases(MongoDB): Stores user registration information in a NoSQL document database
- MongoDB (handled by Flask-PyMongo): Store user information such as name, email, hashed password, registration, time, etc
- Flask_mail:
    - Integrates email functionality into your Flask application, enabling the sending of emails such as visitor's contracts to Gmail
    - Implement email verification with registration, ensuring active and valid user emails
    - Forget-password feature with two-factor authentication (2FA), requiring users to enter a verification code for added security
- Flask sessions: Store user authentication state and information between requests
- Bcrypt (handled by Passlib): Securely hash user passwords before storing them in the database

#AI Help
- Explore Python and Flask framework for backend development and familiarize with MongoDB.
- Receive guidance on Python syntax, registration, login, and contracts.
- Establish backend-to-frontend connectivity.
- Collaborate on JavaScript concepts and brainstorm ideas.
## License

[CD](LICENSE)
