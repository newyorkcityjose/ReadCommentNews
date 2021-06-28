from flask import Blueprint
from flask import Flask, render_template, request, session, flash, redirect, session, g, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import exists
from init_app import newsapi, CURR_USER_KEY 
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date
from init_app.picture_handler import add_profile_pic
import datetime 
import arrow 

import os

from init_app.users.forms import AddUserForm, LoginForm, UpdateProfileForm
from init_app.bookmark.forms import CommentForm
from init_app.models import db, connect_db, User, Bookmark, Comment, bcrypt, Follower, Inbox, Discussion


users = Blueprint('users', __name__, template_folder='templates')


######################################
# Homepage

@users.route('/')
def home():

    if g.user:
            user_id = current_user.id
            g_user = g.user.id

            if not current_user.is_authenticated:
                flash("Access unauthorized.", "danger")
                return redirect("/login")
    
            bookmarks = [bookmark for bookmark in db.session.query(Bookmark).filter_by(user_id=current_user.id)]
            return render_template('index.html', g_user=g.user, bookmarks=bookmarks, user_id=user_id)
    else:        
        topheadlines = newsapi.get_top_headlines(sources=None, category='business', q=None, language='en', country='us', page_size=12)

        articles = topheadlines['articles']
        desc = []
        news = []
        img = []
        url = []

        for i in range(len(articles)):
            myarticles = articles[i]

            news.append(myarticles['title'])
            desc.append(myarticles['description'])
            img.append(myarticles['urlToImage'])
            url.append(myarticles['url'])
            

            mylist = zip(news, desc, img, url)
        return render_template('index.html', context=mylist)


##########################################
# login/logout/signup form

@users.before_request
def add_user_to_g():
    """if we are log in"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user"""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """logout"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


def news_top_headlines():
    """Top headline news"""

    topheadlines = newsapi.get_top_headlines(sources=None, q=None, language='en', country='us', page_size=12)

    articles = topheadlines['articles']
    desc = []
    news = []
    img = []
    url = []
    ids = []
    time = []
    saved = []
    

    for i in range(len(articles)):
        myarticles = articles[i]

        ids.append(i)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])
        time.append(str(myarticles["publishedAt"])[11:-1])
        saved.append(db.session.query(Bookmark.url).filter_by(url=myarticles['url'], user_id=current_user.id).first() is not None)

        mylist = zip(ids, news, desc, img, url, saved, time)
    return render_template('/users/news/news.html', context=mylist)

##########
## signup

@users.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup form"""

    form = AddUserForm()

    if form.validate_on_submit():
        print(form.picture.data)
        try:
            user = User.signup(username=form.username.data, password=form.password.data, email=form.email.data, bio=form.bio.data)
            print(user)
            print(form.picture.data)
            if form.picture.data:
                username = user.username
                pic = add_profile_pic(form.picture.data, username)
                user.profile_image = pic
            db.session.commit()

        except IntegrityError:
            flash('username already taken', 'danger')
            return render_template('signup.html', form=form)

        return redirect('/')

    else:
        return render_template('signup.html', form=form)

###########
## login user

