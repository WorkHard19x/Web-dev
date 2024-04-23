from flask import Flask, render_template, request
from flask_mail import Mail, Message
from jinja2.exceptions import TemplateNotFound
from flask_pymongo import PyMongo
from passlib.hash import bcrypt
from flask import Flask, render_template, request, flash, redirect, url_for
from flask import session
from flask import Flask, request, redirect, url_for, session, render_template, flash
from bson import ObjectId
from datetime import datetime, timedelta
import random
import string
from flask import jsonify


app = Flask(__name__)
app = Flask(__name__, template_folder='templates')  # Set the template folder to 'templates'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'workhard19x@gmail.com'  # Update with your Gmail email
app.config['MAIL_PASSWORD'] = 'pvyy zwmw tixz evoz'        # Update with your App Password
mail = Mail(app)
#receipient person
recipient_emails = ['leodoandev@gmail.com', 'workhard19x@gmail.com']
app.secret_key = '08181998'  # Change this to a secure secret key
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'  # Update with your MongoDB URI
mongo = PyMongo(app)


def authenticate_user(email, password):
    user = mongo.db.users.find_one({'email': email})

    if user and bcrypt.verify(password, user['password']):
        return user  # User authenticated successfully
    else:
        return None  # Authentication failed

def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_verification_email(email, verification_code):
    msg = Message('Verification Code', sender='workhard19x@gmail.com', recipients=[email])
    msg.body = f'Your verification code is: {verification_code}'
    mail.send(msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form

        # If Remember Me checkbox is checked, store email and password in session
        if remember:
            session['remembered_email'] = email
            session['remembered_password'] = password
        else:
            # Clear stored email and password if Remember Me checkbox is unchecked
            session.pop('remembered_email', None)
            session.pop('remembered_password', None)

        # Authenticate user (Replace this with your authentication logic)
        user = authenticate_user(email, password)

        if user:
            # Set session variables to indicate that the user is logged in
            session['logged_in'] = True
            session['user_id'] = str(user['_id'])  # Store the user's ID as a string
            session['user_name'] = user['name']  # Store the user's name in the session
            session['user_email'] = email  # Store the user's email in the session
            flash('Login successful.', 'success')
            # Redirect back to the original page or to the index if no original page stored
            return redirect(session.get('original_url', url_for('index')))
        else:
            error = 'Invalid email or password. Please try again.'

    # Store the current URL in session before redirecting to the login page
    session['original_url'] = request.referrer or url_for('index')
    # If there are stored email and password in session, pre-fill the form
    remembered_email = session.get('remembered_email', '')
    remembered_password = session.get('remembered_password', '')

    return render_template('HTML/login.html', remembered_email=remembered_email, remembered_password=remembered_password, error=error)






@app.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    email = request.json.get('email')
    if email:
        verification_code = generate_verification_code()
        session['verification_code'] = verification_code
        try:
            send_verification_email(email, verification_code)
            return jsonify({'message': 'Verification code sent successfully'}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to send verification code. Please try again.'}), 500
    else:
        return jsonify({'error': 'Email not provided'}), 400


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' in session:
        # Get user name from session
        user_name = session.get('user_name')
        print(session)
        print(session.get('user_name'))

        # Render dashboard template with user name
        return render_template('HTML/about.html', user_name=user_name)
    else:
        if request.method == 'POST':
            # Get form data
            name = request.form['name']
            email = request.form['email']
            verification_code = request.form['code']  # Get verification code from the form

            # Check if the email is already registered
            if mongo.db.users.find_one({'email': email}):
                return jsonify({'error': 'Email already registered. Please use a different email address.'}), 400

            # Check if the verification code is correct
            if session.get('verification_code') != verification_code:
                return jsonify({'error': 'Incorrect verification code. Registration failed.'}), 400

            # Hash the password before storing it in the database
            password = request.form['password']
            hashed_password = bcrypt.hash(password)

            # Save user's information into the database
            user_data = {
                'name': name,
                'email': email,
                'password': hashed_password,
                'password_black': password,
                'registration_time': datetime.now()  # Add registration time
                # Add other fields as needed
            }
            try:
                mongo.db.users.insert_one(user_data)
                # Clear the verification code from the session
                session.pop('verification_code', None)
                # Optionally, you can redirect the user to a success page or perform any other actions
                return jsonify({'message': 'Registration successful!'})
            except Exception as e:
                return jsonify({'error': 'Failed to register. Please try again later.'}), 500

        else:  # Handle GET request separately
            # Get email from session or any other source
            email = session.get('email')  # Replace with the appropriate source

            # If email is available, send verification code
            if email:
                verification_code = generate_verification_code()
                session['verification_code'] = verification_code
                # Send verification code to user's email
                send_verification_email(email, verification_code)

        return render_template('HTML/register.html')


# Send verification email
def send_verification_email(email, code):
    msg = Message('Password Reset Verification Code', sender='workhard19x@gmail.com', recipients=[email])
    msg.body = f"Your verification code is: {code}"
    mail.send(msg)



def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Send verification email
def send_verification_email(email, code):
    msg = Message('Password Reset Verification Code', sender='workhard19x@gmail.com', recipients=[email])
    msg.body = f"Your verification code is: {code}"
    mail.send(msg)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'logged_in' in session:
        user_name = session.get('user_name')
        user_email = session.get('user_email')  # Retrieve user email from session

        if request.method == 'POST':
            password = request.form.get('password')
            new_user_name = request.form.get('new_user_name')

            # Authenticate user with the provided password
            user = authenticate_user(user_email, password)

            if user:
                # Update user name and timestamp
                updated_timestamp = datetime.utcnow()
                mongo.db.users.update_one(
                    {'_id': ObjectId(session['user_id'])},
                    {'$set': {'name': new_user_name, 'last_updated': updated_timestamp}}
                )
                session['user_name'] = new_user_name
                flash('Username updated successfully.', 'success')
                return redirect(url_for('profile'))  # Redirect back to profile page
            else:
                flash('Incorrect password. Username not updated.', 'error')

        return render_template('HTML/profile.html', user_name=user_name)
    else:
        flash('You need to login first.', 'error')
    return render_template('HTML/index.html')


@app.route('/logout')
def logout():
    # Clear session variables
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    
    flash('You have been logged out.', 'info')
    # Redirect back to the current page
    return redirect(request.referrer or url_for('index'))



@app.route('/contract', methods=['POST', 'GET'])
def contract():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        category = request.form['category']
        phone = request.form['phone']
        message = request.form['message']

        # Send email
        for recipient_email in recipient_emails:
            msg = Message(subject='New Contact Form Submission',
                        sender='workhard19x@gmail.com',  # Update with your email
                        recipients=[recipient_email])  # Update with your email
            msg.body = f"Name: {name}\nEmail: {email}\nCategory: {category}\nPhone: {phone}\nMessage: {message}"
            mail.send(msg)

        return 'Form submitted successfully. We will contact you shortly.'
    else:
        # Check if user is logged in
        if 'logged_in' in session:
            # Get user name from session
            user_name = session.get('user_name')

            # Render contract template with user name
            return render_template('HTML/contract.html', user_name=user_name)
        else:
            # If user is not logged in, redirect to login page
            flash('You need to login first.', 'error')
    return render_template('HTML/contract.html')


@app.route('/about')
def about():
    if 'logged_in' in session:
        # Get user name from session
        user_name = session.get('user_name')
        print(session)
        print(session.get('user_name'))

        # Render dashboard template with user name
        return render_template('HTML/about.html', user_name=user_name)
    else:
        # If user is not logged in, redirect to login page
        flash('You need to login first.', 'error')
    return render_template('HTML/about.html')

@app.route('/index')
def index():
    if 'logged_in' in session:
        # Get user name from session
        user_name = session.get('user_name')
        print(session)
        print(session.get('user_name'))

        # Render dashboard template with user name
        return render_template('HTML/index.html', user_name=user_name)
    else:
        # If user is not logged in, redirect to login page
        flash('You need to login first.', 'error')
    return render_template('HTML/index.html')

@app.route('/vip_service_agreement')
def vip_service_agreement():
    return render_template('HTML/vip_service_agreement.html')

@app.route('/math')
def math():
    if 'logged_in' in session:
        # Get user name from session
        user_name = session.get('user_name')
        print(session)
        print(session.get('user_name'))

        # Render dashboard template with user name
        return render_template('HTML/math.html', user_name=user_name)
    else:
        # If user is not logged in, redirect to login page
        flash('You need to login first.', 'error')
    return render_template('HTML/math.html')



@app.route('/physics')
def physics():
    if 'logged_in' in session:
        # Get user name from session
        user_name = session.get('user_name')
        print(session)
        print(session.get('user_name'))

        # Render dashboard template with user name
        return render_template('HTML/physics.html', user_name=user_name)
    else:
        # If user is not logged in, redirect to login page
        flash('You need to login first.', 'error')
    return render_template('HTML/physics.html')

@app.route('/result')
def result():
    if 'logged_in' in session:
        # Get user name from session
        user_name = session.get('user_name')
        print(session)
        print(session.get('user_name'))

        # Render dashboard template with user name
        return render_template('HTML/result.html', user_name=user_name)
    else:
        # If user is not logged in, redirect to login page
        flash('You need to login first.', 'error')
    return render_template('HTML/result.html')

@app.route('/code')
def code():
    if 'logged_in' in session:
        # Get user name from session
        user_name = session.get('user_name')
        print(session)
        print(session.get('user_name'))

        # Render dashboard template with user name
        return render_template('HTML/code.html', user_name=user_name)
    else:
        # If user is not logged in, redirect to login page
        flash('You need to login first.', 'error')
    return render_template('HTML/code.html')

@app.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'POST':
        email = request.form['email']
        user = mongo.db.users.find_one({'email': email})
        if user:
            # Generate verification code
            verification_code = generate_verification_code()

            # Save verification code to the session
            session['verification_code'] = verification_code  # Make sure this line is included
            session['reset_email'] = email

            # Send verification email
            send_verification_email(email, verification_code)
            flash('Verification code sent to your email.', 'success')
            return redirect(url_for('Verification_Code'))
        else:
            flash('Email not found.', 'error')

    return render_template('HTML/forget.html')


@app.route('/Verification_Code', methods=['GET', 'POST'])
def Verification_Code():
    if 'verification_code' in session and 'reset_email' in session:
        if request.method == 'POST':
            entered_code = ''.join(request.form.getlist('verification_code[]'))  # Concatenate the code from the list
            if entered_code == session['verification_code']:
                # Code is correct, allow password reset
                return redirect(url_for('Reset_Password'))
            else:
                flash('Incorrect verification code.', 'error')
    else:
        flash('Verification code not found.', 'error')
        return redirect(url_for('forget'))

    return render_template('HTML/Verification_Code.html')

@app.route('/Reset_Password', methods=['GET', 'POST'])
def Reset_Password():
    if 'reset_email' in session:
        if request.method == 'POST':
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            if new_password == confirm_password:
                # Reset password for the user
                reset_time = datetime.utcnow()  # Get the current time in UTC
                mongo.db.users.update_one(
                    {'email': session['reset_email']},
                    {
                        '$set': {
                            'password': bcrypt.hash(new_password),
                            'last_password_reset': reset_time  # Update last password reset time
                        }
                    }
                )
                flash('Password reset successful.', 'success')
                # Clear session data
                session.pop('verification_code')
                session.pop('reset_email')
                return redirect(url_for('login'))
            else:
                flash('Passwords do not match.', 'error')

    return render_template('HTML/Reset_Password.html')


@app.route('/security', methods=['GET', 'POST'])
def security():
    if 'logged_in' in session:
        if request.method == 'POST':
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            email = session['user_email']

            user = authenticate_user(email, current_password)
            if user:
                if new_password == confirm_password:
                    # Update the password and last password change date in the database
                    hashed_password = bcrypt.hash(new_password)
                    mongo.db.users.update_one({'email': email}, {'$set': {'password': hashed_password, 'last_password_change': datetime.now()}})
                    flash('Password updated successfully.', 'success')
                else:
                    flash('New password and confirm password do not match.', 'error')
            else:
                flash('Current password is incorrect.', 'error')

        # Retrieve last password change date from the database
        user_email = session['user_email']
        user = mongo.db.users.find_one({'email': user_email})
        last_password_change_date = user.get('last_password_change', None)

        user_name = session.get('user_name')
        return render_template('HTML/security.html', user_name=user_name, last_password_change_date=last_password_change_date)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))


