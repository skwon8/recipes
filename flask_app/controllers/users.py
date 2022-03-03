from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():

    return render_template("index.html")


@app.route('/users/register', methods=['POST'])
def register_user():

    if not User.validate_new_user(request.form):
        print("validation fails")
        return redirect('/')

    else:
        print("validation success")
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        print(data)
        User.create_new_user(data)
        flash("User registered! Log in with that Account")
        return redirect('/')


@app.route('/users/login', methods=['POST'])
def login_user():
    # determine if users exists

    user_email = User.get_user_by_email(request.form)

    if not user_email:
        flash("User with given Email does not exist. Please Try Again.")
        return redirect('/')

    # check password against DATABASE

    if not bcrypt.check_password_hash(user_email.password, request.form['password']):
        flash("Password is Incorrect!")
        return redirect('/')

    # if two of those commands above fails, we need to redirect the user back to the main page. But if they're not, then logged in.

    # user is logged in

    session['user_id'] = user_email.id
    session['user_email'] = user_email.email
    session['user_first_name'] = user_email.first_name
    session['user_last_name'] = user_email.last_name

    return redirect('/recipes')


@app.route('/users/logout')
def logout():
    session.clear()
    flash("Now You are Logged Out! Please Log In Again!")
    return redirect('/')