@users.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login"""
    
    form = LoginForm()
    
    if form.validate_on_submit():
        
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            login_user(user)
            user_id = current_user.id
            return render_template('index.html')
        flash('invalid', 'danger')

    return render_template('/users/login.html', form=form)

##########
## logout
@users.route('/logout')
def logout():
    """Handle user logout"""

    logout_user()
    flash("You have successfully logged out.", 'success')
    return redirect('/')

###########################################
# user routes

@users.route('/users/<int:user_id>')
def news_list_users(user_id):
    """the list of users news"""

    user = User.query.get_or_404(user_id)
    
    return render_template('users/show.html', user=user)

##################################
# top headline news 


@users.route('/news/', methods=["GET", "POST"])
@login_required
def user_news_technology():
    """user business news"""

    if not current_user.is_authenticated:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    cat = request.args.get("cat", None)
    
    form = CommentForm()

    if request.method == 'POST':
        bookmark = db.session.query(Bookmark).filter_by(url=request.form['url'], user_id=current_user.id).first()
        # print(bookmark)
        if bookmark:
            db.session.delete(bookmark)
        else:
            new_bookmark = Bookmark(
                    news=request.form["news"],
                    description=request.form["desc"], 
                    url = request.form["url"],
                    user_id = current_user.id
                )
            # print(new_bookmark)
            db.session.add(new_bookmark)
        db.session.commit()
        return jsonify({"data": "success"})

    if request.method == "GET":
        if cat is not None and cat in ["technology", "business", "entertainment", "sports"]:
            topheadlines = newsapi.get_top_headlines(sources=None,
            category=cat, q=None, language='en', country='us', page_size=12)
        else:
            topheadlines = newsapi.get_top_headlines(sources=None, q=None, language='en', country='us', page_size=12)
            cat = None
        articles = topheadlines['articles']
        desc = []
        news = []
        img = []
        url = []
        ids = []
        time = []
        saved = []
        print(articles[0]["publishedAt"])
        date = datetime.datetime.strptime(articles[0]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        print(date)
        for i in range(len(articles)):
            myarticles = articles[i]

            ids.append(i)
            news.append(myarticles['title'])
            desc.append(myarticles['description'])
            img.append(myarticles['urlToImage'])
            url.append(myarticles['url'])
            time.append(datetime.datetime.strptime(myarticles["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%a %B %d %Y %I:%M:%S %p"))
            saved.append(db.session.query(Bookmark.url).filter_by(url=myarticles['url'], user_id=current_user.id).first() is not None)

            mylist = zip(ids, news, desc, img, url, saved, time)
        return render_template(f'users/news/news.html', context={"cat": cat.upper() if cat is not None else "TOP HEADLINES", "mylist": mylist}, form=form)
    else:
        return render_template('404.html')

##################################
## profile

@users.route('/profile/', methods=["GET", "POST"])
@login_required
def user_profile():
    """Edit profile"""

    form = UpdateProfileForm()

    if request.method == "GET":
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        return render_template('users/profile/profile.html', form=form)

    if request.method == "POST":

        if form.validate_on_submit():
            if form.picture.data:
                username = current_user.username
                pic = add_profile_pic(form.picture.data, username)
                current_user.profile_image = pic

            if form.password.data:
                hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
                current_user.password = hashed_pwd

            current_user.email = form.email.data
            current_user.bio = form.bio.data

            db.session.commit()
            print("Account changed")

    return render_template('users/profile/profile.html', form=form)


@users.route('/list_users/<int:user_id>/', methods=["GET", "POST"])
@login_required
def list_users(user_id):
    """List Users"""

    if request.method == 'POST':
        users_following = db.session.query(Follower).filter_by(
            user_id=current_user.id,
            user_follower_id=user_id,
        ).first()
        if users_following is None:
            new_follow = Follower(
                user_id=current_user.id,
                user_follower_id=user_id
            )
            db.session.add(new_follow)
        else:
            db.session.delete(users_following)
        db.session.commit()

    filt = request.args.get("filter")

    users = db.session.query(User).all()
    users_following = db.session.query(Follower).filter_by(user_id=current_user.id)
    if filt:
        users = [{
            "id": user.id,
            "username": user.username,
            "user_follower": user.id in [usr.user_follower_id for usr in users_following],
            "profile_image": user.get_profile_image,
        } for user in users if user.id in [usr.user_follower_id for usr in users_following]]
    else:
        users = [{
            "id": user.id,
            "username": user.username,
            "user_follower": user.id in [usr.user_follower_id for usr in users_following],
            "profile_image": user.get_profile_image,
        } for user in users]
    return render_template("users/list_users/list_users.html", users=users)