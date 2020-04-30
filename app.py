from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import os

import import_file
from worker import WorkerQueue

#  Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
queue = WorkerQueue()

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
# CHECK IF ITEM ALREADY EXISTS IN DB

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
            current.agent_id = listing['agent_id']
            current.office_id = listing['office_id']
        else:
            new_listing = Listings(address=listing['address'], city=listing['city'], state=listing['state'], zip=listing['zip'], mls_number=listing['mls_number'], price=listing['price'], status=listing['status'], type=listing['type'], description=listing['description'], agent_id=listing['agent_id'], office_id=listing['office_id'])
            db.session.add(new_listing)

        db.session.commit()
        return


def addOffice(office):

        # Verify Listing doesn't already exist in db
        current = db.session.query(Offices).filter(Offices.office_code == office['office_code']).first()

        if current:
            current.name = listing['name']
            current.office_code = listing['office_code']
            current.phone = listing['phone']
            current.city = listing['city']
            current.state = listing['state']
            current.zip = listing['zip']
        else:
            new_office = Offices(name=office['name'], office_code=office['office_code'], phone=office['phone'], city=office['city'], state=office['state'], zip=office['zip'])
            db.session.add(new_office)

        db.session.commit()
        return

# Routes
@app.route('/deleteAll', methods=['GET'])
def index():
    db.session.query(Agents).delete()
    db.session.query(Listings).delete()
    db.session.query(Offices).delete()
    db.session.commit()
    return ''


test_agent = {
        'type': 'agents',
        'name': 'Batman',
        'agent_code': '777',
        'phone': '12345678',
        'city': 'Burlington',
        'state': 'Vermont',
        'zip': '05456'
    }

test_office = {
        'type': 'offices',
        'name': 'The end of the world Office',
        'office_code': '123',
        'phone': '12345678',
        'city': 'Burlington',
        'state': 'Vermont',
        'zip': '05456'
}

test_listing = {
        'type': 'listings',
        'address': '123 Main Steet',
        'city': 'Harvard',
        'state': 'Vermont',
        'zip': '05456',
        'mls_number': '777',
        'price': '234324',
        'status': 'for rent',
        'description': 'It\'s great!',
        'agent_id': 123432,
        'office_id': 37492
}

# addAgent(test_agent)
# addListing(test_listing)
addOffice(test_office)


# Run Server
# if __name__ == '__main__':
#     app.run(debug=True)
