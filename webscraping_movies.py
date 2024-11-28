import requests
from bs4 import BeautifulSoup
import csv
import sqlite3

def scrape_top_50_movies(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')[1:51]  # Skip the header row and get top 50 rows

    movies = []
    for row in rows:
        cols = row.find_all('td')
        rank = cols[0].text.strip()
        film = cols[1].text.strip()
        year = cols[2].text.strip()
        movies.append((rank, film, year))

    return movies

def save_to_csv(movies, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Average Rank', 'Film', 'Year'])
        writer.writerows(movies)

def save_to_database(movies, db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Top_50 (
            Average_Rank TEXT,
            Film TEXT,
            Year TEXT
        )
    ''')
    cursor.executemany('INSERT INTO Top_50 (Average_Rank, Film, Year) VALUES (?, ?, ?)', movies)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
    movies = scrape_top_50_movies(url)
    save_to_csv(movies, 'top_50_films.csv')
    save_to_database(movies, 'Movies.db')
