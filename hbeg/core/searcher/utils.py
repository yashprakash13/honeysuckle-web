
def get_clean_genres(genres):
    """to return comman separated string of genres 

    Args:
        genres ([string]): genres to remove ! from

    Returns:
        [string]: string with , separated genres
    """
    genre_list = genres.split('!')
    return ', '.join(genre_list)