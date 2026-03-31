import psycopg                                                                                                        
from time import time
from dotenv import load_dotenv
import os

load_dotenv()

db_params = {
    "host": os.getenv("DB_HOST", "localhost"),
    "dbname": os.getenv("DB_NAME", "marvo"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}
async def create_connection():
    conn = await psycopg.AsyncConnection.connect(**db_params)
    return conn                                                                                                       
  
async def create_table(conn):                                                                                         
    async with conn.cursor() as cursor:                                                                             
        await cursor.execute("CREATE TABLE IF NOT EXISTS tickets (channel_id BIGINT PRIMARY KEY, user_id BIGINT, last_message BIGINT)")                                                                                                
        await conn.commit()
                                                                                                                        
async def create_ticket(conn, channel_id, user_id):                                                                 
    async with conn.cursor() as cursor:
        await cursor.execute("INSERT INTO tickets (channel_id, user_id, last_message) VALUES (%s, %s, %s)",(channel_id, user_id, int(time())))
        print(f"Ticket created: {channel_id}")
        await conn.commit()                                                                                           
                                                                                                                      
async def delete_ticket(conn, channel_id):                                                                            
    async with conn.cursor() as cursor:
        await cursor.execute("DELETE FROM tickets WHERE channel_id = %s", (channel_id,))  
        print(f"Ticket deleted: {channel_id}")                            
        await conn.commit()                                                                                         

async def get_ticket(conn, channel_id):                                                                               
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM tickets WHERE channel_id = %s", (channel_id,))                            
        return await cursor.fetchone()       

async def get_user_tickets(conn, user_id):
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM tickets WHERE user_id = %s", (user_id,))
        return await cursor.fetchall()

async def update_last_message(conn, channel_id):
    async with conn.cursor() as cursor:
        await cursor.execute("UPDATE tickets SET last_message = %s WHERE channel_id = %s", (int(time()), channel_id))
        await conn.commit()

async def get_inactive_tickets(conn, threshold):
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM tickets WHERE last_message < %s", (threshold,))
        return await cursor.fetchall()