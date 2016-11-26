from rpc import RPC
from xbmcswift2 import Plugin
import re
import requests
import xbmc,xbmcaddon,xbmcvfs,xbmcgui
import xbmcplugin
import base64
import random
#from HTMLParser import HTMLParser
import urllib
import sqlite3
import time,datetime
import threading
import HTMLParser

import SimpleDownloader as downloader


plugin = Plugin()
big_list_view = False

if plugin.get_setting('english') == 'true':
    headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept-Language' : 'en-GB,en;q=0.5',
    }
else:
    headers={}

def addon_id():
    return xbmcaddon.Addon().getAddonInfo('id')

def log(v):
    xbmc.log(repr(v))

#log(sys.argv)

def get_icon_path(icon_name):
    if plugin.get_setting('user.icons') == "true":
        user_icon = "special://profile/addon_data/%s/icons/%s.png" % (addon_id(),icon_name)
        if xbmcvfs.exists(user_icon):
            return user_icon
    return "special://home/addons/%s/resources/img/%s.png" % (addon_id(),icon_name)

def remove_formatting(label):
    label = re.sub(r"\[/?[BI]\]",'',label)
    label = re.sub(r"\[/?COLOR.*?\]",'',label)
    return label

def escape( str ):
    str = str.replace("&", "&amp;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    str = str.replace("\"", "&quot;")
    return str

def unescape( str ):
    str = str.replace("&lt;","<")
    str = str.replace("&gt;",">")
    str = str.replace("&quot;","\"")
    str = str.replace("&amp;","&")
    return str

@plugin.route('/download/<name>/<url>')
def download(name,url):
    downloads = plugin.get_storage('downloads')
    downloads[name] = url
    dl = downloader.SimpleDownloader()
    params = { "url": url, "download_path": plugin.get_setting('download') }
    dl.download(name, params)

@plugin.route('/stop_downloads')
def stop_downloads():
    downloads = plugin.get_storage('downloads')
    dl = downloader.SimpleDownloader()
    dl._stopCurrentDownload()
    #log(dl._getQueue())
    for name in downloads.keys():
        dl._removeItemFromQueue(name)
        del downloads[name]

@plugin.route('/start_downloads')
def start_downloads():
    dl = downloader.SimpleDownloader()
    dl._processQueue()

@plugin.route('/play/<url>')
def play(url):
    xbmc.executebuiltin('PlayMedia("%s")' % url)

@plugin.route('/execute/<url>')
def execute(url):
    xbmc.executebuiltin(url)
    
