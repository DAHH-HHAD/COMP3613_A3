import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import *

from App.main import create_app
from App.database import create_db
from App.models import User, Author, Publication
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user,
    create_publication,
    get_all_authors_json,
    create_author,
    create_publication,
    get_all_publications_json,
    get_author
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_user_toJSON(self):
        user = User("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class AuthorUnitTests(unittest.TestCase):

    def test_new_author(self):
        author = Author(fname='Carl', lname='Thompson', email='cto@gmail.com', institution='UWI', qualifications='MSc.Party')
        assert author.fname == "Carl" and author.lname == "Thompson"and author.email == "cto@gmail.com" and author.institution == "UWI" and author.qualifications == "MSc.Party"

    def test_author_toJSON(self):
        author = Author(fname='Carl', lname='Thompson', email='cto@gmail.com', institution='UWI', qualifications='MSc.Party')
        author_json = author.toJSON()
        self.assertDictEqual(author_json, {
            'id': None,
            'fname': "Carl",
            'lname': "Thompson",
            'email': "cto@gmail.com",
            'institution': "UWI",
            'qualifications': "MSc.Party",
        })

class PublicationUnitTests(unittest.TestCase):
    def test_new_publication(self):
        # authors = []
        # coauthors = []
        # author = Author("Bob Moog", "05/08/2001", "BSc. Computer Science")
        # authors.append(author)
        # coauthor = Author("Bob Dule", "06/09/2002", "BSc. Computer Engineering")
        # coauthors.append(coauthor)
        publication = Publication(title='The Biology of Life',url='www.comsci.com',publisher='CSpublications',date='05/09/2010')
        assert (
            publication.title == 'The Biology of Life'
            and publication.url== 'www.comsci.com'
            and publication.publisher== 'CSpublications'
            and publication.date == datetime.strptime('05/09/2010', "%d/%m/%Y")
        )

    def test_publication_toJSON(self):
        # authors = []
        # coauthors = []
        # author = Author("Bob Moog", "05/08/2001", "BSc. Computer Science")
        # authors.append(author)
        # coauthor = Author("Bob Dule", "06/09/2002", "BSc. Computer Engineering")
        # coauthors.append(coauthor)
        publication = Publication(title='The Biology of Life',url='www.comsci.com',publisher='CSpublications',date='05/09/2010')
        publication_json = publication.toJSON()
        self.assertDictEqual(publication_json, {
            "id": None,
            "title": "The Biology of Life",
            "url": "www.comsci.com", 
            "publisher": "CSpublications", 
            "date": datetime.strptime('05/09/2010', "%d/%m/%Y"),
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):
    def test_authenticate(self):
        user = create_user("bob", "bobpass")
        assert authenticate("bob", "bobpass") != None

    def test_create_user(self):
        # user = create_user("bob", "bobpass")
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


class AuthorIntegrationTests(unittest.TestCase):
    def test_create_author(self):
        author = create_author("Bob", "Moog", "bob@gmail.com", "UWI", "BSc. Computer Science")
        # author = create_author("Bob Moog", "05/08/2001", "BSc. Computer Science")
        assert author.fname == "Bob" and author.lname == "Moog"

    def test_get_all_authors_json(self):
        author_json=get_all_authors_json()
        self.assertListEqual([{
            'id': 1,
            'fname': "Bob",
            'lname': "Moog",
            'email': "bob@gmail.com",
            'institution': "UWI",
            'qualifications': "BSc. Computer Science",
            }
            ], author_json)

class PublicationIntegrationTests(unittest.TestCase):
    def test_create_publication(self):
        # author = get_author(1)
        # authors = []
        # if author:
        #     authors.append(author)
        # else:
        #     authors.append(create_author("Bob Moog", "05/08/2001", "BSc. Computer Science"))
            
            
        # coauthors = []
        publication= create_publication("[['James','May'], ['Richard','Hammond'], ['Jeremy','Clarkson']]", title='The Biology of Life 2',url='www.comsci2.com',publisher='CSpublications',date='05/09/2010')
        assert publication.title=="The Biology of Life 2"


    def test_get_publication_json(self):
        publication_json = get_all_publications_json()
        self.assertListEqual([
            {
                "id": 1,
                "title": "The Biology of Life 2",
                "url": "www.comsci2.com", 
                "publisher": "CSpublications", 
                "date": datetime.strptime('05/09/2010', "%d/%m/%Y"),
                  
            }
        ], publication_json)