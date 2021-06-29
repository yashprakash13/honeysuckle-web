from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from core.searcher.constants import ALL_DF_COLUMNS, MAIN_EN_DATA_PATH
from core.searcher import utils

"""
THE ENTIRE LOGIC OF EXTRACTING DESIRED STORY DETAILS FROM URL
"""

def save_new_story_into_csvdb(inst, story):
    """
    save the new story into csv db with inst obj of search engine
    """
    storytosave = {}
    for key in story:
        if key in ALL_DF_COLUMNS:
            storytosave[key] = str(story[key])
    storytosave['Pairs'] = utils.find_set_pairings(story['characters'])
    storytosave['Lengths'] = utils.make_length(story['num_words'])

    if storytosave['language'] == 'English':
        print(pd.DataFrame(storytosave, index=[0]))
        df = inst.class_indices.df
        df = df.append(storytosave, ignore_index=True)
        df.to_csv(MAIN_EN_DATA_PATH, index=False)
        print('New story saved into CSV db.')
    else:
        # TODO: do it
        print("Can't save a non-English story yet." )




def get_story_dates_cleaned(datestr, updated = False):
    """
    to get published and updated dates from csv db into the format like: 2 June, 2021 or3 hours ago, so on.
    """

    datetimeFormat = '%m/%d/%Y'
    if not updated:
        story_date = datetime.strptime(str(datestr), datetimeFormat)
        story_date = story_date.strftime(r'%-d %b, %Y')
        return story_date
    else:
        story_date_raw = datetime.strptime(str(datestr), datetimeFormat)
        story_date = story_date_raw.strftime(r'%-d %b, %Y')
        curr_time = datetime.now()
        diff_in_time = relativedelta(curr_time, story_date_raw)

        # only amend hours & minutes diff
        if diff_in_time.days:
            'This week'

        elif diff_in_time.hours:
            if diff_in_time.hours == 1:
                story_date = str(diff_in_time.hours)+" hour ago"
            else:
                story_date = str(diff_in_time.hours)+" hours ago"

        elif diff_in_time.minutes:
            if diff_in_time.minutes == 1:
                story_date = str(diff_in_time.minutes)+" minute ago"
            else:
                story_date = str(diff_in_time.minutes)+" minutes ago"
        return story_date



def get_story_updation_cleaned(story_last_up, _type):
    """
    to get updated date from scraped webpage into the format like: 2 June, 2021 or 3 hours ago, so on.
    """

    curr_time = datetime.now()
    if _type == 1:  # ffn last updated
        datetimeFormat = '%Y-%m-%d %H:%M:%S'
        story_last_up = datetime.strptime(
            str(story_last_up), datetimeFormat)
        story_last_updated = story_last_up.strftime(r'%-d %b, %Y ')
        story_last_updated_to_store = story_last_up.strftime('%m/%d/%Y %H:%M:%S')

    elif _type == 2:  # ao3 last updated
        datetimeFormat = '%Y-%m-%d'
        story_last_up = datetime.strptime(
            str(story_last_up), datetimeFormat)
        story_last_updated = story_last_up.strftime(r'%-d %b, %Y ')
        story_last_updated_to_store = story_last_up.strftime('%m/%d/%Y')

    diff_in_time = relativedelta(curr_time, story_last_up)

    # only amend hours & minutes diff
    if diff_in_time.years:
        pass

    elif diff_in_time.months:
        pass

    elif diff_in_time.days:
        pass

    elif diff_in_time.hours:
        if diff_in_time.hours == 1:
            story_last_updated = str(diff_in_time.hours)+" hour ago"
        else:
            story_last_updated = str(diff_in_time.hours)+" hours ago"

    elif diff_in_time.minutes:
        if diff_in_time.minutes == 1:
            story_last_updated = str(diff_in_time.minutes)+" minute ago"
        else:
            story_last_updated = str(diff_in_time.minutes)+" minutes ago"

    return str(story_last_updated), str(story_last_updated_to_store)




def get_genres(genre_text):
    """
    to get genres in ! separated format
    """
    if genre_text.startswith('Chapters'):
        return [None]
    genres = genre_text.split('/')
    # Hurt/Comfort is annoying because of the '/'
    corrected_genres = []
    for genre in genres:
        if genre == 'Hurt':
            corrected_genres.append('Hurt/Comfort')
        elif genre == 'Comfort':
            continue
        else:
            corrected_genres.append(genre)
    
    genres_string = '!'.join(corrected_genres)
    return genres_string