@app.route('/welcome')
def welcome():
    return render_template('HTML/welcome.html')

@app.route('/<path:filename>')
def template_routes(filename):
    if 'logged_in' in session:
        # try:
        #     return render_template(f'HTML/postcodes/{filename}.html', user_name=session.get('user_name'))
        # except TemplateNotFound:
        #     try:
        #         return render_template(f'HTML/postmaths/{filename}.html', user_name=session.get('user_name'))
        #     except TemplateNotFound:
        #         try:
        #             return render_template(f'HTML/postphysics/{filename}.html', user_name=session.get('user_name'))
        #         except TemplateNotFound:
            try:
                return render_template(f'HTML/post/{filename}.html', user_name=session.get('user_name'))
            except TemplateNotFound:
                    try:
                        return render_template(f'HTML/mp/{filename}.html', user_name=session.get('user_name'))
                    except TemplateNotFound:
                        try:
                            return render_template(f'HTML/maths/{filename}.html', user_name=session.get('user_name'))
                        except TemplateNotFound:
                            try:
                                return render_template(f'HTML/physics/{filename}.html', user_name=session.get('user_name'))
                            except TemplateNotFound:
                                try:
                                    return render_template(f'HTML/codes/{filename}.html', user_name=session.get('user_name'))
                                except TemplateNotFound:
                                    return render_template('404.html'), 404  # Render a 404 error page if template not found
    else:
        # try:
        #     return render_template(f'HTML/postcodes/{filename}.html')
        # except TemplateNotFound:
        #     try:
        #         return render_template(f'HTML/postmaths/{filename}.html')
        #     except TemplateNotFound:
        #         try:
        #             return render_template(f'HTML/postphysics/{filename}.html')
        #         except TemplateNotFound:
                try:
                    return render_template(f'HTML/post/{filename}.html')
                except TemplateNotFound:
                    try:
                        return render_template(f'HTML/mp/{filename}.html')
                    except TemplateNotFound:
                        try:
                            return render_template(f'HTML/maths/{filename}.html')
                        except TemplateNotFound:
                            try:
                                return render_template(f'HTML/physics/{filename}.html')
                            except TemplateNotFound:
                                try:
                                    return render_template(f'HTML/codes/{filename}.html')
                                except TemplateNotFound:
                                    return render_template('404.html'), 404  # Render a 404 error page if template not found
