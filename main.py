import boto3
import json
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from utils import mask_data, convert_app_version
import datetime


app = FastAPI()


class Record(BaseModel):
    user_id: str
    device_type: str
    masked_ip: str
    masked_device_id: str
    locale: str
    app_version: str

# Function to read messages from an AWS SQS queue
def read_messages():
    try:
        aws_access_key_id = 'dummy_access_key'
        aws_secret_access_key = 'dummy_secret_key'
        aws_session_token = 'dummy_session_token'
        
        sqs = boto3.client('sqs', 
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token,
                        endpoint_url='http://localstack:4566', 
                        region_name='us-east-1')
        
        queue_url = 'http://localstack:4566/000000000000/login-queue'
        
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=30)
        messages = response.get('Messages', [])
        return [json.loads(msg['Body']) for msg in messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Function to write records to a PostgreSQL database
def write_to_postgres(records: List[Record]):
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres', 
            password='postgres', 
            host='postgres', 
            port='5432'
        )
        print("Connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        for record in records:
            masked_record = mask_data(record)
            masked_record['app_version'] = convert_app_version(masked_record['app_version'])
            masked_record['create_date'] = datetime.date.today()

            cursor.execute("""
                INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                masked_record['user_id'],
                masked_record['device_type'],
                masked_record['masked_ip'],
                masked_record['masked_device_id'],
                masked_record['locale'],
                masked_record['app_version'],
                masked_record['create_date']
            ))
        conn.commit()
    except Exception as e:
        conn.rollback()  
        raise Exception(f"Issue in writing record to PostgreSQL: {e}")
    finally:
        cursor.close()
        conn.close()    
        
# Function to handle root URL, returns a simple greeting message
@app.get("/")
def get_messages():
    return {"message":"Hello World!"}

# Function to handle reading messages from SQS and returning them via API
@app.get("/read-messages")
def get_messages():
    try:
        messages = read_messages()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to handle reading messages from SQS and writing them to PostgreSQL via API
@app.get("/write-messages")
def post_messages():
    try:
        messages = read_messages()
        write_to_postgres(messages)
        return {"detail": "Messages written to PostgreSQL successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
