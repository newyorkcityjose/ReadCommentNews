from flask import Blueprint
from flask import Flask, render_template, request, session, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import exists
from newsapi import NewsApiClient
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from datetime import date
import datetime 
import arrow 
import os

from init_app.models import db, connect_db, User, Bookmark, Comment, bcrypt, Follower, Inbox, Discussion
from init_app.bookmark.forms import CommentForm

bookmark = Blueprint('bookmark', __name__, template_folder='templates')


@bookmark.route('/users/<int:user_id>/bookmark', methods=["GET", "POST"])
@login_required
def user_bookmark(user_id):
    """Show all bookmark list"""

    user_id = current_user.id
    

    if request.method == "GET":
        if not current_user.is_authenticated:
            flash("Access unauthorized.", "danger")
            return redirect("/login")
        
        bookmarks = [bookmark for bookmark in db.session.query(Bookmark).filter_by(user_id=user_id)]
        # print([bookmark.news for bookmark in bookmarks])
        return render_template('users/bookmark/bookmark.html', bookmarks=bookmarks, user_id=user_id)


def get_comments_exist(bookmark_id, comment_id=None):

    out_comments = []
    
    if comment_id is not None:
        comments = db.session.query(Comment).filter_by(bookmark=bookmark_id, parent_comment=comment_id)

    else:
        comments = db.session.query(Comment).filter_by(bookmark=bookmark_id, parent_comment=None)
    # print([comment.id for comment in comments])
    for comment in comments:
        comments_exist = db.session.query(Comment).filter_by(bookmark=bookmark_id, parent_comment=comment.id) 
        out_comments.append({
            "id": comment.id,
            "user_id": db.session.query(User).filter_by(id=comment.user_id).first().username,
            "comment": comment.comment,
            "create_date": comment.create_date.strftime("%B, %d %Y, %I:%M %p %Z"),
            "comments_exists": get_comments_exist(bookmark_id, comment.id) if comments_exist.first() is not None else None
        })

    return out_comments

#####################################
## bookmark id

@bookmark.route('/users/<int:user_id>/bookmark/<int:bookmark_id>', methods=["GET", "POST"])
@login_required
def user_bookmark_id(user_id, bookmark_id):
    """Show bookmark id"""

    user_id = user_id
    bookmark = db.session.query(Bookmark).filter_by(id=bookmark_id).first()
    comments = db.session.query(Comment).filter_by(bookmark=bookmark_id)
    # out_comments = get_comments_exist(bookmark.id)
    # print(out_comments)
    form = CommentForm()
    return render_template('users/bookmark/bookmarkid.html', bookmark=bookmark, user_id=user_id, form=form)

###################################
## comments

@bookmark.route('/comment/<int:bookmark_id>/', methods=["GET", "POST"])
@login_required
def comment_bookmark(bookmark_id):
    """POST comment into database"""

    user_id = current_user.id
    form = CommentForm()

    if request.method == "POST":
        try:

            text = request.form["comment"].split(":", 1)[1] if ":" in request.form["comment"] else request.form["comment"]
            new_comment = Comment(
                comment=text,
                bookmark=bookmark_id,
                user_id = current_user.id
            )
            db.session.add(new_comment)
            
            comment_id = request.form["comment"].split(":", 1)[0][1:]
            # print(comment_id)
            if comment_id.isnumeric():
                comment_exist = db.session.query(Comment).filter_by(id=comment_id)
                if comment_exist.first() is not None:
                    new_comment.parent_comment = comment_exist.first().id
            
            db.session.commit()
            # print(new_comment)
        
        except IntegrityError:
            return render_template('/', form=form)

        return redirect(f'/users/{user_id}/bookmark/{bookmark_id}')

    else:
        data = get_comments_exist(bookmark_id)
        # print(data)
        return jsonify(data)