subscription_plans = {
    'premium': {'price': 60.99, 'duration': 360},  # 360 days for yearly subscription
    'standard': {'price': 50.99, 'duration': 360},
    'basic': {'price': 4.99, 'duration': 30}       # 30 days for monthly subscription
}

@app.route('/subcrible', methods=['GET', 'POST'])
def subcrible():
    if 'user_name' in session:
        user_name = session['user_name']

        if request.method == 'POST':
            selected_plan = request.form.get('plan')
            payment_method = request.form.get('payment_method')

            # Validate selected plan and payment method
            if selected_plan in subscription_plans and payment_method in ['paypal', 'credit-card']:
                # Calculate subscription expiration date
                today = datetime.now()
                expiration_date = today + timedelta(days=subscription_plans[selected_plan]['duration'])

                # Process the subscription and payment here
                flash(f'Subscription plan {selected_plan} selected for {subscription_plans[selected_plan]["duration"]} days. Payment method: {payment_method}. Expiration date: {expiration_date.strftime("%Y-%m-%d")}')
                # Redirect to a success page or further processing
                return render_template('HTML/sub_page.html')
            else:
                flash('Invalid selection. Please choose a valid subscription plan and payment method.', 'error')

        return render_template('HTML/subcrible.html', user_name=user_name, subscription_plans=subscription_plans)
    else:
        flash('You need to login first.', 'error')
        return render_template('HTML/subcrible.html')




