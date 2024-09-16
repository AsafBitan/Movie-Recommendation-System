import sklearn as sk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
# import surprise as sp

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
tags_df = pd.read_csv(tags_file)
links_df = pd.read_csv(links_file)
genome_scores_df = pd.read_csv(genome_scores_file)
genome_tags_df = pd.read_csv(genome_tags_file)
merged_df = pd.merge(rating_df, movies_df, on='movieId')


print("ratings:\n", rating_df)
print("movies:\n",movies_df)
print("tags:\n",tags_df)
print("tags head:\n",tags_df.head(), "\n")
print("links:\n",links_df)
print("links head:\n",links_df.head(), "\n")
print("scores:\n",genome_scores_df)
print("tags:\n",genome_tags_df)
print("merged df: \n", merged_df)