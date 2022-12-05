from App.models import Publication
from App.models import AuthorPublication
from App.models import Author
from App.controllers import *
from App.database import db
import ast
from flask import Blueprint, render_template, jsonify
# this function will create a publication post and calls create_authorPublication
def create_publication(authors, title, url, publisher, date):
    if (bool(Publication.query.filter_by(title ='title', url = 'url').first())):
        return False
    new_publication = Publication(title = title, url = url, publisher = publisher, date = date)
    db.session.add(new_publication)
    db.session.commit()
    publication = Publication.query.filter_by(url = url).first()
    val = create_authorPublication(authors, title,  publication.id)
    if not val:
        return False
    return new_publication
# create authorPublication when adding a new publication to an author
# authors with position 0 are primary authors
# get_author finds author by id and returns the author, if the author
# does not exist, it calls create_author and returns the created author
def create_authorPublication(authors, title, publicationId):
    i = 0
    if(isinstance(authors, str)):
        authors = ast.literal_eval(authors)
    # new_authorPublication = AuthorPublication(authorId, publicationId, authorPosition)
    if len(authors) == 0:
        return False
    for author in authors:
        print(author)
        author = get_author(author[0], author[1])
        new_authorPublication = AuthorPublication(authorId = author.id, publicationTitle = title, publicationId = publicationId, authorPosition = i)
        db.session.add(new_authorPublication)
        db.session.commit()
        print('pubAuth created!')
        i += 1
    return i

# def add_author(Author, )

#returns AuthorPublication if found for given author id's
def get_AuthorPublication_by_authorId(id):
    authpubs = AuthorPublication.query.filter_by(authorId = id).all()
    if not authpubs:
        return False
    for authpub in authpubs:
        print(authpub.publicationId)
    #print (authpubs)
    return authpubs

#returns AuthorPublication if found for given publication id's i.e list of authors on a publication
def get_AuthorPublication_by_publicationId(id):
    authpubs = AuthorPublication.query.filter_by(publicationId = id).all()
    if not authpubs:
        return False
    for authpub in authpubs:
        print(authpub.authorId)
    #print (authpubs)
    return (authpubs)

def get_AuthorPublication_produced_by_publicationId(id):
    authpubs = AuthorPublication.query.filter_by(publicationId = id, authorPosition = 0).all()
    if not authpubs:
        return False
    for authpub in authpubs:
        print(authpub.authorId)
    #print (authpubs)
    return (authpubs)

#this function returns publications of given author, the publications of their co-authors, and the
#publications of the co-author's co-authors
def pub_tree_search(authorID):
    authpubs =  AuthorPublication.query.all()
    stack = []
    pubset = set()
    authorset =  set()
    if not authpubs:
        return False
    author = get_AuthorPublication_for_authorid(authorID)
    if not author:
        print ("Author not found")
        return False
    stack.append(author)
    authorset.add(author.authorId)
    while stack:
        i = 0
        print (str(i) + "rgferg")
        i += 1
        author = stack.pop()
        # author = get_AuthorPublication_for_authorid(authorID)
        publications = get_AuthorPublication_by_authorId(author.authorId)
        if not publications:
             return false
        for publication in publications:
            pubset.add(publication.publicationId)
            authors =  get_AuthorPublication_by_publicationId(publication.publicationId)
            if not authors:
                return false
            for author in authors:
                if (author.authorId not in authorset):
                    stack.append(author)
                    authorset.add(author.authorId)  
    print("Publications: ")
    list1 = []            
    for publication in pubset:
        print( "\t" + str(publication)) 
        pub = get_publication_by_id_toJSON(publication)
        list1.append(pub)
    print("authors")
    for author in authorset:
        print("\t" + str(author))
    return list1


def get_publication_by_id_toJSON(id):
    publication = Publication.query.filter_by(id = id).first()
    if not publication:
        return False 
    return  publication.toJSON()
             

def get_AuthorPublication_for_authorid(id):
    return  AuthorPublication.query.filter_by(authorId = id).first()


def get_publication(id):
    return Publication.query.get(id)

def get_all_publications():
    return Publication.query.all()

def get_all_authorPublications():
    authorpublications = AuthorPublication.query.all()
    return [authorpublication.toJSON() for authorpublication in authorpublications]

def get_all_publications_json():
    publications = Publication.query.all()
    if not publications:
        return []
    publications = [publication.toJSON() for publication in publications]
    return publications