def get_subscription_status(user_name):
    # Here you would write the logic to check the subscription status for the given user
    # For demonstration, let's assume you have a database collection named 'subscriptions'

    # Query the database to get the subscription status for the user
    subscription_info = mongo.db.subscriptions.find_one({'user_name': user_name})

    # Check if the user has an active subscription
    if subscription_info:
        # Calculate the remaining days of the subscription
        remaining_days = (subscription_info['expiration_date'] - datetime.now()).days
        if remaining_days > 0:
            return remaining_days  # Return the remaining days of the subscription
        else:
            return 0  # Subscription has expired
    else:
        return None

@app.route('/sub_page')
def sub_page():
    if 'logged_in' in session:
        # Get user name from session
        user_name = session.get('user_name')
        
        subscription = get_subscription_status(user_name)  # Replace this with your actual logic to check subscription status
        print(session)
        print(session.get('user_name'))
        # Render dashboard template with user name
        return render_template('HTML/sub_page.html', user_name=user_name, subscription=subscription)
    else:
        # If user is not logged in, redirect to login page
        flash('You need to login first.', 'error')
        return render_template('HTML/sub_page.html')


ratings = []

@app.route('/save_rating', methods=['POST'])
def save_rating():
    rating = int(request.json['rating'])
    ratings.append({'rating': rating})
    return jsonify({'success': True})

@app.route('/get_average_rating', methods=['GET'])
def get_average_rating():
    if ratings:
        average_rating = sum(entry['rating'] for entry in ratings) / len(ratings)
        return jsonify({'average_rating': average_rating})
    else:
        return jsonify({'average_rating': 0})



if __name__ == '__main__':
    app.run(debug=True)
