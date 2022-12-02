from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required
# for exceptions
import sys

from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
)

from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/signup', methods=["POST"])
def create_user_route():
    data = request.get_json()
    if not data:
        return "Missing request body.", 400
    username = data['username']
    password = data['password']
    if not username or not password:
        return "Missing username or password parameter.", 400
    user = create_user(username, password)
    if not user:
        return "Failed to create.", 400
    return user.toJSON(), 201

# @user_views.route('/publications', methods=["GET"])
# def get_publications():
#     args = request.args
#     if not args:
#         pubs = get_all_publications_json()
#         return jsonify(pubs), 200
#     author_id = args.get("author")
#     query = args.get("query")
#     pubs = []
#     if author_id:
#         pubs = get_author_publications(author_id)
#     if query:
#         query = query.lower()
#         print(query)
#         pubs = filter(lambda pub: query in pub['title'].lower(), pubs)
#     return jsonify(list(pubs)), 200
        

@user_views.route('/publications', methods=["POST"])
@jwt_required()
def post_publication():
    list1 = []
    data = request.get_json()
    author_names = data['authors']
    # coauthor_names = data['coauthors']
    # authors = sum ( [get_author(fname,lname) for fname,lname in author_names], [] )                
    # coauthors = sum ( [get_author_by_name(name) for name in coauthor_names], [] )
    # return jsonify(author_names)
    for name in author_names:
        list1.append(name.split(" "))
    try:
        new_pub = create_publication(list1, data['title'], data['url'], data['publisher'],data['date'])
    except Exception as e:
        return f'Could not create due to exception: {e.__class__}', 400
    return new_pub.toJSON(), 201

@user_views.route('/author', methods=["POST"])
@jwt_required()
def create_author_profile():
    data = request.get_json()
    # return jsonify(data)
    try:
        new_author = create_author(data['fname'], data['lname'], data['email'],data['institution'], data['qualifications'])
    except Exception as e:
        return f'Could not create due to exception: {e.__class__}', 400 
    return new_author.toJSON(), 201

@user_views.route('/author', methods=["GET"])
def get_author_profile():
    authors = get_all_authors_json()
    return jsonify(authors)

@user_views.route('/publication', methods=["GET"])
def get_publications():
    publications = get_all_publications_json()
    return jsonify(publications)

@user_views.route('/authorpublication', methods=["GET"])
def get_authorPublications():
    authorpublications = get_all_authorPublications()
    return jsonify(authorpublications)

@user_views.route('/pubtree', methods=['GET'])
def get_pub_tree():
    args = request.args
    author_id = args.get('author_id')
    if not author_id:
        return "Must provide ID.", 400

    pubs = get_author_publications(author_id)
    return jsonify(pubs)
