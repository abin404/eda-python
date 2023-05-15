import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt
from helpers import check_if_element_is_available

# Step 1: Web Scraping IMDb
url = 'https://www.imdb.com/chart/top'
response = requests.get(url)
html_content = response.content

# Step 2: Parsing HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Step 3: Extracting relevant data
movies = soup.select('.lister-list tr')
data = []

for movie in movies:
    title_column = movie.find('td', class_='titleColumn')
    rating = check_if_element_is_available(movie.find('strong'))
    title = title_column.a.text
    year = title_column.span.text.strip('()')
    genre = check_if_element_is_available(title_column.find('span', class_='genre'))
    director = title_column.find('a')['title']
    
    data.append([title, rating, year, genre, director])

# Step 4: Data Cleaning and Pre-processing
# (Optional: Perform necessary data cleaning and pre-processing steps here)

# Step 5: Saving data to a structured format (e.g., CSV)
csv_headers = ['Title', 'Rating', 'Year', 'Genre', 'Director']

with open('movie_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_headers)
    writer.writerows(data)

# Step 6: Exploratory Data Analysis
# (Perform exploratory data analysis using libraries like Pandas, Matplotlib, Seaborn, etc.)
# Load the data from the CSV file
df = pd.read_csv('movie_data.csv')

# Calculate descriptive statistics
average_rating = df['Rating'].mean()

# Identify the highest-rated movies based on IMDb ratings
top_rated_movies = df.nlargest(10, 'Rating')

# How does the rating change over time?
df['Year'] = pd.to_numeric(df['Year'])  # Convert 'Year' column to numeric
rating_by_year = df.groupby('Year')['Rating'].mean()

# Analyze the distribution of movie genres and determine the most popular genres
genre_counts = df['Genre'].value_counts()
top_genres = genre_counts.head(5)

# Explore any patterns or trends in the movie release years
year_counts = df['Year'].value_counts().sort_index()

# Visualize the data
# Plot the average rating
plt.figure(figsize=(8, 6))
plt.plot(rating_by_year.index, rating_by_year.values)
plt.xlabel('Year')
plt.ylabel('Average Rating')
plt.title('Average Movie Rating Over Time')
plt.show()

# Plot the distribution of movie genres
# plt.figure(figsize=(10, 6))
# top_genres.plot(kind='bar')
# plt.xlabel('Genre')
# plt.ylabel('Number of Movies')
# plt.title('Distribution of Movie Genres')
# plt.show()

# Plot the movie release years
plt.figure(figsize=(12, 6))
year_counts.plot(kind='line')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.title('Number of Movies Released by Year')
plt.show()
