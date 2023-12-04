import sqlite3
import requests
from bs4 import BeautifulSoup as bs

class DatabaseObject:
    def __init__(self, db_name="sites.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sites
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                url TEXT,
                                content TEXT)''')
        self.connection.commit()

    def add_site(self, url, content):
        self.cursor.execute("INSERT INTO sites (url, content) VALUES (?, ?)", (url, content))
        self.connection.commit()

    def clear_database(self):
        self.cursor.execute("DELETE FROM sites")
        self.connection.commit()

    def get_sites(self):
        self.cursor.execute("SELECT * FROM sites")
        return self.cursor.fetchall()

class ParserObject:
    def parse_website(self, url):
        response = requests.get(url)
        return response.text

class UserInterfaceObject:
    def get_user_input(self):
        return input("Enter a website URL: ")

    def display_results(self, results):
        for result in results:
            print(result)

def run():
    database = DatabaseObject()
    parser = ParserObject()
    user_interface = UserInterfaceObject()

    database.create_table()

    while True:
        user_input = user_interface.get_user_input()

        if user_input.lower() == "exit":
            break

        content = parser.parse_website(user_input)
        database.add_site(user_input, content)

    results = database.get_sites()
    user_interface.display_results(results)

if __name__ == "__main__":
    run()
