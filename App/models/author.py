from App.database import db
from datetime import *
from .author_publication import *

class Author(db.Model):
    __tablename__ = "author"
    
    id = db.Column(db.Integer, primary_key=True)
    fname =  db.Column(db.String, nullable=False)
    lname =  db.Column(db.String, nullable=False)
    email =  db.Column(db.String, nullable=True)
    institution =  db.Column(db.String, nullable=True)
    qualifications = db.Column(db.String(120), nullable=True)
    publications = db.relationship('AuthorPublication', backref=db.backref('Author'))

    def __init__(self, fname, lname, email, institution, qualifications):
            self.fname = fname
            self.lname = lname
            if email:
                self.email = email
            if institution:
                self.institution = institution
            if qualifications:
                self.qualifications = qualifications
    # class Author(db.Model):
    #     __tablename__ = "author"
    #     id = db.Column(db.Integer, primary_key=True)
    #     name =  db.Column(db.String, nullable=False)
    #     dob = db.Column(db.DateTime, nullable=True)
    #     qualifications = db.Column(db.String(120), nullable=True)
    #     publications = db.relationship("Publication", secondary=AuthorPublication, viewonly=True)

    

    # def __init__(self, name, dob, qualifications):
    #     self.name = name
    #     if dob:
    #         self.dob = datetime.strptime(dob, "%d/%m/%Y")
    #     if qualifications:
    #         self.qualifications = qualifications

    # def get_publications(self):
    #     # return [publication.toJSON() for publication in self.publications]
    #     return [publication.toJSON() for publication in self.publications]

    def toJSON(self):
        return{
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'institution': self.institution,
            'qualifications': self.qualifications,
            # 'publications': self.publications,
        }

