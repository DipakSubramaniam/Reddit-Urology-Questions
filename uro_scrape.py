# Physician & AI Responses to Urology Patient Questions
# Desc: Comparing Physician & Artificial Intelligence Chatbot Responses to Patient
# Urology-Specific Questions Posted to Public Social Media Forums (Reddit)
# Code by: Dipak Subramaniam <dsubram@siue.edu>
# In coordination with: Andrew Gabrielson <agabrie7@jhmi.edu>, Brendan Wallace <bwalla25@jhmi.edu>,
# Pranjal Agrawal <pagrawa9@jhmi.edu>, Aurora Grutman <agrutma1@jhmi.edu>, Taylor Kohn <tkohn2@jhmi.edu>
# Version: 0.1
# Script: General scraper for urology-related subreddits
# Start date: May 27, 2023

# imports
import praw
import pandas as pd
import time
import openpyxl
from prawcore.exceptions import ResponseException
import networkx as nx
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import matplotlib
import warnings
import numpy

# timing
begin = time.time()

# PRAW: Python wrapper for Reddit API - instance registered with Reddit
r = praw.Reddit(client_id='eaGtkvifo9nu2SmL75NtRw', client_secret='e6dLUXpvNjx15G20FjRBC2DcSs0h_A',
                redirect_uri='http://localhost:8080', user_agent='redscrape')
print(r.auth.url(scopes=["identity"], state="...", duration="permanent"))
print('<|> connected PRAW')
r.read_only = True

# try:
#     print("Authenticated as {}".format(r.user.me()))
# except ResponseException:
#     print("Something went wrong during authentication")
# print(r.user.me())

# Subreddits to scrape
subreddits = ['AskDocs', 'KidneyStones', 'ProstateCancer', 'Infertility', 'ErectileDysfunction', 'SexualHealth']

# Data storage
askdocs_data = []
other_sub_data = []

# List of urology-related terms
urology_terms = ['Prostate Cancer', 'Kidney Cancer', 'Bladder Cancer', 'BPH', 'Benign Prostatic Hyperplasia',
                 'Kidney Stones', 'Male Infertility', 'Erectile Dysfunction']


# Function to check if a post or a comment contains any of the urology-related terms
def urology_related(text):
    for term in urology_terms:
        if term.lower() in text.lower():
            return True
    return False


# Loop through the subreddits
for subreddit in subreddits:
    sub = r.subreddit(subreddit)
    print('<|> Subreddit: ', subreddit)
    # Loop through the hot posts of the subreddit
    hotpost = 0
    for post in sub.hot(limit=200):
        print('<|> Hot Post #', hotpost+1)
        hotpost = hotpost + 1
        # If the subreddit is 'AskDocs', check if the post is urology-related
        if subreddit == 'AskDocs':
            if post.link_flair_text == 'Physician Responded' and (urology_related(post.title) or urology_related(post.selftext)):
                print('<|> Found physician response')
                # Loop through the comments of the post
                for comment in post.comments:
                    # If the comment is from a physician
                    if 'Physician' in comment.author_flair_text:
                        # Append the post title (or content), post body and comment body to your data
                        askdocs_data.append([post.title, post.selftext, comment.body])
                        print('<|> Physician response saved!')
        # For other subreddits, assume all posts are relevant and just check for physician responses
        else:
            # Loop through the comments of the post
            for comment in post.comments:
                # Check if post is urology-related
                if urology_related(post.title) or urology_related(post.selftext):
                    # Append the subreddit name, post title (or content), post body and comment body to your data
                    other_sub_data.append([subreddit, post.title, post.selftext, comment.body])
                    print('<|> Urology-related response saved!')

# Convert the data lists into pandas DataFrames
askdocs_df = pd.DataFrame(askdocs_data, columns=['Question Title', 'Question Body', 'Physician Response'])
other_sub_df = pd.DataFrame(other_sub_data, columns=['Subreddit', 'Question Title', 'Question Body', 'Possible Physician Response'])
print('<|> Lists converted to dataframes')

# Save the DataFrames into separate Excel files using openpyxl
askdocs_df.to_excel('askdocs_data.xlsx', index=False)
other_sub_df.to_excel('other_sub_data.xlsx', index=False)
print('<|> Dataframes saved as excel files')

# * timing
print("<|> %s seconds" % (time.time() - begin))

# with pd.ExcelWriter('reddit_data.xlsx') as writer:
#     askdocs_df.to_excel(writer, sheet_name='AskDocs', index=False)
#     other_sub_df.to_excel(writer, sheet_name='Other Subreddits', index=False)


