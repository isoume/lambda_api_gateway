import pymysql
import json
import os

def get_config():
    return {
        "DB_HOST": "",
        "DB_USER": "",
        "DB_PASSWORD": "",
        "DB_NAME": ""
    }

def get_db_connection():
    config = get_config()
    return pymysql.connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        connect_timeout=5
    )

def lambda_handler(event, context):

    # The body of the requests
    body = json.loads(event.get('body', '{}'))
    # The Path parameters
    path_params = event.get('pathParameters') or {}

    path = event.get('path', '')
    # The method Of the request
    method = event.get('httpMethod', '')
    # Si la method que j'ai recu et le path c ....
    if method == 'GET' and path == '/transactions':
        connection = get_db_connection()
        transactions = get_transactions(connection)
        return {
            "statusCode": 200,
            "body": transactions
        }

    return {
        "statusCode": 200,
        "body": "Hello Je suis tranquille en attendant que tu me reveilles"
    }



def get_data(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def get_transactions(connection):
    query = "SELECT id, montant, type, date, description FROM transactions"
    rows = get_data(connection, query)
    transactions = [
        {
            "id": row[0],
            "montant": float(row[1]),
            "type": row[2],
            "date": row[3].isoformat(),
            "description": row[4]
        } for row in rows
    ]
    return transactions