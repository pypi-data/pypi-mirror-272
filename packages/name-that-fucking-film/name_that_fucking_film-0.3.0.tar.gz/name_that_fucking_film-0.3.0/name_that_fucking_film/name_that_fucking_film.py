import os
import pathlib
import re
import sys
from collections import Counter
from random import choice

import pandas as pd
from nltk.stem import WordNetLemmatizer
from rich.console import Console

lemmatizer = WordNetLemmatizer()

console = Console(highlight=False)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


resources_path = resource_path('')


def levenshtein(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def count_same_letters(s1, s2):
    return sum(min(s1.count(c), s2.count(c)) for c in set(s1 + s2))


def read_swears_file(filepath=resources_path + "/resources/combined_file.txt"):
    with open(filepath, 'r') as file:
        return file.read().splitlines()


def get_meta_data(imdb_id, filepath=resources_path + "/resources/movie_meta_data.csv"):
    df = pd.read_csv(filepath)
    meta_data = df[df['imdbid'] == imdb_id]
    return meta_data


def get_random_filepath(directory=resources_path + "/resources/raw_texts"):
    files = os.listdir(directory)
    return os.path.join(directory, choice(files))


def count_words(file_path, swear_words):
    with open(file_path, 'r') as file:
        content = file.read().lower().split()
    content = [lemmatizer.lemmatize(word) for word in content if word.isalpha()]
    swears = {word: content.count(word) for word in swear_words}
    return Counter(swears).most_common(10)


def get_most_common_words(file_path):
    with open(file_path, 'r') as file:
        content = file.read().lower().split()
    content = [lemmatizer.lemmatize(word) for word in content if word.isalpha()]
    content = [word for word in content if
               word not in ['a', 'the', 'i', 'me', 'you', 'your', 'are', 'to', 'from', 'and', 'or', 'of', 'in',
                            'as', 'that', 'he', 'him', 'his', 'she', 'her', 'hers', 'is', 'at', 'it', 'we',
                            'us', 'they', 'them', 'on', 'with', '-', '--']]

    return Counter(content).most_common(10)


def underscore_words(title):
    return re.sub(r'[A-Za-z]', '_', title)


def guess_title(guessed_title, title):
    return guessed_title.lower() == title.lower()


def reveal_letter(underscored_title, title, letter=None):
    indices_not_revealed = [index for index, char in enumerate(underscored_title) if char == '_']
    if indices_not_revealed:
        random_index = choice(indices_not_revealed)
        character_to_reveal = letter if letter else title[random_index]
        revealed_title = ''.join([char if char.lower() == character_to_reveal.lower() else underscored_title[i]
                                  for i, char in enumerate(title)])
    else:
        revealed_title = underscored_title
    return revealed_title


def play(score):
    filepath = get_random_filepath()
    imdb_url_id = pathlib.Path(filepath).name.split('_')[-1].split('.')[0]
    imdb_id = filepath.split('/')[-1].split('.')[0].split('_')[-1]
    imdb_id = int(imdb_id)
    meta_data = get_meta_data(imdb_id)
    title = meta_data['title'].iloc[0]
    underscored_title = underscore_words(title)

    letter_reveals = 0
    straws_used = set()
    while True:
        if title.lower() == underscored_title.lower():
            console.print("Aww shucks... You didn't quite guess the title.", style="bold yellow")
            calculated_score = 0
            break
        calculated_score = score - [3 + x * 3 * len(straws_used) for x in range(0, len(straws_used))][
            -1] if straws_used else score
        calculated_score -= letter_reveals * 3
        console.print(f"\nTitle: {underscored_title}", style="green")
        guess = console.input(f"[green][Enter][/] to get random letter, "
                              f"[{'strike' if '1' in straws_used else 'green'}]1) Decade[/], "
                              f"[{'strike' if '2' in straws_used else 'green'}]2) Awards[/], "
                              f"[{'strike' if '3' in straws_used else 'green'}]3) Genre[/], "
                              f"[{'strike' if '4' in straws_used else 'green'}]4) Budget[/], "
                              f"[{'strike' if '5' in straws_used else 'green'}]5) Keywords[/], "
                              f"[{'strike' if '6' in straws_used else 'green'}]6) Taglines[/], "
                              f"[{'strike' if '7' in straws_used else 'green'}]7) Cast[/], "
                              f"[{'strike' if '8' in straws_used else 'green'}]8) Top-10 Words[/], "
                              f"[{'strike' if '9' in straws_used else 'green'}]9) Top-10 Swears[/], "
                              f"[green]0) Give up[/] or guess a letter or the whole title\n[blue](Score: {calculated_score})>[/] ")
        try:
            straws_used.add(guess) if int(guess) in list(range(0, 10)) else ""
        except ValueError:
            pass

        console.print("")
        match guess.lower():
            case "1":
                console.print("Decade of release", style="blue underline")
                console.print(str(meta_data['year'].iloc[0])[0:3] + "0")
                continue
            case "2":
                console.print("Awards received", style="blue underline")
                console.print(re.sub(r'\b \d{4}\b', '', str(meta_data['awards'].iloc[0])))
                continue
            case "3":
                console.print("Genres", style="blue underline")
                console.print(meta_data['genres'].iloc[0])
                continue
            case "4":
                console.print("Budget", style="blue underline")
                console.print(meta_data['budget'].iloc[0])
                continue
            case "5":
                console.print("Keywords", style="blue underline")
                console.print(', '.join(meta_data['keywords'].iloc[0].split(',')[:5]))
                continue
            case "6":
                console.print("Taglines", style="blue underline")
                console.print(', '.join(meta_data['taglines'].iloc[0].split(',')[:5]))
                continue
            case "7":
                console.print(', '.join(meta_data['cast'].iloc[0].split(',')[:3]))
                continue
            case "8":
                common_words = get_most_common_words(filepath)
                common_words.sort(key=lambda x: x[1], reverse=True)
                console.print("Top-10 words used:", style="blue underline")
                for word, count in common_words:
                    console.print(f"{word}: {count}")
                continue
            case "9":
                swears = count_words(filepath, read_swears_file())
                swears.sort(key=lambda x: x[1], reverse=True)
                console.print("Top-10 Naughty Words Used:", style="blue underline")
                for word, count in swears:
                    if count > 0:
                        console.print(f"{word}: {count}")
                continue
            case "0":
                score = 0
                break
            case "":
                before = underscored_title + ''
                underscored_title = reveal_letter(underscored_title, title)
                letter = ''.join(set(underscored_title.upper()) - set(before.upper()))
                console.print(f"Revealed letter [green]{letter}[/]", style="blue")
                letter_reveals += 1
                continue
            case _ if len(guess) == 1:
                before = underscored_title + ''
                underscored_title = reveal_letter(underscored_title, title, guess)
                if before == underscored_title:
                    letter_reveals += 1
                    console.print(f"No letter [green]{guess.upper()}[/] found.", style="yellow")
                else:
                    console.print(f"Revealing letter [green]{guess.upper()}[/] in the title...", style="blue")
                continue

        if guess_title(guess, title):
            console.print("Congratulations! You guessed the title correctly!", style="bold green")
            break

        console.print(f"Your guess is {levenshtein(guess.lower(), title.lower())} changes off.", style="blue")
        console.print(f"You have {count_same_letters(guess.lower(), title.lower())} of the correct letters.",
                      style="blue")

        # underscored_title = reveal_letters(underscored_title, title)
    console.print(f"\n[blue underline]Title:[/] '{title}' ({meta_data['year'].iloc[0]})", style="italic")
    console.print(f"[blue underline]IMDb Link:[/] https://www.imdb.com/title/tt{imdb_url_id}/", style="italic")
    console.print(f"[blue underline]Genres:[/] {meta_data['genres'].iloc[0]}", style="italic")
    console.print(f"[blue underline]Budget:[/] {meta_data['budget'].iloc[0]}", style="italic")
    console.print(f"[blue underline]Awards:[/] {meta_data['awards'].iloc[0]}", style="italic")
    console.print(f"[blue underline]IMDb User Rating:[/] {meta_data['imdb user rating'].iloc[0]}", style="italic")
    console.print(f"\n[blue underline]Taglines:[/]\n{meta_data['taglines'].iloc[0]}", style="italic")
    console.print(f"\n[blue underline]Plot:[/]\n{meta_data['plot'].iloc[0]}", style="italic")
    console.print(f"\n[blue underline]Cast:[/]\n{meta_data['cast'].iloc[0]}", style="italic")
    return calculated_score


def main():
    console.clear()
    start_score = 100
    while True:
        score = play(start_score)
        console.print(f"\nYou scored [blue]{score}[/] points!", style="green")
        user_input = console.input("\n[bold green]Press [ENTER] to continue or q to quit...[/]")
        if user_input.lower() == "q":
            break
        console.clear()


if __name__ == "__main__":
    main()
