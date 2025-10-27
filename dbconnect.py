#!/usr/bin/env python3

import oracledb
import os
import sys
from typing import Optional

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.pool = None
        
    @staticmethod
    def find_instant_client():
        """
        Attempt to locate Oracle Instant Client directory
        """
        possible_paths = [r"C:\Oracle\instantclient-basic-windows.x64-23.9.0.25.07\instantclient_23_9"]
  
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
        
    def init_oracle_client(self, wallet_location: str) -> None:
        """
        Initialize the Oracle Client with wallet configuration.
        
        Args:
            wallet_location (str): Path to the wallet directory
        """
        try:
            # Try to find Oracle Instant Client
            instant_client_path = self.find_instant_client()
            if not instant_client_path:
                raise Exception("Oracle Instant Client not found. Please install it and add to PATH")
            
            # Add Instant Client to PATH if not already there
            if instant_client_path not in os.environ['PATH']:
                os.environ['PATH'] = instant_client_path + os.pathsep + os.environ['PATH']
            
            # Initialize in Thick mode with instant client
            oracledb.init_oracle_client(
                lib_dir=instant_client_path,
                config_dir=wallet_location
            )
        except Exception as e:
            print(f"Error initializing Oracle Client: {e}")
            print("\nPlease ensure Oracle Instant Client is installed:")
            print("1. Download from: https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html")
            print("2. Extract to C:\\oracle\\instantclient")
            print("3. Add the path to your system's PATH environment variable")
            raise
    
    def connect(self, username: str, password: str, dsn: str, wallet_location: str = None) -> bool:
        """
        Establishes a connection to the Oracle Autonomous Database.
        
        Args:
            username (str): Database username
            password (str): Database password
            dsn (str): TNS name from tnsnames.ora
            wallet_location (str): Path to the wallet directory (optional if already initialized)
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            if wallet_location:
                self.init_oracle_client(wallet_location)
            
            # Enable TLS for autonomous database connection
            connection_params = {
                "user": username,
                "password": password,
                "dsn": dsn,
                "config_dir": wallet_location
            }
            
            self.connection = oracledb.connect(**connection_params)
            return True
        except oracledb.Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self) -> None:
        """Closes the database connection if it exists."""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except oracledb.Error as e:
                print(f"Error disconnecting from database: {e}")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> list:
        """
        Executes a SQL query and returns the results.
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            
        Returns:
            list: Query results
        """
        if not self.connection:
            raise Exception("Not connected to database")
            
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            cursor.close()
            return results
        except oracledb.Error as e:
            print(f"Error executing query: {e}")
            return []

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# Example usage:
if __name__ == "__main__":
    # Replace these with actual values
    DB_USER = os.getenv("DB_USER", "")
    DB_PASS = os.getenv("DB_PASS", "")
    DB_DSN = os.getenv("DB_DSN", "")  # TNS name from tnsnames.ora
    WALLET_LOCATION = os.getenv("WALLET_LOCATION", "")  # Path to wallet directory
    
    
    db = DatabaseConnection()
    if db.connect(DB_USER, DB_PASS, DB_DSN, WALLET_LOCATION):
        try:                       
            # Example query
            results = db.execute_query("SELECT 'You are connected as user: '||user|| ' on '|| CURRENT_DATE FROM dual")
            print(f"Test query result: {results}")
        finally:
            db.disconnect()