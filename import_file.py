import csv
import json
import xml.etree.ElementTree as ET


def parse_data(location, data_type):
    packet = []
    
    try:
        with open(location, 'r') as input_file:
            if location.endswith('.json'):
                data = json.load(input_file)

                for item in data:
                    new_item = {}

                    new_item['data_type'] = 'agents'
                    new_item['name'] = item['agent_name']
                    new_item['agent_code'] = item['agent_code']
                    new_item['phone'] = item['office_phone']
                    new_item['city'] = item['city']
                    new_item['state'] = item['state']
                    new_item['zip'] = item['zip']

                    packet.append(new_item)


            elif location.endswith('.csv'):
                reader = csv.reader(input_file)

                if data_type == 'agents':
                    for name, agent_code, office_code, phone, city, state, zip_code in reader:
                        new_item = {}

                        new_item['data_type'] = 'agents'
                        new_item['name'] = name
                        new_item['agent_code'] = agent_code
                        new_item['phone'] = phone
                        new_item['city'] = city
                        new_item['state'] = state
                        new_item['zip'] = zip_code

                        packet.append(new_item) 

                elif data_type == 'listings':
                    for mls, address, city, state, zip_code, price, status, listing_type, agent_code, office_code, desc in reader:
                        new_item = {}

                        new_item['data_type'] = 'listings'
                        new_item['address'] = address
                        new_item['city'] = city
                        new_item['state'] = state
                        new_item['zip'] = zip_code
                        new_item['mls_number'] = mls
                        new_item['price'] = price
                        new_item['status'] = status
                        new_item['type'] = listing_type
                        new_item['description'] = desc
                        new_item['agent_id'] = agent_code
                        new_item['office_id'] = office_code

                        packet.append(new_item)

                elif data_type == 'offices':
                    for name, office_code, phone, city, state, zip_code in reader:
                        new_item = {}

                        new_item['data_type'] = 'offices'
                        new_item['name'] = name
                        new_item['office_code'] = office_code
                        new_item['phone'] = phone
                        new_item['city'] = city
                        new_item['state'] = state
                        new_item['zip'] = zip_code

                        packet.append(new_item)

            elif location.endswith('.xml'):
                tree = ET.parse(input_file)
                root = tree.getroot()
                
                for listing in root.iter('listing'):
                    new_item = {}
                    
                    broker = listing[3]
                    agent = listing[4]
                    address = listing[5]

                    new_item['data_type'] = 'listings'
                    new_item['address'] = address[2].text
                    new_item['city'] = address[1].text
                    new_item['state'] = address[3].text
                    new_item['zip'] = address[0].text
                    new_item['mls_number'] = listing[6].text
                    new_item['price'] = listing[0].text
                    new_item['status'] = listing[2].text
                    new_item['type'] = listing[7].text
                    new_item['description'] = listing[1].text
                    new_item['agent_id'] = agent[0].text
                    new_item['office_id'] = broker[0].text

                    packet.append(new_item)

        return packet

    except FileNotFoundError:
        print("Cannot find file")
        return None



