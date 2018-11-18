#brought to you by nananananate



import urllib.parse
import urllib.request
import urllib.error
import json
import sys
import ssl
import time
import traceback
import urllib
import requests


class TestError(Exception):
    pass



GOOGLE_API_KEY = 'key' #nate
BASE_GOOGLE_URL = 'https://www.googleapis.com/plus/v1/people/'


GOOGLE_SEARCH_API_KEY = 'key' # pie
BASE_SPECIFIC_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1/siterestrict?key='

YOUTUBE_V3_API_KEY = 'key'
BASE_YOUTUBE_V3_URL = 'https://www.googleapis.com/youtube/v3/activities?part=snippet%2CcontentDetails&channelId='
BASE_STREAM_URL = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId='

CONTEXTUAL_SEARCH_URL = 'https://contextualwebsearch.com/api/Search/WebSearchAPI?q='

GOOGLE_SHEETS_API_KEY = 'key'
BASE_SHEETS_URL = 'https://sheets.googleapis.com/v4/spreadsheets/'

TUMBLR_API_KEY = 'key'
BASE_TUMBLR_URL = 'https://api.tumblr.com/v2/blog/'

PASTEBIN_API_KEY = 'ket'
PASTEE_API_KEY = 'uDfdGtXcRb2FIT46ijYQI0Qm7BLjYcOdRj5h1SJhl'

def build_youtube_url(userid: str) -> str:
    return BASE_YOUTUBE_V3_URL + userid + '&key=' + YOUTUBE_V3_API_KEY


def build_google_url(userid: int) -> str:  #change the name
    '''Builds url for elevation API '''
    return BASE_GOOGLE_URL + str(userid) + '/activities' + '/public?' + 'key=' + GOOGLE_API_KEY


def build_sheets_url(sheetid: str, sheet_range: 'A1:A1 FORMAT'):
    '''Needs range'''
    return BASE_SHEETS_URL + sheetid + '/values/' + sheet_range  + '?key=' + GOOGLE_SHEETS_API_KEY



def build_stream_url(userid: str) -> str:
    return BASE_STREAM_URL + userid + '&type=video&eventType=live&key=' + YOUTUBE_V3_API_KEY


def build_specific_search_url(s_id: str, query: str):
    query = urllib.parse.quote_plus(query)
    return '{}{}&cx={}&q={}'.format(BASE_SPECIFIC_SEARCH_URL, GOOGLE_SEARCH_API_KEY, s_id, query)

def build_contextual_search_url(query: str):
    query = urllib.parse.quote_plus(query)
    end = '&count=22&autoCorrect=true&safeSearch=true'
    return CONTEXTUAL_SEARCH_URL + query + end


def build_tumblr_url(userid: str):
    return BASE_TUMBLR_URL + userid + '/posts?api_key=' + TUMBLR_API_KEY


def pastebin_paste(content):
    try:
        pastebin_vars = {'api_dev_key':PASTEBIN_API_KEY,'api_option':'paste','api_paste_code': content}
        result = requests.post('https://pastebin.com/api/api_post.php', data = pastebin_vars)
        url = result.text
        return url

    except:
        traceback.print_exc()
        return 'Unable to paste'

def pastee(content):
    try:
        headers = {'X-Auth-Token': PASTEE_API_KEY}
        params = {"sections":[{"name":"robot-nate","syntax":"autodetect","contents": content}]}
        post = requests.post("https://api.paste.ee/v1/pastes", json=params, headers = headers)
        print(post)
        return post.json()["link"]
    except:
        traceback.print_exc()
        return 'Unable to paste'





def get_json(url: str) -> dict:
    '''Returns content of given url as a dict (JSON)'''
    response = None

    flag = True


    try:
        #print(url)
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(url, context=context)
        json_text = json.loads(response.read().decode(encoding = 'utf-8'))


        if json_text == None:
            print('shit')

        flag = False

        return json_text

    except:
        print('oh no')
        #time.sleep(3)

    finally:
        if response != None:
            response.close()
