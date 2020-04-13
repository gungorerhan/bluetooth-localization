import sys
import logging
import rds_config
import pymysql
import json

#rds settings
rds_host  = "ips-1.c6mdsdjlgnmm.eu-central-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def handler(event, context):
    # Parse event body
    eventBody = event["body"]
    eventBody = json.loads(eventBody)
    personId = eventBody["personId"]
    firstName = eventBody["firstName"]
    lastName = eventBody["lastName"]
    cardId = eventBody["cardId"]

    # Construct thae body of the response object
    responseBody = {}
    responseBody['status'] = f'New person added with id={personId}'
    
    with conn.cursor() as cur:
        values = f'("{personId}", "{firstName}", "{lastName}", "{cardId}")'
        cur.execute("INSERT INTO Person (personId, firstName, lastName, cardId) VALUES" + values + ";")
        logger.info(f'New person added with id={personId}')


    conn.commit()


    # Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(responseBody)

    # Return the response object
    return responseObject