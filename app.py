from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import time
import os

import import_file
from worker import WorkerQueue


#  Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'homes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Automap SQLAlchemy to existing homes.db
Base = automap_base()
Base.prepare(db.engine, reflect=True)

Agents = Base.classes.agents
Listings = Base.classes.listings
Offices = Base.classes.offices

# Methods to populate db
def addAgent(agent):

        # Verify Agent doesn't already exist in db
        current = db.session.query(Agents).filter(Agents.agent_code == agent['agent_code']).first()

        if current:
            current.name = agent['name']
            current.agent_code = agent['agent_code']
            current.phone = agent['phone']
            current.city = agent['city']
            current.state = agent['state']
            current.zip = agent['zip']
        else:
            new_agent = Agents(name= agent['name'], agent_code= agent['agent_code'], phone=agent['phone'], city=agent['city'], state=agent['state'], zip=agent['zip'])
            db.session.add(new_agent)

        db.session.commit()
        return 


def addListing(listing):

        # Verify Listing doesn't already exist in db
        current = db.session.query(Listings).filter(Listings.mls_number == listing['mls_number']).first()

        if current:
            current.address = listing['address']
            current.city = listing['city']
            current.state = listing['state']
            current.zip = listing['zip']
            current.mls_number = listing['mls_number']
            current.price = listing['price']
            current.status = listing['status']
            current.type = listing['type']
            current.description = listing['description']
            current.agent_id = str(listing['agent_id'])
            current.office_id = str(listing['office_id'])
        else:
            new_listing = Listings(address=listing['address'], city=listing['city'], state=listing['state'], zip=listing['zip'], mls_number=listing['mls_number'], price=listing['price'], status=listing['status'], type=listing['type'], description=listing['description'], agent_id= listing['agent_id'], office_id=listing['office_id'])
            db.session.add(new_listing)

        db.session.commit()
        return


def addOffice(office):

        # Verify Office doesn't already exist in db
        current = db.session.query(Offices).filter(Offices.office_code == office['office_code']).first()

        if current:
            current.name = office['name']
            current.office_code = office['office_code']
            current.phone = office['phone']
            current.city = office['city']
            current.state = office['state']
            current.zip = office['zip']
        else:
            new_office = Offices(name=office['name'], office_code=office['office_code'], phone=office['phone'], city=office['city'], state=office['state'], zip=office['zip'])
            db.session.add(new_office)

        db.session.commit()
        return


def enterData(current_queue):
    results = current_queue.remove()

    for item in results:
        if item['data_type'] == 'agents':
            addAgent(item)
        elif item['data_type'] == 'listings':
            addListing(item)
        elif item['data_type'] == 'offices':
            addOffice(item)
    
    return



def getFiles(directory):
    files = []

    def traverse(current_dir):
        current_files = os.listdir(current_dir)
        
        for filename in current_files:
            path = current_dir + '/' + filename
            if os.path.isfile(path):
                files.append(path)
            elif os.path.isdir(path):
                traverse(path)
            
        return

    traverse(directory)
    return files


# Clear db method for testing
def clearDB():
    db.session.query(Agents).delete()
    db.session.query(Listings).delete()
    db.session.query(Offices).delete()
    db.session.commit()
    return ''


def startApp():
    queue = WorkerQueue()

    while True:
        try:
            source = input('\nEnter file directory: ')
            results = getFiles(source)
            
            for item in results:
                queue.insert(item)
            
            print('Directory found.')
            time.sleep(1)
            break
                
        except FileNotFoundError:
            print('File not found. Try again')
            time.sleep(1)
    

    while queue.length > 0:
        enterData(queue)
        print('Enterting data...')
        # time.sleep(2)
    
    print('Successful Import')


startApp()
# clearDB()
