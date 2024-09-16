import sklearn as sk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import difflib
from dotenv import load_dotenv
import os


load_dotenv()

data_path = os.getenv("DATA_PATH")

rating_file = os.path.join(data_path, "ratings.csv")
movies_file = os.path.join(data_path, "movies.csv")
tags_file = os.path.join(data_path, "tags.csv")
links_file = os.path.join(data_path, "links.csv")

user_ids_file = 'user_ids.csv'

# Load existing user data
try: 
    user_data = pd.read_csv('user_data.csv', index_col=0)
except FileNotFoundError:
    user_data = pd.DataFrame()


rating_df = pd.read_csv(rating_file)
movies_df = pd.read_csv(movies_file)


def get_next_user_id():
    if os.path.exists(user_ids_file):
        try:
            user_ids_df = pd.read_csv(user_ids_file)
            if not user_ids_df.empty:
                last_user_id = user_ids_df['userId'].max()
                return last_user_id +1
            else:
                return len(rating_df['userId'].unique()) + 1 
        except pd.errors.EmptyDataError:
            return len(rating_df['userId'].unique()) + 1 
    else: 
        return 1 
    
def save_new_user_id(user_id):
    if os.path.exists(user_ids_file):
        try:
            user_ids_df = pd.read_csv(user_ids_file)
            # If the file exists but is empty, create a new DataFrame with user_id
            if user_ids_df.empty:
                user_ids_df = pd.DataFrame({'userId': [user_id]})
            else:
                user_ids_df = pd.concat([user_ids_df, pd.DataFrame({'userId': [user_id]})], ignore_index=True)
        except pd.errors.EmptyDataError:
            # If file is empty or can't be read, create a new DataFrame with user_id
            user_ids_df = pd.DataFrame({'userId': [user_id]})
    else:
        # If file doesn't exist, create a new DataFrame with user_id
        user_ids_df = pd.DataFrame({'userId': [user_id]})

    user_ids_df.to_csv(user_ids_file, index=False)

def EDA(rating_df, movies_df):
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

    movie_user_matrix = merged_df.pivot_table(index='title', columns='userId', values='rating')
    print(movie_user_matrix.head())

    movie_to_check_name = 'Toy Story (1995)'

    if movie_to_check_name in movie_user_matrix.index:
        movie_to_check_ratings = movie_user_matrix.loc[movie_to_check_name]
        print(movie_to_check_ratings)
    else:
        print(f"Moive '{movie_to_check_name}' not found in the matix")


# tags_df = pd.read_csv(tags_file)
# links_df = pd.read_csv(links_file)

def collect_user_rating(movies_df, user_id):
    user_rating = []
    while len(user_rating) < 10:
        random_movie = movies_df.sample(n=1)
        movie_title = random_movie['title'].iloc[0]
        genre = random_movie['genres'].iloc[0]
        print(f"Movie: {movie_title} - Genre: {genre}")
        user_movie_rating = int(input(f"Rate the movie '{movie_title}' out of 5 (or 0 if you havent seen it): \n"))

        while user_movie_rating not in range(0,6):
            print("Invalid rating. Please enter a number between 0 and 5.")
            user_movie_rating = int(input(f"Rate the movie '{movie_title}' out of 5 (or 0 if you havent seen it): \n"))
        
        if user_movie_rating != 0:
            user_rating.append({'userId': user_id, 'movieId': random_movie['movieId'].iloc[0], 'rating': user_movie_rating})

    return user_rating

# def recommend_movie(rating_df, user_id):
#     want_rec = input("Do you want movie recommendations? (y/n): ").strip().lower()

#     if want_rec == "y":
#         user_data = pd.read_csv(f'user_data_{user_id}.csv')
#         print("User data before merging:")
#         print(user_data.head())

#         full_data = pd.concat([rating_df, user_data], ignore_index=True)


        
#         full_data['userId'] = full_data['userId'].astype(int)
#         full_data['movieId'] = full_data['movieId'].astype(int)

#         full_data = full_data.dropna(subset=['userId'])

#         movie_user_matrix = full_data.pivot_table(index='userId', columns='movieId', values='rating')
        
#         if user_id not in movie_user_matrix.index:
#             print(f"No ratings found for User {user_id}.")
#             return
#         # movie_user_matrix = movie_user_matrix.fillna(0)

#         similarity_matrix = movie_user_matrix.T.corr(method='pearson')

#         user_ratings = movie_user_matrix.loc[user_id]
#         user_ratings = user_ratings.fillna(0)

#         valid_users = user_ratings.index[user_ratings > 0]
#         similar_users = similarity_matrix.loc[valid_users, valid_users].mean(axis=1)

#         similar_users = similar_users.sort_values(ascending=False).head(5)

