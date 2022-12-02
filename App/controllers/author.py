from App.models import Author
from App.database import db


def create_author(fname, lname, email, institution, qualifications):
    if (bool(Author.query.filter_by(fname='fname', lname = 'lname').first())):
        return False

    newAuthor = Author(fname = fname, lname = lname, email = email, institution = institution, qualifications = qualifications)
    db.session.add(newAuthor)
    db.session.commit()
    return newAuthor
# def create_author(name, dob, qualifications):
#     new_author = Author(name=name, dob=dob, qualifications=qualifications)
#     db.session.add(new_author)
#     db.session.commit()
#     return new_author

def get_author(fname, lname):
    author = Author.query.filter_by(fname = fname, lname = lname).first()
    if not author:
        author = create_author(fname = fname, lname = lname, email = None, institution = None, qualifications = None)
        db.session.add(author)
        db.session.commit()
        return (author)
    return author

def get_all_authors():
    return Author.query.all()

def get_all_authors_json():
    authors = Author.query.all()
    if not Author:
        return []
    authors = [author.toJSON() for author in authors]
    return authors

def get_author_by_name(fname):
    print(name)
    authors = Author.query.filter_by(fname=fname)
    authors = [author for author in authors]
    # this code should be in a different method
    if not authors:
        new_author = create_authorAuthor(fname = fname, lname = lname, email = None, institution = None, qualifications = None)
        authors = [new_author]
        return authors
    return authors

def get_author_publications(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()

def getpublicationtree(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()
    