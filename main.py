import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('sites.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS sites (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL)''')

def add_site():
    url = input('Enter the URL of the website you want to add: ')
    c.execute('''INSERT INTO sites (url) VALUES (?)''',(url, ))
    conn.commit()
    print('The website has been added successfully.')

def remove_site():
    url = input('Enter the URL of the website you want to remove: ')
    c.execute('''DELETE FROM sites WHERE url=?''', (url, ))
    conn.commit()
    print('The website has been removed successfully.')

def clear_database():
    c.execute('''DELETE FROM sites''')
    conn.commit()
    print('The database has been cleared successfully.')

def search_website(url, query):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    count = soup.text.count(query)
    return count

def search_websites(query):
    results = []
    c.execute('''SELECT * FROM sites''')
    rows = c.fetchall()
    for row in rows:
        url = row[1]
        count = search_website(url, query)
        results.append((url, count))
        results.sort(key=lambda x: x[1], reverse=True)

    print('Search results: ')
    for result in results:
        print(result[0], "-", result[1])

while True:
    print("What would you like to do?")
    print("1. Add a website to the database")
    print("2. Remove a website from the database")
    print("3. Clear the database")
    print("4. Search for information on websites")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        add_site()
    elif choice == "2":
        remove_site()
    elif choice == "3":
        clear_database()
    elif choice == "4":
        query = input("Enter the information you want to search for: ")
        search_websites(query)
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")

conn.close()