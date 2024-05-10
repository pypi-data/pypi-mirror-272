# Name That Fucking Film

A Python-based command-line game that challenges players to guess movie titles based on limited information and strategically revealed letters.

## Description

"Name That Fucking Film" is a command-line game where players attempt to guess the title of a movie from a scrambled or obscured representation. The game pulls movie metadata from a locally stored dataset, giving hints and revealing letters upon request or as part of the gameplay mechanics.

## Features

- **Movie Hints**: Receive hints about the movie's decade, awards, genre, and budget.
- **Letter Reveal**: Opt to reveal a letter in the movie title to help with your guess.
- **Score Tracking**: Keep track of your score, which changes based on the number of hints and guesses.
- **Rich Formatting**: Utilizes the `rich` Python library to enhance the CLI experience with stylized text output.

## Installation

Before you can run the game, you need to install the necessary Python dependencies:

```bash
# Clone the repository
git clone https://github.com/jkarenko/name-that-fucking-film.git
cd name-that-fucking-film

# Install dependencies using Poetry
poetry install

# run
poetry run python name_that_fucking_film/main.py {path_to_dir_containing_resources}
```

Or using PIP
```bash
# Install from PyPI
pip install name-that-fucking-film

# Run
name-that-fucking-film {path_to_dir_containing_resources}
```

Download [resources.zip](https://www.dropbox.com/scl/fi/3p4r5drnp8s79lz7fmt8k/resources.zip?rlkey=hnubde0f9jadzthscimz2nx5b&st=54mjk0kb&dl=0) and unzip it somewhere convenient (e.g. `c:\name-that-fucking-film` or `~/name-that-fucking-film`)

Zip file contains excerpts from https://www.kaggle.com/datasets/gufukuro/movie-scripts-corpus
and https://github.com/chucknorris-io/swear-words/tree/master

