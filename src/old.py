
#----------------------------------- TWITTER ----------------------------------#
elif (what_a.get('choice') == what_c[1]):

        # API / authentication
        twitter = twitter.Api(consumer_key = config.twitter_consumer_key,
                              consumer_secret = config.twitter_consumer_secret,
                              access_token_key = config.twitter_access_token_key,
                              access_token_secret = config.twitter_access_token_secret,
                              tweet_mode = 'extended')


        # Get : username
        try:
            user_name = input(bcolors.HEADER
                              + 'From which user? '
                              + '\n'
                              + '> '
                              + bcolors.END)
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Get : number of epochs
        try:
            n_epochs = input(bcolors.HEADER
                             + 'On a scale of 1 (fast but inaccurate) to 10 (effective but slow), which number would you choose?'
                             + '\n'
                             + '> '
                             + bcolors.END)
            n_epochs = int(n_epochs)
            if n_epochs not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                print(bcolors.WARNING
                      + 'Invalid number!'
                      + bcolors.END)
                exit(1)
            if (n_epochs == 0):
                number_epochs = 1
            elif (n_epochs != 0):
                number_epochs = n_epochs * 5
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Get : number of results
        try:
            n_results = input(bcolors.HEADER
                              + 'How many results? (min is 1, max is 100)'
                              + '\n'
                              + '> '
                              + bcolors.END)
            n_results = int(n_results)

            if (n_results < 1) or (n_results > 100):
                print(bcolors.WARNING
                      + 'Invalid number!'
                      + bcolors.END)
                exit(1)
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Get : prefix wanted
        try:
            prefix = input(bcolors.HEADER
                           + 'Do you want a prefix? (Y/N)'
                           + '\n'
                           + '> '
                           + bcolors.END)

            if prefix.lower() not in ['y', 'n']:
                print(bcolors.WARNING
                      + 'Invalid answer!'
                      + bcolors.END)
                exit(1)
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Case : prefix is wanted
        if (prefix.lower() == 'y'):
            try:
                prefix_name = input(bcolors.HEADER
                                    + 'Which one? '
                                    + '\n'
                                    + '> '
                                    + bcolors.END)

            except KeyboardInterrupt:
                print(' → '
                      + bcolors.FAIL
                      + 'Interrupted'
                      + bcolors.END)
                exit(0)


        # Collecting data
        print(bcolors.OKBLUE
              + 'Collecting data...'
              + bcolors.END)

        t = twitter.GetUserTimeline(screen_name = user_name,
                                    count = 200)
        tweets = [i.AsDict() for i in t]

        with open('../data/data.txt', 'w+') as f:
            for t in tqdm(tweets):
                f.write(t['full_text'] + '\n')


        # Case : prefix is wanted
        if (prefix.lower() == 'y'):
            print(bcolors.OKBLUE
                  + 'Generating '
                  + str(n_results)
                  + ' random tweets like user "https://twitter.com/'
                  + user_name
                  + '/" with prefix "'
                  + prefix_name
                  + '" using '
                  + str(number_epochs)
                  + ' epochs...'
                  + bcolors.END)

            textgen.train_from_file('../data/data.txt',
                                    num_epochs = number_epochs)

            textgen.generate(n_results, prefix = prefix_name)


        # Case : prefix is not wanted
        elif (prefix.lower() == 'n'):
            print(bcolors.OKBLUE
                  + 'Generating '
                  + str(n_results)
                  + ' random tweets like user "https://twitter.com/'
                  + user_name
                  + '/" using '
                  + str(number_epochs)
                  + ' epochs...'
                  + bcolors.END)

            textgen.train_from_file('../data/data.txt',
                                    num_epochs = number_epochs)

            textgen.generate(n_results)

        print(bcolors.OKBLUE
              + '\n'
              + 'Writing results to file...'
              + '\n'
              + bcolors.END)


        # Print results in a file
        file_name = '../results/tweets_' + user_name + '.txt'
        textgen.generate_to_file(file_name, n = n_results)

        print(bcolors.OKGREEN
              + 'Results are located in file '
              + bcolors.BOLD
              + file_name
              + bcolors.END)
#------------------------------------------------------------------------------#

