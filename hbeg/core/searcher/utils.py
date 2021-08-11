import re


def get_clean_genres(genres):
    """to return comman separated string of genres

    Args:
        genres ([string]): genres to remove ! from

    Returns:
        [string]: string with , separated genres
    """
    try:
        genre_list = genres.split("!")
        return ", ".join(genre_list)
    except Exception as e:
        print("Exception in get clean genres: ", e)
        return None


def find_pair(pair_found):
    """
    return the pair found from string of characters passed
    """

    if "Harry P." in pair_found and "Hermione G." in pair_found:
        return "Harmony"
    elif "Harry P." in pair_found and "Daphne G." in pair_found:
        return "Haphne"
    elif "James P." in pair_found and "Lily Evans P." in pair_found:
        return "Jily"
    elif "Draco M." in pair_found and "Hermione G." in pair_found:
        return "Dramione"
    elif "Sirius B." in pair_found and "Hermione G." in pair_found:
        return "Sirimione"
    elif "James P." in pair_found and "Hermione G." in pair_found:
        return "Jamione"
    elif "Remus L." in pair_found and "Hermione G." in pair_found:
        return "Remione"
    elif "Severus S." in pair_found and "Hermione G." in pair_found:
        return "Snamione"
    elif "Tom R. Jr." in pair_found and "Hermione G." in pair_found:
        return "Tomione"
    elif "Voldemort" in pair_found and "Hermione G." in pair_found:
        return "Volmione"
    elif "Harry P." in pair_found and "Draco M." in pair_found:
        return "Drarry"
    elif "Harry P." in pair_found and "Tom R. Jr." in pair_found:
        return "Tomarry"
    elif "Harry P." in pair_found and "Severus S." in pair_found:
        return "Snarry"
    elif "Harry P." in pair_found and "Draco M." in pair_found and "Hermione G." in pair_found:
        return "Dramionarry"
    else:
        return "OtherPair"


def find_set_pairings(chars_str):
    """
    return pairing "Pairs" column value for characters got in chars_str
    """

    pairs_found = re.findall(r"\[(.*?)\]", str(chars_str)[1:-1])
    if len(pairs_found) == 1:
        return find_pair(pairs_found[0])
    elif len(pairs_found) == 2:
        return find_pair(pairs_found[0]) + "!" + find_pair(pairs_found[1])
    else:
        return "NoPairs"


def make_length(words):
    """
    to return length from num words
    """
    words = int(words)
    if words <= 50000:
        return "Small"
    elif words <= 100000 and words >= 50000:
        return "Medium"
    elif words <= 200000 and words >= 100000:
        return "Long"
    else:
        return "VeryLong"
