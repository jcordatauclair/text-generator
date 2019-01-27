#! usr/bin/env python3
# -*- coding: utf-8 -*-

# GenIt : v0.3

# IMPORTS ---------------------------------------------------------------------#
import praw                         # https://praw.readthedocs.io/en/latest/
import prawcore                     # https://pypi.org/project/prawcore/
import twitter                      # https://developer.twitter.com/en/docs.html
import wikiquotes                   # https://pypi.org/project/wikiquotes/
import imdb                         # https://media.readthedocs.org/pdf/imdbpy/latest/imdbpy.pdf

from textgenrnn import textgenrnn   # https://github.com/minimaxir/textgenrnn
from tqdm import tqdm               # https://github.com/tqdm/tqdm
from pyfiglet import Figlet         # https://github.com/pwaller/pyfiglet
from keras import backend as k
from shutil import copyfile

import cli
import config
import sys
import os
import os.path
#------------------------------------------------------------------------------#


# MISC ------------------------------------------------------------------------#
# Disables the warning (doesn't enable AVX/FMA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Reset textgenrnn
textgen = textgenrnn()
textgen.reset()

# Styling in CLI
class bcolors:
    HEADER = '\033[96m'
    INFO = '\033[7m'
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

success_logo = '[' + bcolors.OKGREEN + 'o' + bcolors.END + ']' + ' '
warning_logo = '[' + bcolors.WARNING + '!' + bcolors.END + ']' + ' '
fail_logo = '[' + bcolors.FAIL + 'x' + bcolors.END + ']' + ' '
info_logo = '[' + bcolors.OKBLUE + '-' + bcolors.END + ']' + ' '
#------------------------------------------------------------------------------#


# CORE ------------------------------------------------------------------------#
print(bcolors.ITALIC
      + bcolors.UNDERLINE
      + 'v0.3'
      +bcolors.END)

f = Figlet(font='slant')
print(bcolors.BOLD
      + f.renderText('GenIt')
      + bcolors.END)

# Q : What do you want to generate?
what_q = 'Select what kind of text you want to generate'
what_c = ['Reddit posts titles',
          'Tweets',
          'Quotes',
          'Movies titles',
          'Other (use a local file)']
what_a = cli.selection_menu(what_q, what_c)
what_type = what_a.get('choice')


if (what_type == what_c[0]): # Reddit posts titles have been chosen

    # API / authentication
    reddit_log = praw.Reddit(client_id = config.reddit_client_id,
                             client_secret = config.reddit_client_secret,
                             user_agent = config.reddit_user_agent,
                             username = config.reddit_username,
                             password = config.reddit_password)

    cli.delete_last_lines(len(what_c) + 1)

    try:
        print(info_logo
              + "Logging in...")
        reddit_log.user.me()
    except prawcore.exceptions.ResponseException:
        cli.delete_last_lines(1)
        print(fail_logo
              + "Can't log in to your Reddit account. Please double check your credentials and try again.")
        k.clear_session()
        sys.exit(1)

    cli.delete_last_lines(1)
    print(success_logo
          + "Logged in")


    # Q : Which subreddit?
    while True:
        try:
            subreddit_a = cli.type_answer_menu('Of which subreddit?',
                                               'None')
            subreddit_name = subreddit_a.get('answer')
            file_name = '../results/reddit_' + subreddit_name + '.txt' # output file
            print(info_logo
                  + "Searching for the subreddit...")
            reddit_log.subreddits.search_by_name(subreddit_name,
                                                 exact = True)
        except prawcore.exceptions.NotFound:
            cli.delete_last_lines(1)
            print(warning_logo
                  + "This subreddit doesn't exist. Please try another one.")
            continue
        else:
            cli.delete_last_lines(1)
            subreddit = reddit_log.subreddit(subreddit_name)
            print(success_logo
                  + "Subreddit found")
            break

elif (what_type == what_c[1]): # Twitter has been chosen

    # API / authentication
    twitter_log = twitter.Api(consumer_key = config.twitter_consumer_key,
                              consumer_secret = config.twitter_consumer_secret,
                              access_token_key = config.twitter_access_token_key,
                              access_token_secret = config.twitter_access_token_secret,
                              tweet_mode = 'extended')

    cli.delete_last_lines(len(what_c) + 1)

    try:
        print(info_logo
              + "Logging in...")
        twitter_log.VerifyCredentials()
    except twitter.error.TwitterError:
        cli.delete_last_lines(1)
        print(fail_logo
              + "Can't log in to your Twitter account. Please double check your credentials and try again.")
        k.clear_session()
        sys.exit(1)

    cli.delete_last_lines(1)
    print(success_logo
          + "Logged in")


    # Q : Which user?
    while True:
        try:
            user_a = cli.type_answer_menu('Of which user?',
                                          'None')
            user_name = user_a.get('answer')
            file_name = '../results/twitter_' + user_name + '.txt' # output file
            print(info_logo
                  + "Searching for the user...")
            twitter_log.GetUserTimeline(screen_name = user_name,
                                        count = 1)
        except twitter.error.TwitterError:
            cli.delete_last_lines(1)
            print(warning_logo
                  + "This user doesn't exist. Please try another one.")
            continue
        else:
            cli.delete_last_lines(1)
            print(success_logo
                  + "User found")
            break