#------------------------------------ QUOTES ----------------------------------#
elif (what_a.get('choice') == what_c[2]):

    # Get : name of the author
    try:
        author_name = input(bcolors.HEADER
                          + 'From which author? '
                          + '\n'
                          + '> '
                          + bcolors.END)
    except KeyboardInterrupt:
        print(' → '
              + bcolors.FAIL
              + 'Interrupted'
              + bcolors.END)
        exit(0)


    # Get : number of epochs
    try:
        n_epochs = input(bcolors.HEADER
                         + 'On a scale of 1 (fast but inaccurate) to 10 (effective but slow), which number would you choose?'
                         + '\n'
                         + '> '
                         + bcolors.END)
        n_epochs = int(n_epochs)
        if n_epochs not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            print(bcolors.WARNING
                  + 'Invalid number!'
                  + bcolors.END)
            exit(1)
        if (n_epochs == 0):
            number_epochs = 1
        elif (n_epochs != 0):
            number_epochs = n_epochs * 5
    except KeyboardInterrupt:
        print(' → '
              + bcolors.FAIL
              + 'Interrupted'
              + bcolors.END)
        exit(0)


    # Get : number of results
    try:
        n_results = input(bcolors.HEADER
                          + 'How many results? (min is 1, max is 100)'
                          + '\n'
                          + '> '
                          + bcolors.END)
        n_results = int(n_results)

        if (n_results < 1) or (n_results > 100):
            print(bcolors.WARNING
                  + 'Invalid number!'
                  + bcolors.END)
            exit(1)
    except KeyboardInterrupt:
        print(' → '
              + bcolors.FAIL
              + 'Interrupted'
              + bcolors.END)
        exit(0)


    # Get : prefix wanted
    try:
        prefix = input(bcolors.HEADER
                       + 'Do you want a prefix? (Y/N)'
                       + '\n'
                       + '> '
                       + bcolors.END)

        if prefix.lower() not in ['y', 'n']:
            print(bcolors.WARNING
                  + 'Invalid answer!'
                  + bcolors.END)
            exit(1)
    except KeyboardInterrupt:
        print(' → '
              + bcolors.FAIL
              + 'Interrupted'
              + bcolors.END)
        exit(0)


    # Case : prefix is wanted
    if (prefix.lower() == 'y'):
        try:
            prefix_name = input(bcolors.HEADER
                                + 'Which one?'
                                + '\n'
                                + '> '
                                + bcolors.END)

        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


    # Collecting data
    print(bcolors.OKBLUE
          + 'Collecting data...'
          + bcolors.END)

    quotes = wikiquotes.get_quotes(author_name, "english")

    with open('../data/data.txt', 'w+') as f:
        for q in tqdm(quotes):
            f.write(q + '\n')


    # Case : prefix is wanted
    if (prefix.lower() == 'y'):
        print(bcolors.OKBLUE
              + 'Generating '
              + str(n_results)
              + ' random quotes like '
              + author_name
              + ' with prefix "'
              + prefix_name
              + '" using '
              + str(number_epochs)
              + ' epochs...'
              + bcolors.END)

        textgen.train_from_file('../data/data.txt',
                                num_epochs = number_epochs)

        textgen.generate(n_results, prefix = prefix_name)


    # Case : prefix is not wanted
    elif (prefix.lower() == 'n'):
        print(bcolors.OKBLUE
              + 'Generating '
              + str(n_results)
              + ' random quotes like '
              + author_name
              + ' using '
              + str(number_epochs)
              + ' epochs...'
              + bcolors.END)

        textgen.train_from_file('../data/data.txt',
                                num_epochs = number_epochs)

        textgen.generate(n_results)

    print(bcolors.OKBLUE
          + '\n'
          + 'Writing results to file...'
          + '\n'
          + bcolors.END)


    # Print results in a file
    file_name = '../results/quotes_' + author_name + '.txt'
    textgen.generate_to_file(file_name, n = n_results)

    print(bcolors.OKGREEN
          + 'Results are located in file '
          + bcolors.BOLD
          + file_name
          + bcolors.END)
#------------------------------------------------------------------------------#

#-------------------------------- MOVIES TITLES -------------------------------#
elif (what_a.get('choice') == what_c[3]):


        # Get : number of epochs
        try:
            n_epochs = input(bcolors.HEADER
                             + 'On a scale of 1 (fast but inaccurate) to 10 (effective but slow), which number would you choose?'
                             + '\n'
                             + '> '
                             + bcolors.END)
            n_epochs = int(n_epochs)
            if n_epochs not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                print(bcolors.WARNING
                      + 'Invalid number!'
                      + bcolors.END)
                exit(1)
            if (n_epochs == 0):
                number_epochs = 1
            elif (n_epochs != 0):
                number_epochs = n_epochs * 5
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Get : number of results
        try:
            n_results = input(bcolors.HEADER
                              + 'How many results? (min is 1, max is 100)'
                              + '\n'
                              + '> '
                              + bcolors.END)
            n_results = int(n_results)

            if (n_results < 1) or (n_results > 100):
                print(bcolors.WARNING
                      + 'Invalid number!'
                      + bcolors.END)
                exit(1)
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Get : prefix wanted
        try:
            prefix = input(bcolors.HEADER
                           + 'Do you want a prefix ? (Y/N)'
                           + '\n'
                           + '> '
                           + bcolors.END)

            if prefix.lower() not in ['y', 'n']:
                print(bcolors.WARNING
                      + 'Invalid answer!'
                      + bcolors.END)
                exit(1)
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Case : prefix is wanted
        if (prefix.lower() == 'y'):
            try:
                prefix_name = input(bcolors.HEADER
                                    + 'Which one?'
                                    + '\n'
                                    + '> '
                                    + bcolors.END)

            except KeyboardInterrupt:
                print(' → '
                      + bcolors.FAIL
                      + 'Interrupted'
                      + bcolors.END)
                exit(0)


        # Collecting data
        print(bcolors.OKBLUE
              + 'Collecting data...'
              + bcolors.END)

        ia = imdb.IMDb()
        movies = ia.get_top250_movies()

        with open('../data/data.txt', 'w+') as f:
            for i in tqdm(range(1, 250)):
                f.write(movies[i]['title'] + '\n')


        # Case : prefix is wanted
        if (prefix.lower() == 'y'):
            print(bcolors.OKBLUE
                  + 'Generating '
                  + str(n_results)
                  + ' random movies titles with prefix "'
                  + prefix_name
                  + '" using '
                  + str(number_epochs)
                  + ' epochs...'
                  + bcolors.END)

            textgen.train_from_file('../data/data.txt',
                                    num_epochs = number_epochs)

            textgen.generate(n_results, prefix = prefix_name)


        # Case : prefix is not wanted
        elif (prefix.lower() == 'n'):
            print(bcolors.OKBLUE
                  + 'Generating '
                  + str(n_results)
                  + ' random movies titles using '
                  + str(number_epochs)
                  + ' epochs...'
                  + bcolors.END)

            textgen.train_from_file('../data/data.txt',
                                    num_epochs = number_epochs)

            textgen.generate(n_results)

        print(bcolors.OKBLUE
              + '\n'
              + 'Writing results to file...'
              + '\n'
              + bcolors.END)


        # Print results in a file
        file_name = '../results/movies_titles.txt'
        textgen.generate_to_file(file_name, n = n_results)

        print(bcolors.OKGREEN
              + 'Results are located in file '
              + bcolors.BOLD
              + file_name
              + bcolors.END)