#         similar_user_ratings = movie_user_matrix.loc[similar_users.index]
#         recommended_movies = similar_user_ratings.mean(axis=0).sort_values(ascending=False)

#         recommended_movies = recommended_movies[recommended_movies.index.difference(user_ratings[user_ratings > 0].index)]

#         print("We recommend the following movies for you:")
#         print(recommended_movies.head(10))

#     else:
#         print("Bye!")
def recommend_movie(rating_df, user_id):
    want_rec = input("Do you want movie recommendations? (y/n): ").strip().lower()

    if want_rec == "y":
        # Load user data
        try:
            user_data = pd.read_csv(f'user_data_{user_id}.csv')
            print("User data before merging:")
            print(user_data.head())
        except FileNotFoundError:
            print(f"User data for {user_id} not found.")
            return
        
        # Concatenate the user's ratings with the existing dataset
        full_data = pd.concat([rating_df, user_data], ignore_index=True)

        # Convert userId and movieId to integers to ensure consistency
        full_data['userId'] = full_data['userId'].astype(int)
        full_data['movieId'] = full_data['movieId'].astype(int)

        # Drop rows with missing userId or movieId
        full_data = full_data.dropna(subset=['userId', 'movieId'])

        # Create the full user-item matrix
        movie_user_matrix = full_data.pivot_table(index='userId', columns='movieId', values='rating')

        # Get the user's ratings
        user_ratings = movie_user_matrix.loc[user_id]
        print("User Ratings:")
        print(user_ratings)

        # Get movies rated by the user
        rated_movies = user_ratings[user_ratings > 0].index
        print("Rated Movies:")
        print(rated_movies)

        # Filter the matrix to only include these movies for all users
        filtered_matrix = movie_user_matrix[rated_movies]
        print("Filtered User-item Matrix:")
        print(filtered_matrix.head())

        # Calculate the similarity matrix using Pearson correlation on the filtered matrix
        similarity_matrix = filtered_matrix.T.corr(method='pearson')

        # Calculate similarity for the user based on the filtered matrix
        similar_users = similarity_matrix.mean(axis=1)
        similar_users = similar_users.sort_values(ascending=False).head(5)

        # Get the ratings from similar users
        similar_user_ratings = filtered_matrix.loc[similar_users.index]
        print("Similar User Ratings:")
        print(similar_user_ratings.head())

        recommended_movies = similar_user_ratings.mean(axis=0)
        recommended_movies = recommended_movies.sort_values(ascending=False)

        # Ensure we have a list of movies to recommend
        if recommended_movies.empty:
            print("No movies to recommend based on similar users' ratings.")
            random_movie_id_list = rating_df['movieId'].dropna().sample(10).tolist()
            random_movie_list = []

            for movie_id in random_movie_id_list:
                movie_title = movies_df[movies_df['movieId'] == movie_id]['title']
                if not movie_title.empty:
                    random_movie_list.append(movie_title.values[0])
                else:
                    random_movie_list.append('Unknown')

            print("Here are some random movies for you:")
            for movie in random_movie_list:
                print(movie)
        else:
            # Select top 10 movies with the highest mean ratings
            top_recommended_movies = recommended_movies.head(10)
            print("We recommend the following movies for you:")
            for movie_id in top_recommended_movies.index:
                movie_name = movies_df[movies_df['movieId'] == movie_id]['title'].values
                if movie_name.size > 0:
                    print(f"Movie ID {movie_id}: {movie_name[0]}")
                else:
                    print(f"Movie ID {movie_id}: Unknown Movie")
    else:
        print("Bye!")



# Ask if the user is new
def handle_new_user(user_data, rating_df, movies_df):
    is_new_user = input("Are you a new user? (y/n): ").strip().lower()

    if is_new_user == "y":
        user_id = get_next_user_id()
        print(f"Welcom, User {user_id}!")
        user_ratings = collect_user_rating(movies_df, user_id)
        user_df = pd.DataFrame(user_ratings)

        user_df.to_csv(f"user_data_{user_id}.csv", index=False)
        save_new_user_id(user_id)

        print(f"User {user_id}'s data has been saved to 'user_data_{user_id}.csv'.")
        recommend_movie(rating_df, user_id)

    elif is_new_user == "n":
        try: 
            user_id = int(input("please enter your user ID: "))
            user_data = pd.read_csv(f"user_data_{user_id}.csv")
            print(f"Welcome back, User {user_id}!")
            recommend_movie(rating_df, user_id)
        except FileNotFoundError:
            print(f"User data for User {user_id} not found. Please tr again.")
            handle_new_user(user_data, rating_df, movies_df)
    else:
        print("please answer 'y' or 'n. ")
        handle_new_user(user_data, rating_df, movies_df)


#handle_new_user(user_data, rating_df, movies_df)
# EDA(rating_df, movies_df)
recommend_movie(rating_df, user_id=612)