def get_characters_from_string(string):
    """
    to get characters in [['c1', 'c2'], 'c3', 'c4'] format
    """
    if not string:
        return ''
    stripped = string.strip()
    if stripped.find('[') == -1:
        return stripped.split(', ')
    else:
        characters = []
        num_pairings = stripped.count('[')
        for idx in range(0, num_pairings):
            open_bracket = stripped.find('[')
            close_bracket = stripped.find(']')
            characters.append(get_characters_from_string(stripped[open_bracket+1:close_bracket]))
            stripped = stripped[close_bracket+1:]
        if stripped != '':
            singles = get_characters_from_string(stripped)
            [characters.append(character) for character in singles]
        
        return characters




def get_story_details_from_reponse(story_id, response):
    """
    for scraping all story metadata from response text passed
    """

    ffn_soup = BeautifulSoup(response.content, 'html.parser')

    try:
        ffn_story_name = ffn_soup.find_all('b', 'xcontrast_txt')[
            0].string.strip()

    except :
        pass

    ffn_story_id = int(story_id)

    ffn_author_name = ffn_soup.find_all(
        'a', {'href': re.compile(r'^/u/\d+/.')})[0].string.strip()

    ffn_author_url = (ffn_soup.find(
        'div', attrs={'id': 'profile_top'}).find('a', href=True))['href']

    ffn_author_id = (
        re.search(r"\d+", ffn_author_url)).group(0)

    try:
        ffn_story_summary = ffn_soup.find_all('div', {
            'style': 'margin-top:2px',
            'class': 'xcontrast_txt'})[0].string.strip()

    except :
        pass

    ffn_story_fandom = ffn_soup.find(
        'span', attrs={'class': 'lc-left'}).find(
        'a', attrs={'class': 'xcontrast_txt'}).text

    try:
        ffn_story_image = (ffn_soup.find(
            'div', attrs={'id': 'profile_top'}).find(
            'img', attrs={'class': 'cimage'}))['src']

    except :
        pass

    # if the fandom isnt crossover, then go to the next <a>
    if not re.search(r"\bcrossover\b", ffn_story_fandom, re.IGNORECASE):
        ffn_story_fandom = ffn_soup.find(
            'span', attrs={'class': 'lc-left'}).find(
            'a', attrs={'class': 'xcontrast_txt'}).findNext('a').text

    details = ffn_soup.find_all(
        'span', {'class': 'xgray xcontrast_txt'}
    )[0].text.split(' - ')

    dates = [date for date in ffn_soup.find_all(
        'span') if date.has_attr('data-xutime')]

    for i in range(0, len(details)):

        if details[i].startswith('Updated:'):

            ffn_story_status = "Updated"

            ffn_story_last_updated = datetime.fromtimestamp(
                int(dates[0]['data-xutime']))

            ffn_story_published = datetime.fromtimestamp(
                int(dates[1]['data-xutime']))  # Published date

            # change formatting
            ffn_story_published = datetime.strptime(
                str(ffn_story_published), '%Y-%m-%d %H:%M:%S')
            
            ffn_story_published_to_store = datetime.strptime(
                str(ffn_story_published), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %H:%M:%S')

            ffn_story_published = ffn_story_published.strftime(
                r'%-d %b, %Y')

            break  # if found, exit the loop to prevent overwriting of the variable

        elif details[i].startswith('Published:'):

            ffn_story_status = "Complete"

            # if Updated not found, pub & last_up will be same
            ffn_story_last_updated = str(datetime.fromtimestamp(
                int(dates[0]['data-xutime'])))  # Published date

            ffn_story_published = str(datetime.fromtimestamp(
                int(dates[0]['data-xutime'])))  # Published dat

            # change formatting
            ffn_story_published = datetime.strptime(
                str(ffn_story_published), '%Y-%m-%d %H:%M:%S')
            
            ffn_story_published_to_store = datetime.strptime(
                str(ffn_story_published), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %H:%M:%S')


            ffn_story_published = ffn_story_published.strftime(
                r'%-d %b, %Y')

    for i in range(0, len(details)):

        if details[i].startswith('Reviews:'):

            ffn_story_reviews = details[i].replace(
                'Reviews:', '').strip()
            ffn_story_reviews_to_store = int(ffn_story_reviews.replace(',', ''))

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
            ffn_story_reviews = ''
            ffn_story_reviews_to_store = ''

    for i in range(0, len(details)):
        if details[i].startswith('Favs:'):

            ffn_story_favs = details[i].replace(
                'Favs:', '').strip()
            ffn_story_favs_to_store = int(ffn_story_favs.replace(',', ''))

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
            ffn_story_favs = ''
            ffn_story_favs_to_store = ''

    for i in range(0, len(details)):
        if details[i].startswith('Follows:'):

            ffn_story_follows = details[i].replace(
                'Follows:', '').strip()
            ffn_story_follows_to_store = int(ffn_story_follows.replace(',', ''))

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
             ffn_story_follows = ''
             ffn_story_follows_to_store = ''

    for i in range(0, len( details)):
        if  details[i].startswith('Rated:'):

            ffn_story_rating =  details[i].replace(
                'Rated:', '').strip()
            ffn_story_rating = ffn_story_rating[ffn_story_rating.index('Fiction ')+len('Fiction '):]

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
             ffn_story_rating = ''

    ffn_story_lang =  details[1]
    ffn_story_genre =  details[2]
    ffn_story_characters =  details[3]

    if re.search(r'\d', str( ffn_story_genre)) is not None:
         ffn_story_genre = None
        
    ffn_story_genre_to_store = get_genres(ffn_story_genre)

    if re.search(r'\d', str( ffn_story_characters)):
         ffn_story_characters = None
    
    ffn_story_characters_to_store = get_characters_from_string(ffn_story_characters)

    ffn_story_metainfo = ''
    for i in range(0, len( details)):
        if  details[i].startswith('Reviews'):
             ffn_story_metainfo +=  details[i].replace(
                'Reviews:', '**Reviews:**').strip()
             ffn_story_metainfo += " ☘︎ "

        if  details[i].startswith('Favs'):
             ffn_story_metainfo +=  details[i].replace(
                'Favs:', '**Favs:**').strip()
             ffn_story_metainfo += " ☘︎ "

        if  details[i].startswith('Follows'):
             ffn_story_metainfo +=  details[i].replace(
                'Follows:', '**Follows:**').strip()

    search = [x for x in details if x.startswith("Words:")]
    if len(search) == 0:
        ffn_story_length = 0
    else:
        ffn_story_length = int(
            search[0][len("Words:"):].replace(',', ''))
        ffn_story_length_to_store = ffn_story_length

        ffn_story_length = "{:,}".format(
            int(ffn_story_length))

    search = [x for x in details if x.startswith("Chapters:")]
    if len(search) == 0:
        ffn_story_chapters = 1  # 1 as the default chapter number
    else:
        ffn_story_chapters = str(
            int(search[0][len("Chapters:"):].replace(',', ''))).strip()

    ffn_author_url = "https://www.fanfiction.net" + ffn_author_url

    ffn_story_last_updated, ffn_story_last_updated_to_store = get_story_updation_cleaned(
        ffn_story_last_updated, 1)

    if ffn_story_status == "Updated":
        ffn_story_status = "Incomplete"

    try:
        if  not ffn_story_image:
            ffn_story_image = ''
    except:
        ffn_story_image = ''

    story = {
        'title': ffn_story_name,
        'num_words': ffn_story_length,
        'num_words_to_store':ffn_story_length_to_store,
        'author_name':ffn_author_name,
        'status' : ffn_story_status,
        'rated': ffn_story_rating,
        'num_chapters':ffn_story_chapters,
        'genres':ffn_story_genre,
        'genres_to_store':ffn_story_genre_to_store,
        'characters':ffn_story_characters,
        'characters_to_store':ffn_story_characters_to_store,
        'summary':ffn_story_summary,
        'author_id':ffn_author_id,
        'language':ffn_story_lang,
        'published':ffn_story_published,
        'published_to_store':ffn_story_published_to_store[:10],
        'updated':ffn_story_last_updated,
        'updated_to_store': ffn_story_last_updated_to_store[:10],
        'num_favs':ffn_story_favs,
        'num_favs_to_store':ffn_story_favs_to_store,
        'num_reviews': ffn_story_reviews,
        'num_reviews_to_store': ffn_story_reviews_to_store,
        'num_follows':ffn_story_follows,
        'num_follows_to_store':ffn_story_follows_to_store,
        'story_image':ffn_story_image
    }
    return story



