# Physician & AI Responses to Urology Patient Questions
# Desc: Comparing Physician & Artificial Intelligence Chatbot Responses to Patient
# Urology-Specific Questions Posted to Public Social Media Forums (Reddit)
# Code by: Dipak Subramaniam <dsubram@siue.edu>
# In coordination with: Andrew Gabrielson <agabrie7@jhmi.edu>, Brendan Wallace <bwalla25@jhmi.edu>,
# Pranjal Agrawal <pagrawa9@jhmi.edu>, Aurora Grutman <agrutma1@jhmi.edu>, Taylor Kohn <tkohn2@jhmi.edu>
# Version: 0.1
# Script: Parser for askdocs subreddit
# Start date: May 27, 2023

# imports
import praw
import pandas as pd
import time
from praw.models import MoreComments
import matplotlib
import warnings
import numpy
import openpyxl
from prawcore.exceptions import ResponseException

# List of urology-related terms# List of urology-related terms
urology_terms = ['Prostate Cancer', 'prostate', 'Kidney Cancer', 'kidney', 'Bladder Cancer', 'bladder',
                 'Benign Prostatic Hyperplasia', 'BPH', 'Kidney Stones', 'kidney stone', 'Male Infertility',
                 'Erectile Dysfunction', 'ED', 'Urinary Tract Infection', 'UTI', 'blood in urine', 'urine blood',
                 'poor bladder control', 'urine leakage', 'difficulty urinating', 'incontinence', 'cystectomy',
                 'erection', 'bladder control', 'loss of bladder control', 'nephrectomy', 'orchiectomy',
                 'prostatectomty', 'pyuria', 'stress urinary incontinence', 'urinary incontinence', 'urethra',
                 'vasectomy', 'varicocele', 'vas deferens', 'ureter', 'urodynamics', 'seminal vesicle', 'prostatitis',
                 'priprism', 'hematuria', 'enuresis', 'brachytherapy', 'urine', 'pee', 'testicles', 'balls', 'penis',
                 'vagina', 'infertility', 'sexual medicine']
uro_lower = set([x.lower() for x in urology_terms])

# timing
begin = time.time()

# PRAW: Python wrapper for Reddit API - instance registered with Reddit
r = praw.Reddit(client_id='eaGtkvifo9nu2SmL75NtRw', client_secret='e6dLUXpvNjx15G20FjRBC2DcSs0h_A',
                redirect_uri='http://localhost:8080', user_agent='redscrape')
print(r.auth.url(scopes=["identity"], state="...", duration="permanent"))
print('<|> connected PRAW')
r.read_only = True

# Loop through the hot posts of the subreddit
subred = 'AskDocs'
askdocs_data = []
sub = r.subreddit(subred)
print('<|> Subreddit: ', subred)
hotpost = 0
for post in sub.search('flair:"Physician Responded"', syntax='lucene', limit=1000):
    print('<|> Hot Post #', hotpost+1)
    hotpost = hotpost + 1
    # Check if the post is urology-related
    title = set(post.title.split())
    text = set(post.selftext.split())
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue
        com = set(comment.body.split())
        print('<|> title flag(s): ', list(uro_lower & title))
        print('<|> text flag(s): ', list(uro_lower & text))
        print('<|> comment flag(s): ', list(uro_lower & com))
        # Loop through the comments of the post
        if uro_lower.intersection(title) or uro_lower.intersection(text) or uro_lower.intersection(com):
            print('<|> Found physician response')
            # If the comment is from a physician
            print('<|> Author Flair: ', comment.author_flair_text)
            if comment.author_flair_text != None and ('Physician' in comment.author_flair_text or 'MD' in comment.author_flair_text):
                # Append the post title (or content), post body and comment body to your data
                askdocs_data.append([post.title, post.selftext, comment.body, comment.author_flair_text])
                print('<|> Physician response saved!')

# Convert the data lists into pandas DataFrames
askdocs_df = pd.DataFrame(askdocs_data, columns=['Question Title', 'Question Body', 'Physician Response', 'Author'])
print('<|> List converted to dataframe')

# Save the DataFrames into an Excel file using openpyxl
askdocs_df.to_excel('askdocs_parsed_v2.xlsx', index=False)
print('<|> Dataframe saved as excel file')

# * timing
print("<|> %s seconds" % (time.time() - begin))
