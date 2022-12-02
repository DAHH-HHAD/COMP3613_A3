from App.database import db
from .author import *
from .publication import *


class AuthorPublication(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    publicationTitle = db.Column(db.String, nullable=True)
    authorId = db.Column(db.Integer, db.ForeignKey('author.id'))
    publicationId = db.Column(db.Integer, db.ForeignKey('publication.id'))
    authorPosition = db.Column(db.Integer, nullable = False)

    def __init__(self, authorId, publicationTitle, publicationId, authorPosition):
        self.authorId = authorId
        self.publicationTitle = publicationTitle
        self.publicationId = publicationId
        self.authorPosition = authorPosition
        
    def toJSON(self):
        return{
            'id': self.id,
            'publicationTitle' : self.publicationTitle,
            'authorId': self.authorId,
            'publicationId': self.publicationId,
            'authorPosition': self.authorPosition,
        }

# AuthorPublication = db.Table(
#     "authorpublication",
#     db.Column("author_id", db.ForeignKey("author.id"), primary_key=True),
#     db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True)
# )

# CoAuthorPublication = db.Table(
#     "coauthorpublication",
#     db.Column("author_id", db.ForeignKey("author.id"), primary_key=True),
#     db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True)
# )