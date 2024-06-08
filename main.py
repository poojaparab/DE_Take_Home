import boto3
import json
import psycopg2
from utils import mask_data, convert_app_version
import datetime

def read_messages():
    aws_access_key_id = 'dummy_access_key'
    aws_secret_access_key = 'dummy_secret_key'
    aws_session_token = 'dummy_session_token'
    
    sqs = boto3.client('sqs', 
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token,
                        endpoint_url='http://localhost:4566', 
                        region_name='us-east-1')
    
    queue_url = 'http://localhost:4566/000000000000/login-queue'
    
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=12)
    messages = response.get('Messages', [])
    return [json.loads(msg['Body']) for msg in messages]

def write_to_postgres(records):

    
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres', 
            password='postgres', 
            host='localhost', 
            port='5432'
        )
        print("Connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")
    cursor = conn.cursor()
    for record in records:
        masked_record = mask_data(record)
        masked_record['app_version']=convert_app_version(masked_record['app_version'])
        masked_record['create_date'] = datetime.date.today()

        cursor.execute("""
            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version,create_date)
            VALUES (%s, %s, %s, %s, %s, %s,%s)
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
    cursor.close()
    conn.close()



if __name__ == "__main__":
    messages = read_messages()
    write_to_postgres(messages)