#------------------------------------------------------------------------------#

#---------------------------------- LOCAL FILE --------------------------------#
elif (what_a.get('choice') == what_c[4]):

        # Get : path of the file
        try:
            file_path = input(bcolors.HEADER
                              + 'From which file? (enter path)'
                              + '\n'
                              + '> '
                              + bcolors.END)
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)

        # Get : number of epochs
        try:
            n_epochs = input(bcolors.HEADER
                             + 'On a scale of 1 (fast but inaccurate) to 10 (effective but slow), which number would you choose?'
                             + '\n'
                             + '> '
                             + bcolors.END)
            n_epochs = int(n_epochs)
            if n_epochs not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                print(bcolors.WARNING
                      + 'Invalid number!'
                      + bcolors.END)
                exit(1)
            if (n_epochs == 0):
                number_epochs = 1
            elif (n_epochs != 0):
                number_epochs = n_epochs * 5
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Get : number of results
        try:
            n_results = input(bcolors.HEADER
                              + 'How many results? (min is 1, max is 100)'
                              + '\n'
                              + '> '
                              + bcolors.END)
            n_results = int(n_results)

            if (n_results < 1) or (n_results > 100):
                print(bcolors.WARNING
                      + 'Invalid number!'
                      + bcolors.END)
                exit(1)
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Get : prefix wanted
        try:
            prefix = input(bcolors.HEADER
                           + 'Do you want a prefix? (Y/N)'
                           + '\n'
                           + '> '
                           + bcolors.END)

            if prefix.lower() not in ['y', 'n']:
                print(bcolors.WARNING
                      + 'Invalid answer!'
                      + bcolors.END)
                exit(1)
        except KeyboardInterrupt:
            print(' → '
                  + bcolors.FAIL
                  + 'Interrupted'
                  + bcolors.END)
            exit(0)


        # Case : prefix is wanted
        if (prefix.lower() == 'y'):
            try:
                prefix_name = input(bcolors.HEADER
                                    + 'Which one?'
                                    + '\n'
                                    + '> '
                                    + bcolors.END)

            except KeyboardInterrupt:
                print(' → '
                      + bcolors.FAIL
                      + 'Interrupted'
                      + bcolors.END)
                exit(0)


        # Case : prefix is wanted
        if (prefix.lower() == 'y'):
            print(bcolors.OKBLUE
                  + 'Generating '
                  + str(n_results)
                  + ' random sentences with prefix "'
                  + prefix_name
                  + '" using '
                  + str(number_epochs)
                  + ' epochs...'
                  + bcolors.END)

            textgen.train_from_file(file_path,
                                    num_epochs = number_epochs)

            textgen.generate(n_results, prefix = prefix_name)


        # Case : prefix is not wanted
        elif (prefix.lower() == 'n'):
            print(bcolors.OKBLUE
                  + 'Generating '
                  + str(n_results)
                  + ' random sentences using '
                  + str(number_epochs)
                  + ' epochs...'
                  + bcolors.END)

            textgen.train_from_file('../data/data.txt',
                                    num_epochs = number_epochs)

            textgen.generate(n_results)

        print(bcolors.OKBLUE
              + '\n'
              + 'Writing results to file...'
              + '\n'
              + bcolors.END)


        # Print results in a file
        file_name = '../results/random_text_from_file_' + file_path + '.txt'
        textgen.generate_to_file(file_name, n = n_results)

        print(bcolors.OKGREEN
              + 'Results are located in file '
              + bcolors.BOLD
              + file_name
              + bcolors.END)
#------------------------------------------------------------------------------#
#==============================================================================#
