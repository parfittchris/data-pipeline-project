# Homes Data Pipeline


## Background and Overview
 This application converts data from JSON, CSV, and XML files into instances of Agents, Offices, and Listings and inserts them into a local SQLite3 database.

## Functionality
  * Import method will convert all files in chosen directory into useable data format
  * Worker Queue receives data packet output and stores the information for later retrieval
  * Database file selectively takes packets from worker queue and inserts each into it's correct database table: Agent, Listing, or Office.
  * App file runs the application and selection of file directory through the terminal
  * The only modifications to the data are converting phone numbers into the same format via the translateNum method


## Install Instructions
  Requirements: Python3 and Pipenv
   
  1) Navigate to chosen directory to store application
  
  2) In terminal, type the following commands:
      * git clone https://github.com/parfittchris/data-pipeline-project.git
      * pipenv shell
      * pipenv install
      * python3 app.py

  3) At this point the application will start up in and ask you to select your file directory. (Default location of files for this project is ./static)
  
  
## Code Examples

### File Finder
Submitting a folder directory runs a recursive python algorithm that locates each individual file in all nested directories in that folder.

 
 ```
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
  ```

### Adding Item to DB
Data packets inserted and retrieved from worker queue contain all the data from a single imported file. Each packet has one or multiple items with an attribute indicating it's type. The type determines which insertion method is run like the following for 'agent':


```
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
```

### Potential Future Work
  * Create GUI for easier navigation and locating of file directories


