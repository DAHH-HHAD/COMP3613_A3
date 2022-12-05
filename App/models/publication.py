from App.database import db
# from .author import *
from .author import *
from .author_publication import *


# AuthorPublication = db.Table(
#     "authorpublication",
#     db.Column("author_id", db.ForeignKey("author.id"), primary_key=True),
#     db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True)
# )

class Publication(db.Model):
    __tablename__ = "publication"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=False)
    url = db.Column(db.String(120), nullable=False, unique=True)
    publisher = db.Column(db.String(120), nullable=False, unique=False)
    date = db.Column(db.DateTime, nullable=True)
    # authors = db.relationship("Author")
    authors = db.relationship('AuthorPublication', backref=db.backref('publication'))

# class Publication(db.Model):
#     __tablename__ = "publication"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(120), nullable=False, unique=True)
#     # authors = db.relationship("Author")
#     authors = db.relationship(Author, secondary=AuthorPublication, backref=db.backref('publication'))
#     coauthors = db.relationship(Author, secondary=CoAuthorPublication)

    def __init__(self, title, url, publisher, date):
            self.title = title
            self.url = url
            self.publisher = publisher
            if date:
                self.date = datetime.strptime(date, "%d/%m/%Y")
            # self.authors.extend(authors)
            

    # def __init__(self, title, authors, coauthors):
    #     self.title = title
    #     # self.authors.append(authors)
    #     # [self.authors.append(author) for author in authors]
    #     self.authors.extend(authors)

    #     if coauthors:
    #         self.coauthors.extend(coauthors)
    
    def toJSON(self):
        return{
            "id": self.id,
            "title": self.title,
            "url": self.url, 
            "publisher": self.publisher, 
            "date": self.date,
            # "authors": self.authors
            # "authors": [author.toJSON() for author in self.authors],
            # "coauthors": [coauthor.toJSON() for coauthor in self.coauthors]
        }
    # def toJSON(self):
    #     return{
    #         "id": self.id,
    #         "title": self.title, 
    #         "authors": [author.toJSON() for author in self.authors],
    #         "coauthors": [coauthor.toJSON() for coauthor in self.coauthors]
    #     }

    # def toJSON2(self):
    #     return{
    #         "id": self.id,
    #         "title": self.title, 
    #     }

