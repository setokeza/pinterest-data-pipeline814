import datetime
import json
import requests
import random
import sqlalchemy 
from time import sleep
import yaml

class AWSDBConnector:
    def __init__(self):
        self.creds = {}
    
    def read_db_creds(self):
        """
        Returns the database credentials from the yaml file
        """
        with open('db_creds.yaml') as yaml_file:
            self.creds = yaml.safe_load(yaml_file)
        return self.creds
       
    def create_db_connector(self):
        """
        Using the database credentials, creates a database engine to connect to the database
        """
        self.creds = self.read_db_creds()
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.creds['USER']}:{self.creds['PASSWORD']}@{self.creds['HOST']}:{self.creds['PORT']}/{self.creds['DATABASE']}?charset=utf8mb4")
        return engine

def datetime_converter(date_time):
    """
    Converts datetime to string

    Paramenter: 
    date_time : datetime
    """
    if isinstance(date_time, datetime.datetime):
        return date_time.__str__()

def run_infinite_post_data_loop():
    """
    Creates a connection to the database to emulate row data that is generated randomly into AWS S3
    """
    i=1
    while i == 1:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()
        headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}

        with engine.connect() as connection:
            tablenames_topics = {'pinterest_data':'0ecf5ea19ac5.pin', 'geolocation_data':'0ecf5ea19ac5.geo', 'user_data':'0ecf5ea19ac5.user'}
            for table_name, topic in tablenames_topics.items():
                sql_string = sqlalchemy.text(f"SELECT * FROM {table_name} LIMIT {random_row}, 1")
                selected_row = connection.execute(sql_string)
                invoke_url = f"https://g7wixjqbxa.execute-api.us-east-1.amazonaws.com/0ecf5ea19ac5-test/topics/{topic}"
                for row in selected_row:
                    result = dict(row._mapping)
                    payload = json.dumps({"records": [{ "value": result}]},default=datetime_converter)
                    print(payload)
                    response = requests.request("POST", invoke_url, headers=headers, data=payload)
                    if response.status_code == 200:
                        print(f'Successfully sent data to Kafka topic {topic}')
                    else:
                        print(f'Failed to send data to Kafka topic {topic}')
                        print(f'Response: {response.status_code}, {response.text}')

            
        i += 1


if __name__ == "__main__":
    new_connector = AWSDBConnector()
    run_infinite_post_data_loop()