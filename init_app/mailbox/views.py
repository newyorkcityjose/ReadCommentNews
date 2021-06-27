from flask import Blueprint
from flask import Flask, render_template, request, session, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import exists
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from datetime import date
import datetime 
import arrow 

import os

from init_app.mailbox.forms import MessageForm
from init_app.models import db, connect_db, User, Bookmark, Comment, bcrypt, Follower, Inbox, Discussion

mailbox = Blueprint('mailbox', __name__, template_folder='templates')


@mailbox.route('/user_profile/<int:user_id>/', methods=["GET"])
@login_required
def user_list(user_id):
    """List Users"""

    user = db.session.query(User).filter_by(id=user_id).first()
    bookmarks = db.session.query(Bookmark).filter_by(user_id=user_id)
    print(bookmarks)
    return render_template("users/list_users/user_profile.html", user=user, bookmarks=bookmarks)


@mailbox.route('/mailbox/', methods=["GET"])
@login_required
def mailbox_view():
    return render_template("users/mailbox/mailbox.html")


@mailbox.route('/compose_message/<int:id>/', methods=["GET", "POST"])
@login_required
def compose_message(id):
    """Compose message"""

    reply = request.args.get("reply")
    form = MessageForm()
    if reply is None:
        user = db.session.query(User).filter_by(id=id).first() 
    elif reply is not None:
        discussion = db.session.query(Discussion).filter_by(id=id).first()
        message = sorted(discussion.inbox_messages, key=lambda x: x.create_date, reverse=True)[0]
        print(message)
    print(reply)
    if request.method == "POST":
        if reply is None:
            if form.validate_on_submit():
                message = Inbox(
                    user_id=user.id,
                    title=form.title.data,
                    message=form.message.data,
                    author_message=current_user.id
                )
                db.session.add(message)
                discussion = Discussion(
                    user_dis_start_id=current_user.id,
                    user_dis_follow_id=user.id,
                    title=message.title
                )
                db.session.add(discussion)
                discussion.inbox_messages.append(message)
                db.session.commit()
            else:
                print(form.errors)

        elif reply is not None:
            print("Here")
            if form.validate_on_submit():
                message_new = Inbox(
                    user_id=message.author_message,
                    title=form.title.data,
                    message=form.message.data,
                    author_message=current_user.id,
                )
                db.session.add(message_new)
                discussion.inbox_messages.append(message_new)
                db.session.commit()
            else:
                print(form.errors)

        return redirect('/mailbox/')
    if reply:
        return render_template("users/mailbox/compose.html", user=message.message_from, form=form, discussion=discussion, reply=True) 
    else:
        return render_template("users/mailbox/compose.html", user=user, form=form) 

@mailbox.route('/inbox/', methods=["GET", "POST"])
@login_required
def inbox():
    # """Inbox message"""
    # discussions = db.session.query(Discussion).filter(Discussion.inbox_messages.any(Inbox.user==current_user))
    discussions = db.session.query(Discussion).filter_by(user_dis_follow_id=current_user.id)
    print([i for i in discussions])
    messages = [{
        "id": discussion.id,
        "username": discussion.user_dis_start.username,
        "title": discussion.title,

        "content": sorted(discussion.inbox_messages, key=lambda x: x.create_date, reverse=True)[0].message[:10]
        } for discussion in discussions]
    print(messages)

    return jsonify(messages)

@mailbox.route('/outbox/', methods=["GET", "POST"])
@login_required
def outbox():
    """Inbox message"""
    discussions = db.session.query(Discussion).filter_by(user_dis_start_id=current_user.id)
    print([i for i in discussions])
    messages = [{
        "id": discussion.id,
        "username": discussion.user_dis_follow.username,
        "title": discussion.title,

        "content": sorted(discussion.inbox_messages, key=lambda x: x.create_date, reverse=True)[0].message[:10]
        } for discussion in discussions]
    print(messages)

    return jsonify(messages)

@mailbox.route('/inbox/<int:discussion_id>/', methods=["GET", "POST"])
@login_required
def message(discussion_id):
    """Inbox message"""
    discussion = db.session.query(Discussion).filter_by(id=discussion_id).first()
    messages = discussion.inbox_messages

    result = [
        {
            "from": message.message_from.username,
            "to": message.user.username,
            "message": message.message,
            "create_date": message.create_date.strftime("%Y-%m-%d")
        } for message in messages
    ]
    print(result)
    return jsonify(result)
