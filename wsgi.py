import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
import contextlib
from sqlalchemy import MetaData

from App.database import create_db, get_migrate, clear, db
from App.main import create_app

from App.controllers import ( create_user, get_all_users_json, get_all_users )
from App.controllers import ( create_author, get_all_authors_json, get_all_authors, get_author, get_author_by_name )
# from App.controllers import ( get_all_items_json )
from App.controllers import ( create_publication, get_all_publications_json )
from App.controllers import *
from App.models import *
from datetime import date

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
# migrate = get_migrate(app)
# sys.argv[1] = [['richard','hammond'],['James', 'May'],['Jeremy', 'Clarkson']]
# # print(sys.argv[1])

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    # meta = MetaData()
    # with contextlib.closing(engine.connect()) as con:
    #     trans = con.begin()
    #     for table in reversed(meta.sorted_tables):
    #         con.execute(table.delete())
    #     trans.commit()
    db.drop_all()
    create_db(app)
    db.session.commit()
    a1 = Author(fname='Angela', lname='Broski', email='angelabski@gmail.com', institution='UWI', qualifications='MSc. Biology')
    a2 = Author(fname='Jeff', lname='Weenie', email='jweenie3@gmail.com', institution='UWI', qualifications='MSc. Computer Science')
    a3 = Author(fname='Carla', lname='Marla', email='cm07@gmail.com', institution='UWI', qualifications='MSc.Party')
    a4 = Author(fname='Sana', lname='Marsh', email='samarsh@hotmail.com', institution='UWI', qualifications='MSc. Apples')
    a5 = Author(fname='Fredrick', lname='Street', email='fredstreet@outlook.com', institution='UWI', qualifications='MSc. Painting')
    a6 = Author(fname='Phil', lname='Mill', email='phmill@hotmail.com', institution='UWI', qualifications='MSc. Biochemical Engineering')
    a7 = Author(fname='Afrika', lname='Toto', email='totoafrika22@gmail.com', institution='UWI', qualifications='MSc. Music')
    db.session.add_all([a1, a2, a3, a4, a5, a6, a7])
    db.session.commit()

    p1 = create_publication("[['Angela','Broski'], ['Fredrick','Street'], ['Sana','Marsh']]", title='The Biology of Life',url='www.comsci.com',publisher='CSpublications',date='05/09/2010')
    p2 = create_publication("[['Sana','Marsh'],['Jeff','Weenie'], ['Fredrick','Street']]", title='Different Types of Ferns',url='www.biology.com',publisher='Biopublications',date='10/05/2008')
    p3 = create_publication("[['Phil','Mill'],['Angela','Broski'], ['Sana','Marsh']]", title='Exploring the Universe',url='www.spacelovers.com',publisher='Spacepublications',date='13/08/2007')
    p4 = create_publication("[['Fredrick','Street'],['Afrika','Toto'], ['Sana','Marsh']]", title='Computers and Networks',url='www.comscii.com',publisher='CSpublications',date='04/10/2004')
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit

    print('database intialized with some data')

# |       ID      |       PublicationTitle                |       AuthorId        |       PublicationId   |       Position        |
# |       1       |       The Biology of Life             |       1               |       1               |       0               |
# |       2       |       The Biology of Life             |       5               |       1               |       1               |
# |       3       |       The Biology of Life             |       2               |       1               |       2               |
# |       4       |       Different Types of Ferns        |       4               |       2               |       0               |
# |       5       |       Different Types of Ferns        |       1               |       2               |       1               |
# |       6       |       Different Types of Ferns        |       5               |       2               |       2               |
# |       7       |       Exploring the Universe          |       6               |       3               |       0               |
# |       8       |       Exploring the Universe          |       1               |       3               |       1               |
# |       9       |       Exploring the Universe          |       4               |       3               |       2               |
# |       10      |       Computers and Networks          |       5               |       4               |       0               |
# |       11      |       Computers and Networks          |       2               |       4               |       1               |
# |       12      |       Computers and Networks          |       4               |       4               |       2               |

# @app.cli.command("drop", help="Creates and initializes the database")
# def initialize():
#     create_db(app)
#     print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Generic Commands
'''

# @app.cli.command("init")
# def initialize():
#     create_db(app)
#     print('database intialized')

@app.cli.command("pubData")
def printFeed():
    pubauts = AuthorPublication.query.all()
    print('|\tID\t|\tPublicationTitle\t\t|\tAuthorId\t|\tPublicationId\t|\tPosition\t|')
    for pubaut in pubauts:
        print('|\t' + str(pubaut.id) + '\t|\t' + pubaut.publicationTitle + '\t|\t' + str(pubaut.authorId )+ '\t\t|\t' + str(pubaut.publicationId) + '\t\t|\t' + str(pubaut.authorPosition )+ '\t\t|')

@app.cli.command("pubTree")
def printTree():
    print (Author.query.all())
    authorId = input("Enter Id: ")
    pub_tree_search(authorId)
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))

@test.command("author", help="Run Author tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AuthorUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "AuthorIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Author"]))

@test.command("publication", help="Run Publication tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "PublicationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "PublicationIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Publication"]))
    

app.cli.add_command(test)

# authors
author_cli = AppGroup('author', help='author object commands') 

@author_cli.command("create", help="Creates an author")
@click.argument("fname", default="Richard")
@click.argument("lname", default="Hammond")
@click.argument("email", default="hamm@email.com")
@click.argument("institution", default="UWI")
@click.argument("qualifications", default="BSc. Science")
def create_author_command(fname, lname, email, institution, qualifications):
    create_author(fname, lname, email, institution, qualifications)
    print(f'{fname} created!')

# # @click.argument("dob", default="05/08/2001")
# @click.option("--dob", "-d")
# # @click.argument("qualifications", default="BSc. Science")
# @click.option("--qualifications", "-q")

@author_cli.command("listby")

def list_authors():
    authors = get_all_authors_json()
    print(authors)

@author_cli.command("list")
def list_authors():
    authors = get_all_authors_json()
    print(authors)

app.cli.add_command(author_cli)

# publications
publication_cli = AppGroup('pub', help='pub object commands') 

@publication_cli.command("create", help="Creates a publication")
# @click.option("--author_ids", "-a", multiple=True)

# @click.option("--coauthor_ids", "-ca", multiple=True)
@click.argument("authors", default= "[['James','May'],['James', 'May'],['Jeremy', 'Clarkson']]")
@click.argument("title", default="Computer Science 1st Edition")
@click.argument("url", default="www.comsci.com")
@click.argument("publisher", default="CSpublications")
@click.argument("date", default="05/08/2001")
def create_publication_command(authors, title, url, publisher, date):

    create_publication(authors, title, url, publisher, date)
    print(f'{title} created!')

@publication_cli.command("list")
def list_publications():
    publications = get_all_publications_json()
    print(publications)

# @publication_cli.command("create_names")
# @click.option("--author_names", "-A", multiple=True)
# @click.option("--coauthor_names", "-CA", multiple=True)
# @click.argument("title", default="Computer Science 1st Edition")
# def create_publication_command(title, author_names, coauthor_names):
#     authors = sum ( [get_author_by_name(name) for name in author_names], [] )
#     print(authors)
#     coauthors = sum ( [get_author_by_name(name) for name in coauthor_names], [] )
#     print(coauthors)
#     # a = get_author(author_ids)
#     create_publication(title, authors, coauthors)
#     print(f'{title} created!')


app.cli.add_command(publication_cli)


