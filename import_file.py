import csv
import json
import xml.etree.ElementTree as ET

def parse_data(location):
    packet = []
    
    with open(location, 'r') as input_file:
        if location.endswith('.json'):
            data = json.load(input_file)

            for item in data:
                new_listing = {}
                new_agent = {}
                new_office = {}

                new_listing['data_type'] = 'listings'
                new_listing['address'] = str(item['street_address'])
                new_listing['city'] = str(item['city'])
                new_listing['state'] = str(item['state'])
                new_listing['zip'] = str(item['zip'])
                new_listing['mls_number'] = str(item['mls_number'])
                new_listing['price'] = str(item['price'])
                new_listing['status'] = str(item['status'])
                new_listing['type'] = str(item['type'])
                new_listing['description'] = str(item['description'])
                new_listing['agent_id'] = item['agent_code']
                new_listing['office_id'] = item['office_code']

                new_agent['data_type'] = 'agents'
                new_agent['name'] = str(item['agent_name'])
                new_agent['agent_code'] = str(item['agent_code'])
                new_agent['phone'] = str(item['office_phone'])
                new_agent['city'] = str(item['city'])
                new_agent['state'] = str(item['state'])
                new_agent['zip'] = str(item['zip'])

                new_office['data_type'] = 'offices'
                new_office['name'] = str(item['office_name'])
                new_office['office_code'] = str(item['office_code'])
                new_office['phone'] = str(item['office_phone'])
                new_office['city'] = str(item['city'])
                new_office['state'] = str(item['state'])
                new_office['zip'] = str(item['zip'])

                packet.append(new_listing)
                packet.append(new_agent)
                packet.append(new_office)


        elif location.endswith('.csv'):
            reader = csv.reader(input_file)
            
            if 'office' in location:
                for name, office_code, phone, city, state, zip_code in reader:
                    new_item = {}

                    new_item['data_type'] = 'offices'
                    new_item['name'] = str(name)
                    new_item['office_code'] = str(office_code)
                    new_item['phone'] = str(phone)
                    new_item['city'] = str(city)
                    new_item['state'] = str(state)
                    new_item['zip'] = str(zip_code)

                    packet.append(new_item)

            elif 'agent' in location:
                for name, agent_code, office_code, phone, city, state, zip_code in reader:
                    new_item = {}

                    new_item['data_type'] = 'agents'
                    new_item['name'] = str(name)
                    new_item['agent_code'] = str(agent_code)
                    new_item['phone'] = str(phone)
                    new_item['city'] = str(city)
                    new_item['state'] = str(state)
                    new_item['zip'] = str(zip_code)

                    packet.append(new_item)

            else:
                for mls, address, city, state, zip_code, price, status, listing_type, agent_code, office_code, desc in reader:
                    new_item = {}
       
                    new_item['data_type'] = 'listings'
                    new_item['address'] = str(address)
                    new_item['city'] = str(city)
                    new_item['state'] = str(state)
                    new_item['zip'] = str(zip_code)
                    new_item['mls_number'] = str(mls)
                    new_item['price'] = str(price)
                    new_item['status'] = str(status)
                    new_item['type'] = str(listing_type)
                    new_item['description'] = str(desc)
                    new_item['agent_id'] = agent_code
                    new_item['office_id'] = office_code

                    packet.append(new_item)

        elif location.endswith('.xml'):
            tree = ET.parse(input_file)
            root = tree.getroot()
            
            for listing in root.iter('listing'):
                new_listing = {}
                new_agent = {}
                new_office = {}
                
                broker = listing[3]
                agent = listing[4]
                address = listing[5]

                new_listing['data_type'] = 'listings'
                new_listing['address'] = str(address[2].text)
                new_listing['city'] = str(address[1].text)
                new_listing['state'] = str(address[3].text)
                new_listing['zip'] = str(address[0].text)
                new_listing['mls_number'] = str(listing[6].text)
                new_listing['price'] = str(listing[0].text)
                new_listing['status'] = str(listing[2].text)
                new_listing['type'] = str(listing[7].text)
                new_listing['description'] = str(listing[1].text)
                new_listing['agent_id'] = str(agent[0].text)
                new_listing['office_id'] = str(broker[0].text)

                new_agent['data_type'] = 'agents'
                new_agent['name'] = str(agent[2])
                new_agent['agent_code'] = str(agent[0])
                new_agent['phone'] = str(agent[1])
                new_agent['city'] = str(address[1].text)
                new_agent['state'] = str(address[3].text)
                new_agent['zip'] = str(address[0].text)

                new_office['data_type'] = 'offices'
                new_office['name'] = str(broker[2])
                new_office['office_code'] = str(broker[0])
                new_office['phone'] = str(broker[1])
                new_office['city'] = str(address[1].text)
                new_office['state'] = str(address[3].text)
                new_office['zip'] = str(address[0].text)

                packet.append(new_listing)
                packet.append(new_agent)
                packet.append(new_office)


    return packet


