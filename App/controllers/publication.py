from App.models import Publication
from App.models import AuthorPublication
from App.models import Author
from App.controllers import *
from App.database import db
import ast
# this function will create a publication post and calls create_authorPublication
def create_publication(authors, title, url, publisher, date):
    if (bool(Publication.query.filter_by(title ='title', url = 'url').first())):
        return False
    new_publication = Publication(title = title, url = url, publisher = publisher, date = date)
    db.session.add(new_publication)
    db.session.commit()
    publication = Publication.query.filter_by(url = url).first()
    create_authorPublication(authors, title,  publication.id)
    return new_publication
# create authorPublication when adding a new publication to an author
# authors with position 0 are primary authors
# get_author finds author by id and returns the author, if the author
# does not exist, it calls create_author and returns the created author
def create_authorPublication(authors, title, publicationId):
    i = 0
    authors = ast.literal_eval(authors)
    # new_authorPublication = AuthorPublication(authorId, publicationId, authorPosition)
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
    print (authpubs)
    return authpubs

#returns AuthorPublication if found for given publication id's i.e list of authors on a publication
def get_AuthorPublication_by_publicationId(id):
    authpubs = AuthorPublication.query.filter_by(publicationId = id).all()
    if not authpubs:
        return False
    for authpub in authpubs:
        print(authpub.authorId)
    print (authpubs)
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
    stack.append(author)
    authorset.add(author.authorId)
    while stack:
        author = stack.pop()
        # author = get_AuthorPublication_for_authorid(authorID)
        publications = get_AuthorPublication_by_authorId(authorID)
        if not publications:
             return false
        for publication in publications:
            pubset.add(publication.publicationId)
            authors =  get_AuthorPublication_by_publicationId(publication.publicationId)
            if not authors:
                return false
            for author in authors:
                authorset.add(author.authorId)
                if (author.authorId not in authorset):
                    stack.append(author) 
    print("Publications: ")            
    for publication in pubset:
        print( "\t" + str(publication)) 
    print("authors")
    for author in authorset:
        print("\t" + str(author))
                

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