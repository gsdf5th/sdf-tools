__author__ = 'kwhatcher'
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
import boto
import boto.s3.connection

conn = boto.connect_s3(
        calling_format = boto.s3.connection.OrdinaryCallingFormat()
        )

bucket = conn.get_bucket('gsdf')

def getallmissions():
    missions = []
    conn = DynamoDBConnection()
    tables = conn.list_tables()
    table = Table('missions', connection=conn)
    results = conn.scan('missions')
    for result in results['Items']:
        print result
    return results['Items']


def getmissionurl(SAD_ID):
    plans_key = bucket.get_key(str(SAD_ID['S']) + ".pdf")
    plans_url = plans_key.generate_url(3600, query_auth=True)
    return plans_url
