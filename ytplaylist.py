from bs4 import BeautifulSoup
from json.decoder import JSONDecoder
import requests

def FindVideoData(playlist_id: str) -> list[dict[str,str]] | None:
    url = f'https://www.youtube.com/playlist?list={playlist_id}'
    s = requests.Session()
    s.cookies.set('CONSENT', 'YES+cb.20220807-18-p0.it+FX+626')
    response = s.get(url=url)
    html = response.text.encode('utf-8', 'ignore')

    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')

    base_url = 'https://youtube.com/watch?v='
    toFind = 'var ytInitialData = '
    urls = None
    titles = None
    thumbnails = None
    for script in scripts:
        t = str(script)
        if t.find(toFind) != -1:
            t = t[t.find(toFind)+len(toFind):].removesuffix(';</script>')
            target = JSONDecoder.decode(JSONDecoder(), t)['contents']['twoColumnBrowseResultsRenderer']['tabs']
            target = target[0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
            thumbnails = [t['playlistVideoRenderer']['thumbnail']['thumbnails'][0]['url'] for t in target]
            titles = [el['playlistVideoRenderer']['title']['runs'][0]['text'] for el in target]
            urls = [el['playlistVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'].split('&list=')[0].split('watch?v=')[1] for el in target]
            break
    if urls is None or titles is None or thumbnails is None:
        return None
    return [{'base': base_url, 'title': titles[i], 'url': urls[i], 'thumbnail': thumbnails[i]} for i in range(len(titles))]