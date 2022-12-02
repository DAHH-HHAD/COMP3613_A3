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