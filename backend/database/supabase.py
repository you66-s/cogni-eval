import os
from supabase import create_client, Client
from dotenv import load_dotenv

class SupabaseDB:
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        print("Supabase client initialized.")
        print("Supabase URL:", self.supabase_url)
        print("Supabase Key:", self.supabase_key)

    def insert_data(self, table_name: str, data: dict):
        try:
            if not self.client:
                raise ValueError("Supabase client is not initialized.")
            if not table_name or not data:
                raise ValueError("Table name and data must be provided.")
                
            response = self.client.table(table_name).insert(data).execute()
            print(f"Data inserted into {table_name} successfully.")
            return True
        except Exception as e:
            print(f"Error inserting data into {table_name}: {e}")
            return False