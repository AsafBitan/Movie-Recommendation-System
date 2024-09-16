import sklearn as sk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from dotenv import load_dotenv
import os


load_dotenv()

data_path = os.getenv("DATA_PATH")

rating_file = os.path.join(data_path, "ratings.csv")
movies_file = os.path.join(data_path, "movies.csv")
tags_file = os.path.join(data_path, "tags.csv")
links_file = os.path.join(data_path, "links.csv")
genome_scores_file = os.path.join(data_path, "genome-scores.csv")
genome_tags_file = os.path.join(data_path, "genome-tags.csv")



rating_df = pd.read_csv(rating_file)
movies_df = pd.read_csv(movies_file)
# tags_df = pd.read_csv(tags_file)
# links_df = pd.read_csv(links_file)

# Checking for missing values
print(rating_df.isnull().sum(),"\n")
print(movies_df.isnull().sum(),"\n")

# Getting basic statistics about the ratings
print(rating_df.describe(),"\n")

print(f"Number of unique Users: {rating_df['userId'].nunique()}")
print(f"Number of unique Movies: {rating_df['movieId'].nunique()}","\n")

# Check for the most rated movies
most_rated_movies = rating_df.groupby('movieId').size().sort_values(ascending=False).head(10)
print(most_rated_movies,"\n")



merged_df = pd.merge(rating_df, movies_df, on='movieId')

# Check for the most rated movies
popular_movies = merged_df.groupby('title').size().sort_values(ascending=False).head(10)
print(popular_movies,"\n")

sns.countplot(x='rating', data=rating_df)
plt.title('Destribution of Movie Ratings')
plt.show()

movie_user_marix = merged_df.pivot_table(index='title', columns='userId', values='rating')
print(movie_user_marix.head())

movie_to_check_name = 'Toy Story (1995)'

movie_to_check_ratings = movie_user_marix[movie_to_check_name]
similar_movies = movie_user_marix.corrwith(movie_to_check_ratings)
similar_movies = similar_movies.dropna().sort_values(ascending=False)

# print("ratings:\n", rating_df)
# print("movies:\n",movies_df)
# print("tags:\n",tags_df)
# print("links:\n",links_df)
#print("merged df: \n", merged_df)