elif (what_type == what_c[2]): # Quotes have been chosen

    cli.delete_last_lines(len(what_c) + 1)

    # Q : Which author?
    while True:
        author_a = cli.type_answer_menu('Of which author?',
                                        'None')
        author_name = author_a.get('answer')
        file_name = '../results/quotes_' + author_name + '.txt' # output file
        print(info_logo
              + "Searching for the author...")
        n_quotes = len(wikiquotes.get_quotes(author_name, 'english'))
        if (n_quotes < 20):
            cli.delete_last_lines(1)
            print(warning_logo
                  + "This author doesn't have enough quotes. Please try another one.")
            continue
        else:
            cli.delete_last_lines(1)
            print(success_logo
                  + "Author found")
            break


elif (what_type == what_c[3]): # Movies titles have been chosen

    cli.delete_last_lines(len(what_c) + 1)

    file_name = '../results/movies_titles.txt' # output file


elif (what_type == what_c[4]): # Local file has been chosen

    cli.delete_last_lines(len(what_c) + 1)

    # Q : What file?
    while True:
        file_a = cli.type_answer_menu('Enter the path of your file',
                                      'None')
        file_path = file_a.get('answer')
        file_name = '../results/random_text_from_file_' + file_path + '.txt' # output file
        print(info_logo
              + "Searching for the file...")
        file_exists = os.path.isfile(file_path)
        if (file_exists == False):
            cli.delete_last_lines(1)
            print(warning_logo
                  + "This file doesn't exist. Please try with another one.")
            continue
        else:
            cli.delete_last_lines(1)
            print(success_logo
                  + "File found")
            break


# Q : Which performance?
epochs_q = 'Select which performance you want'
epochs_c = ['Very low (very fast processing but very imprecise results)',
            'Low (fast processing but inaccurate results)',
            'Medium (recommended)',
            'High (accurate results but slow processing)',
            'Very high (very precise results but extremely slow processing)']
epochs_a = cli.selection_menu(epochs_q, epochs_c)
epochs_aprox = epochs_a.get('choice')

if (epochs_aprox == epochs_c[0]):
    epochs_number = 1
elif (epochs_aprox == epochs_c[1]):
    epochs_number = 10
elif (epochs_aprox == epochs_c[2]):
    epochs_number = 20
elif (epochs_aprox == epochs_c[3]):
    epochs_number = 40
elif (epochs_aprox == epochs_c[4]):
    epochs_number = 80

cli.delete_last_lines(len(epochs_c) + 1)


# Q : How many results?
results_q = 'Select the number of results you want'
results_c = ['10',
             '50',
             '100']
results_a = cli.selection_menu(results_q, results_c)
results_aprox = results_a.get('choice')

if (results_aprox == results_c[0]):
    results_number = 10
elif (results_aprox == results_c[1]):
    results_number = 50
elif (results_aprox == results_c[2]):
    results_number = 100

cli.delete_last_lines(len(results_c) + 1)


# Q : Prefix or not?
prefix_q = 'Do you want to set a prefix?'
prefix_c = ['Yes',
            'No']
prefix_a = cli.selection_menu(prefix_q, prefix_c)
prefix_bool = prefix_a.get('choice')

cli.delete_last_lines(len(prefix_c) + 1)

if (prefix_bool == prefix_c[0]):
    prefix_a = cli.type_answer_menu('Which one?',
                                    'None')
    prefix_name = prefix_a.get('answer')


# Collecting data
print(info_logo
      + 'Collecting data...')

if (what_type == what_c[0]):
    with open('../data/data.txt', 'w+') as f:
        for submission in tqdm(subreddit.top(limit = 1000)):
            f.write(submission.title + '\n')
elif (what_type == what_c[1]):
    t = twitter_log.GetUserTimeline(screen_name = user_name,
                                count = 200)
    tweets = [i.AsDict() for i in t]
    with open('../data/data.txt', 'w+') as f:
        for t in tqdm(tweets):
            f.write(t['full_text'] + '\n')
elif (what_type == what_c[2]):
    quotes = wikiquotes.get_quotes(author_name, 'english')
    with open('../data/data.txt', 'w+') as f:
        for q in tqdm(quotes):
            f.write(q + '\n')
elif (what_type == what_c[3]):
    ia = imdb.IMDb()
    movies = ia.get_top250_movies()
    with open('../data/data.txt', 'w+') as f:
        for i in tqdm(range(1, 250)):
            f.write(movies[i]['title'] + '\n')
elif (what_type == what_c[4]):
    copyfile(file_path, '../data/data.txt')

cli.delete_last_lines(1)
print(success_logo
      + "Data collected")


# Learning
print(info_logo
      + "Training...")
textgen.train_from_file('../data/data.txt',
                        num_epochs = epochs_number)
cli.delete_last_lines(1)
print(success_logo
      + "Data trained")


# Generating results
print(info_logo
      + "Generating results...")
if (prefix_bool == prefix_c[0]):
    textgen.generate(n_results,
                     prefix = prefix_name)
elif (prefix_bool == prefix_c[1]):
    textgen.generate(results_number)
cli.delete_last_lines(1)
print(success_logo
      + "Results generated")


# Writing results to a file
print(info_logo
      + "Writing to file...")
textgen.generate_to_file(file_name, n = results_number)
cli.delete_last_lines(1)
print(success_logo
      + bcolors.OKGREEN
      + bcolors.BOLD
      + "Done! "
      + bcolors.END
      + "You can now check the results here: "
      + file_name)
#------------------------------------------------------------------------------#
