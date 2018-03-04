#qpy:qpyapp

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import androidhelper 


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


if __name__ == '__main__':
    # create droid object
    droid = androidhelper.Android()

    # get
    raw_html = simple_get('https://reserve.dlt.go.th/reserve/s.php?confirm=1')
    # parse
    html = BeautifulSoup(raw_html, 'html.parser')
    # get current plate no. set
    for i, s in zip(html.select('input'), html.select('span')):
        cartype = i['value'].split()[-1]
        plateset = s.text
        if 'รถเก๋ง' in cartype:
            print(cartype,  plateset)
            break

    
    html = BeautifulSoup(raw_html, 'html.parser')
    for c in html.select('center'):
        if 'ปิดระบบจองเลข' in c:
            print('System is unavailable now')
            droid.notify(c.text, 'System is unavailable now')
        else:
            for i, s in zip(c.select('input'), c.select('span')):
                cartype = i['value'].split()[-1]
                plateset = s.text
                if 'รถเก๋ง' in cartype:
                    print(cartype,  plateset)
                    droid.notify(cartype, plateset)
                    break

    

    
    