@plugin.route('/title_page/<url>')
def title_page(url):
    r = requests.get(url, headers=headers)
    html = r.text
    html = HTMLParser.HTMLParser().unescape(html)

    lister_items = html.split('<div class="lister-item ')
    items = []
    for lister_item in lister_items:
        if not re.search(r'^mode-advanced">',lister_item):
            continue
        title_type = ''
        #loadlate="http://ia.media-imdb.com/images/M/MV5BMjIyMTg5MTg4OV5BMl5BanBnXkFtZTgwMzkzMjY5NzE@._V1_UX67_CR0,0,67,98_AL_.jpg"
        img_url = ''
        img_match = re.search(r'<img.*?loadlate="(.*?)"', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if img_match:
            img = img_match.group(1)
            img_url = re.sub(r'U[XY].*_.jpg','SX344_.jpg',img) #NOTE 344 is Confluence List View width

        title = ''
        imdbID = ''
        year = ''
        #<a href="/title/tt1985949/?ref_=adv_li_tt"\n>Angry Birds</a>
        title_match = re.search(r'<a href="/title/(tt[0-9]*)/\?ref_=adv_li_tt".>(.*?)</a>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            imdbID = title_match.group(1)
            title = title_match.group(2)

        #<span class="lister-lister_item-year text-muted unbold">(2016)</span>
        title_match = re.search(r'<span class="lister-lister_item-year text-muted unbold">.*?\(([0-9]*?)\)<\/span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            year = title_match.group(1)
            title_type = "movie"


        #Episode:</small>\n    <a href="/title/tt4480392/?ref_=adv_li_tt"\n>\'Cue Detective</a>\n    <span class="lister-lister_item-year text-muted unbold">(2015)</span>
        #Episode:</small>\n    <a href="/title/tt4952864/?ref_=adv_li_tt"\n>#TeamLucifer</a>\n    <span class="lister-lister_item-year text-muted unbold">(2016)</span
        episode = ''
        episode_id = ''
        episode_match = re.search(r'Episode:</small>\n    <a href="/title/(tt.*?)/?ref_=adv_li_tt"\n>(.*?)</a>\n    <span class="lister-lister_item-year text-muted unbold">\((.*?)\)</span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if episode_match:
            episode_id = episode_match.group(1)
            episode = "%s (%s)" % (episode_match.group(2), episode_match.group(3))
            year = episode_match.group(3)
            title_type = "tv_episode"

        #Users rated this 6.1/10 (65,165 votes)
        rating = ''
        votes = ''
        rating_match = re.search(r'title="Users rated this (.+?)/10 \((.+?) votes\)', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if rating_match:
            rating = rating_match.group(1)
            votes = rating_match.group(2)
            votes = re.sub(',','',votes)

        #<p class="text-muted">\nRusty Griswold takes his own family on a road trip to "Walley World" in order to spice things up with his wife and reconnect with his sons.</p>
        plot = ''
        plot_match = re.search(r'<p class="text-muted">(.+?)</p>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if plot_match:
            plot = plot_match.group(1).strip()

        #Stars:\n<a href="/name/nm0255124/?ref_=adv_li_st_0"\n>Tom Ellis</a>, \n<a href="/name/nm0314514/?ref_=adv_li_st_1"\n>Lauren German</a>, \n<a href="/name/nm1204760/?ref_=adv_li_st_2"\n>Kevin Alejandro</a>, \n<a href="/name/nm0940851/?ref_=adv_li_st_3"\n>D.B. Woodside</a>\n    </p>
        cast = []
        cast_match = re.search(r'<p class="">(.*?)</p>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if cast_match:
            cast = cast_match.group(1)
            cast_list = re.findall(r'<a.+?>(.+?)</a>', cast, flags=(re.DOTALL | re.MULTILINE))
            cast = cast_list


        #<span class="genre">\nAdventure, Comedy            </span>
        genres = ''
        genre_match = re.search(r'<span class="genre">(.+?)</span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if genre_match:
            genres = genre_match.group(1).strip()
            #genre_list = re.findall(r'<a.+?>(.+?)</a>', genre)
            #genres = ",".join(genre_list)

        #class="runtime">99 min</span>
        runtime = ''
        runtime_match = re.search(r'class="runtime">(.+?) min</span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if runtime_match:
            runtime = int(runtime_match.group(1)) * 60

        sort = ''
        #sort_match = re.search(r'<span class="sort"><span title="(.+?)"', lister_item, flags=(re.DOTALL | re.MULTILINE))
        #if sort_match:
        #    sort = sort_match.group(1)

        #<span class="certificate">PG</span>
        certificate = ''
        certificate_match = re.search(r'<span class="certificate">(.*?)</span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if certificate_match:
            certificate = certificate_match.group(1)
            
        if imdbID:
            id = imdbID
            if title_type == "tv_series" or title_type == "mini_series":
                meta_url = "plugin://plugin.video.meta/tv/search_term/%s/1" % urllib.quote_plus(title.encode("utf8"))
            elif title_type == "tv_episode":
                vlabel = "%s - %s" % (title, episode)
                vlabel = urllib.quote_plus(vlabel.encode("utf8"))
                meta_url = "plugin://plugin.video.imdbsearch/?action=episode&imdb_id=%s&episode_id=%s&title=%s" % (imdbID,episode_id,vlabel)
                id = episode_id
            else:
                meta_url = 'plugin://plugin.video.meta/movies/play/imdb/%s/select' % imdbID            

        if imdbID:
            items.append(
            {
                'label': title,
                'path': meta_url,
                'thumbnail':img_url,

            })


    #href="?count=100&sort=moviemeter,asc&production_status=released&languages=en&release_date=2015,2016&user_rating=6.0,10.0&start=1&num_votes=100,&title_type=feature&page=2&ref_=adv_nxt"
    pagination_match = re.search('<a href="([^"]*?&ref_=adv_nxt)"', html, flags=(re.DOTALL | re.MULTILINE))
    if pagination_match:
        next_page = 'http://www.imdb.com/search/title?'+pagination_match.group(1)
        items.append(
        {
            'label': "[COLOR orange]Next Page >>[/COLOR]",
            'path': plugin.url_for('title_page', url=next_page),
            'thumbnail': 'DefaultNetwork.png',
        })        

    return items

    
@plugin.route('/feature')
def feature():
    url = 'http://www.imdb.com/search/title?count=100&production_status=released&title_type=feature'    
    return title_page(url)
    
    
@plugin.route('/tv_movie')
def tv_movie():
    url = 'http://www.imdb.com/search/title?count=100&production_status=released&title_type=tv_movie'    
    return title_page(url)

@plugin.route('/add_search')
def add_search():
    searches = plugin.get_storage('searches')    
    d = xbmcgui.Dialog()
    name = d.input("Name")
    if not name:
        return
    url = d.input("URL",'http://www.imdb.com/search/title?count=100&production_status=released&title_type=feature')
    if not url:
        return
    searches[name] = url
    
@plugin.route('/edit_search/<name>')
def edit_search(name):
    searches = plugin.get_storage('searches')  
    url = searches[name]
    #http://www.imdb.com/search/title?certificates=us:g,us:pg&count=100&countries=at,be&genres=action,adventure&groups=top_100,top_250&languages=hr,nl&num_votes=1,2&production_status=released&title=xx&title_type=feature,tv_movie&user_rating=2.1,9.9
    fields = ["certificates", "count", "countries", "genres", "groups", "languages", "num_votes", "production_status", "release_date", "title", "title_type", "user_rating"]
    params = dict((key, '') for key in fields)
    if '?' in url:
        head,tail = url.split('?',1)
        key_values = tail.split('&')
        for key_value in key_values:
            if '=' in key_value:
                key,value = key_value.split('=')
                params[key] = value
    else:
        head = url
    d = xbmcgui.Dialog()
    while True:
        actions = ["%s=%s" % (x,params.get(x,'')) for x in fields]
        #action = d.select(name,["Name: "+name,"Title","Type","Date","Rating","Votes","Genres","Groups","Certificates","Countries","Languages","Locations","Popularity","Plot","Status","Cast/Crew","Runtime","Sort"])
        action = d.select(name,actions)
        if action < 0:
            return
            
        elif action == 9:
            title = params.get('title','')
            title = d.input("Title",title)
            if title:
                params['title'] = title
            else:
                if 'title' in params:
                    del params['title']
        elif action == 10:
            title_type = params.get('title_type','')
            if title_type:
                current_types = title_type.split(',') #TODO preselect in Krypton
            types = ['feature','tv_movie','tv_series','tv_episode','tv_special','mini_series','documentary','game','short','video']
            which = d.multiselect('Title Types',types)
            if which:
                title_types = [types[x] for x in which]
                params['title_type'] = ",".join(title_types)
            else:
                if 'title_type' in params:
                    del params['title_type']
        elif action == 8:
            date = params.get('release_date','')
            start = ''
            end = ''
            if date:
                start,end= date.split(',')
            which = d.select('Release Date',['Start','End'])
            if which == 0:
                start = d.input("Start",start)
            elif which == 1:
                end = d.input("Start",end)
            if start or end:
                params['release_date'] = ",".join([start,end])
            else:
                if 'release_date' in params:
                    del params['release_date']
                    
        params = {k: v for k, v in params.items() if v}    
        kv = ["%s=%s" % (x,params[x]) for x in params]
        tail = '&'.join(kv)
        url = head+"?"+tail
        log(url)
        searches[name] = url 
        xbmc.executebuiltin('Container.Refresh')
    
@plugin.route('/')
def index():
    searches = plugin.get_storage('searches')
    items = []
    for search in searches:
        context_items = []
        context_items.append(('[COLOR yellow]Edit[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('edit_search', name=search))))    
        items.append(
        {
            'label': search,
            'path': plugin.url_for('title_page',url=searches[search]),
            'thumbnail':get_icon_path('search'),
            'context_menu': context_items,
        })
    
    items.append(
    {
        'label': "Add Search",
        'path': plugin.url_for('add_search'),
        'thumbnail':get_icon_path('settings'),

    })    
    
    items.append(
    {
        'label': "Feature Movies",
        'path': plugin.url_for('feature'),
        'thumbnail':get_icon_path('movies'),

    })
    items.append(
    {
        'label': "TV Movies",
        'path': plugin.url_for('tv_movie'),
        'thumbnail':get_icon_path('movies'),

    })
    return items



if __name__ == '__main__':

    plugin.run()
    if big_list_view == True:
        #view_mode = int(plugin.get_setting('view_mode'))
        #plugin.set_view_mode(view_mode)
        plugin.set_view_mode(518)
    plugin.set_content("movies")