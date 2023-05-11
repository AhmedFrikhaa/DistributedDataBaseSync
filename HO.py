import mysql.connector
import pika
import json, threading
from CustomJSONEncoderDecoder import CustomJSONDecoder


# Connect to the HO database
ho_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ho_sales"
)


# Define a function to handle incoming sales data

def handle_sales_data(ch, method, _, body):
    # print(body)
    # Parse the JSON message body
    print("consuming sales data")
    rowss = json.loads(body, cls=CustomJSONDecoder)
    bo_id = rowss[-1]
    rowss = rowss[:-1]
    print(rowss)
    print("bo_id", bo_id)
    for row in rowss:
        print(row)
        # Insert the sales data into the HO database
        cursor = ho_db.cursor()
        query = "INSERT INTO sales (product_name, price, quantity, sale_date, id_bo, product_id_from_bo ) VALUES ( %s,%s, %s, %s, %s, %s)"

        values = (row[1], row[2], row[3], row[4], bo_id, row[0])

        cursor.execute(query, values)

    ho_db.commit()
    cursor.close()

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('Received and processed sales data')


def run():

    # Connect to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange and queue names
    exchange_name = 'sales_exchange'
    queue_name = 'ho_sales_queue'
    routing_key = 'sales.ho'

    # Declare the exchange
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    # Declare the queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Bind the queue to the exchange with the routing key
    channel.queue_bind(exchange=exchange_name, queue=queue_name,
                       routing_key=routing_key)

    # Consume messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=handle_sales_data)

    # Start consuming
    print('Waiting for sales data from BO database')
    #channel.start_consuming()
    threading.Thread(target=channel.start_consuming, daemon=True).start()

