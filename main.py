from rpc import RPC
from xbmcswift2 import Plugin
from xbmcswift2 import actions
from xbmcswift2 import ListItem
import re
import requests
import xbmc,xbmcaddon,xbmcvfs,xbmcgui,xbmcvfs,xbmcplugin
import xbmcplugin
import base64
import random
#from HTMLParser import HTMLParser
import urllib
import sqlite3
import time,datetime
import threading
import HTMLParser
import json
import sys

import SimpleDownloader as downloader


plugin = Plugin()
big_list_view = False

if plugin.get_setting('english') == 'true':
    headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept-Language' : 'en-US,en;q=0.5',
    "X-Forwarded-For": "54.239.17.118"}
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
    global big_list_view
    big_list_view = True
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
        #title_match = re.search(r'<span class="lister-lister_item-year text-muted unbold">.*?\(([0-9]*?)\)<\/span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        title_match = re.search(r'<span class="lister-item-year text-muted unbold">.*?\(([0-9]{4})\)<\/span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            year = title_match.group(1)
            title_type = "movie"
            log(year)
        else:
            #log(lister_item)
            pass

        title_match = re.search(r'<span class="lister-item-year text-muted unbold">.*?\(([0-9]{4}).*?\)<\/span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            year = title_match.group(1)
            title_type = "tv_series"
            log(year)
        else:
            #log(lister_item)
            pass


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
            runtime = int(re.sub(',','',runtime_match.group(1))) * 60

        sort = ''
        #sort_match = re.search(r'<span class="sort"><span title="(.+?)"', lister_item, flags=(re.DOTALL | re.MULTILINE))
        #if sort_match:
        #    sort = sort_match.group(1)

        #<span class="certificate">PG</span>
        certificate = ''
        certificate_match = re.search(r'<span class="certificate">(.*?)</span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if certificate_match:
            certificate = certificate_match.group(1)

        vlabel = title
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
        log((title,year))
        if imdbID:
            item = ListItem(label=title,thumbnail=img_url,path=meta_url)
            item.set_info('video', {'title': vlabel, 'genre': genres,'code': imdbID,
            'year':year,'mediatype':'movie','rating':rating,'plot': plot,
            'mpaa': certificate,'cast': cast,'duration': runtime, 'votes': votes})
            video_streaminfo = {'codec': 'h264'}
            video_streaminfo['aspect'] = round(1280.0 / 720.0, 2)
            video_streaminfo['width'] = 1280
            video_streaminfo['height'] = 720
            item.add_stream_info('video', video_streaminfo)
            item.add_stream_info('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})
            items.append(item)


    #href="?count=100&sort=moviemeter,asc&production_status=released&languages=en&release_date=2015,2016&boxoffice_gross_us=6.0,10.0&start=1&num_votes=100,&title_type=feature&page=2&ref_=adv_nxt"
    pagination_match = re.search('<a href="([^"]*?&ref_=adv_nxt)"', html, flags=(re.DOTALL | re.MULTILINE))
    if pagination_match:
        next_page = 'http://www.imdb.com/search/title?'+pagination_match.group(1)
        items.append(
        {
            'label': "[COLOR orange]Next Page >>[/COLOR]",
            'path': plugin.url_for('title_page', url=next_page),
            'thumbnail': get_icon_path('nextpage'),
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

@plugin.route('/export_searches')
def export_searches():
    searches = plugin.get_storage('searches')
    f = xbmcvfs.File("special://profile/addon_data/plugin.video.imdb/searches.json","wb")
    s = dict((x,searches[x]) for x in searches)
    j = json.dumps(s,indent=2)
    f.write(j)
    f.close()
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/import_searches')
def import_searches():
    searches = plugin.get_storage('searches')
    f = xbmcvfs.File("special://profile/addon_data/plugin.video.imdb/searches.json","rb")
    j = f.read()
    s = json.loads(j)
    f.close()
    for name in s:
        searches[name] = s[name]
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/add_search')
def add_search():
    searches = plugin.get_storage('searches')
    d = xbmcgui.Dialog()
    name = d.input("Name")
    if not name:
        return
    url = d.input("URL",'http://www.imdb.com/search/title?count=100&user_rating=6.0,&production_status=released&title_type=feature')
    if not url:
        return
    searches[name] = url
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/remove_search/<name>')
def remove_search(name):
    searches = plugin.get_storage('searches')
    del searches[name]
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/rename_search/<name>')
def rename_search(name):
    searches = plugin.get_storage('searches')
    url = searches[name]
    d = xbmcgui.Dialog()
    new_name = d.input("Rename: "+name, name)
    if not new_name:
        return
    if name != new_name:
        searches[new_name] = url
        del searches[name]
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/duplicate_search/<name>')
def duplicate_search(name):
    searches = plugin.get_storage('searches')
    url = searches[name]
    d = xbmcgui.Dialog()
    while True:
        new_name = d.input("Duplicate: "+name, name)
        if not new_name:
            return
        if name != new_name:
            searches[new_name] = url
            xbmc.executebuiltin('Container.Refresh')
            return


@plugin.route('/edit_search/<name>')
def edit_search(name):
    searches = plugin.get_storage('searches')
    url = searches[name]
    fields = ["boxoffice_gross_us", "certificates", "companies", "count", "countries", "genres", "groups", "keywords", "languages", "locations", "num_votes", "plot", "production_status", "release_date", "role", "runtime", "sort", "title", "title_type", "user_rating"]

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
        actions = ["%s = %s" % (x,params.get(x,'')) for x in fields]
        action = d.select(name,actions)
        if action < 0:
            return
        elif fields[action] == 'certificates':
            certificates = ["us:g","us:pg","us:pg_13","us:r","us:nc_17","gb:u" ,"gb:pg" ,"gb:12" ,"gb:12a","gb:15" ,"gb:18" ,"gb:r18"]
            which = d.multiselect('Certificates',certificates)
            if which:
                certificates = [certificates[x] for x in which]
                params['certificates'] = ",".join(certificates)
            else:
                if 'certificates' in params:
                    del params['certificates']
        elif fields[action] == 'count':
            count = ["50","100"]
            which = d.select('count',count)
            if which > -1:
                params['count'] = count[which]
        elif fields[action] == 'countries':
            countries = ["ar", "au", "at", "be", "br", "bg", "ca", "cn", "co", "cr", "cz", "dk", "fi", "fr", "de", "gr", "hk", "hu", "is", "in", "ir", "ie", "it", "jp", "my", "mx", "nl", "nz", "pk", "pl", "pt", "ro", "ru", "sg", "za", "es", "se", "ch", "th", "gb", "us", "af", "ax", "al", "dz", "as", "ad", "ao", "ai", "aq", "ag", "am", "aw", "az", "bs", "bh", "bd", "bb", "by", "bz", "bj", "bm", "bt", "bo", "bq", "ba", "bw", "bv", "io", "vg", "bn", "bf", "bumm", "bi", "kh", "cm", "cv", "ky", "cf", "td", "cl", "cx", "cc", "km", "cg", "ck", "ci", "hr", "cu", "cy", "cshh", "cd", "dj", "dm", "do", "ddde", "ec", "eg", "sv", "gq", "er", "ee", "et", "fk", "fo", "yucs", "fm", "fj", "gf", "pf", "tf", "ga", "gm", "ge", "gh", "gi", "gl", "gd", "gp", "gu", "gt", "gg", "gn", "gw", "gy", "ht", "hm", "va", "hn", "id", "iq", "im", "il", "jm", "je", "jo", "kz", "ke", "ki", "xko", "xkv", "kw", "kg", "la", "lv", "lb", "ls", "lr", "ly", "li", "lt", "lu", "mo", "mg", "mw", "mv", "ml", "mt", "mh", "mq", "mr", "mu", "yt", "md", "mc", "mn", "me", "ms", "ma", "mz", "mm", "na", "nr", "np", "an", "nc", "ni", "ne", "ng", "nu", "nf", "kp", "vdvn", "mp", "no", "om", "pw", "xpi", "ps", "pa", "pg", "py", "pe", "ph", "pn", "pr", "qa", "mk", "re", "rw", "bl", "sh", "kn", "lc", "mf", "pm", "vc", "ws", "sm", "st", "sa", "sn", "rs", "csxx", "sc", "xsi", "sl", "sk", "si", "sb", "so", "gs", "kr", "suhh", "lk", "sd", "sr", "sj", "sz", "sy", "tw", "tj", "tz", "tl", "tg", "tk", "to", "tt", "tn", "tr", "tm", "tc", "tv", "vi", "ug", "ua", "ae", "um", "uy", "uz", "vu", "ve", "vn", "wf", "xwg", "eh", "ye", "xyu", "zrcd", "zm", "zw"
    ]
            which = d.multiselect('Countries',countries)
            if which:
                countries = [countries[x] for x in which]
                params['countries'] = ",".join(countries)
            else:
                if 'countries' in params:
                    del params['countries']
        elif fields[action] == 'genres':
            genres = ["action", "adventure", "animation", "biography",  "comedy", "crime", "documentary", "drama", "family", "fantasy", "film_noir", "game_show", "history", "horror", "music", "musical", "mystery", "news", "reality_tv", "romance", "sci_fi", "sport", "talk_show", "thriller", "war", "western"]
            which = d.multiselect('Genres',genres)
            if which:
                genress = [genres[x] for x in which]
                params['genres'] = ",".join(genress)
            else:
                if 'genres' in params:
                    del params['genres']
        elif fields[action] == 'groups':
            groups = ["top_100", "top_250", "top_1000", "now-playing-us", "oscar_winners", "oscar_best_picture_winners", "oscar_best_director_winners", "oscar_nominees", "emmy_winners", "emmy_nominees", "golden_globe_winners", "golden_globe_nominees", "razzie_winners", "razzie_nominees", "national_film_registry", "bottom_100", "bottom_250", "bottom_1000"]
            which = d.multiselect('groups',groups)
            if which:
                groups = [groups[x] for x in which]
                params['groups'] = ",".join(groups)
            else:
                if 'groups' in params:
                    del params['groups']
        elif fields[action] == 'languages':
            languages = ["ar", "bg", "zh", "hr", "nl", "en", "fi", "fr", "de", "el", "he", "hi", "hu", "is", "it", "ja", "ko", "no", "fa", "pl", "pt", "pa", "ro", "ru", "es", "sv", "tr", "uk", "ab", "qac", "guq", "qam", "af", "qas", "ak", "sq", "alg", "ase", "am", "apa", "an", "arc", "arp", "hy", "as", "aii", "ath", "asf", "awa", "ay", "az", "ast", "qbd", "ban", "bm", "eu", "bsc", "be", "bem", "bn", "ber", "bho", "qbi", "qbh", "bs", "bzs", "br", "bfi", "my", "yue", "ca", "km", "qax", "ce", "chr", "chy", "hne", "kw", "co", "cr", "mus", "qal", "crp", "cro", "cs", "da", "prs", "dso", "din", "qaw", "doi", "dyu", "dz", "qbc", "frs", "egy", "eo", "et", "ee", "qbg", "fo", "fil", "qbn", "fon", "fsl", "ff", "fvr", "gd", "gl", "ka", "gsg", "grb", "grc", "kl", "gn", "gu", "gnn", "gup", "ht", "hak", "bgc", "qav", "ha", "haw", "hmn", "qab", "hop", "iba", "qag", "icl", "ins", "id", "iu", "ik", "ga", "jsl", "dyo", "ktz", "qbf", "kea", "kab", "xal", "kn", "kpj", "mjw", "kar", "kk", "kca", "kha", "ki", "rw", "qar", "tlh", "kfa", "kok", "kvk", "khe", "qaq", "kro", "kyw", "qbb", "ku", "kwk", "ky", "lbj", "lad", "lo", "la", "lv", "lif", "ln", "lt", "nds", "lb", "mk", "qbm", "mag", "mai", "mg", "ms", "ml", "pqm", "qap", "mt", "mnc", "cmn", "man", "mni", "mi", "arn", "mr", "mh", "mas", "mls", "myn", "men", "mic", "enm", "nan", "min", "mwl", "lus", "moh", "mn", "moe", "qaf", "mfe", "qbl", "nah", "qba", "nv", "nbf", "nd", "nap", "yrk", "ne", "ncg", "zxx", "non", "nai", "qbk", "nyk", "ny", "oc", "oj", "qaz", "ang", "or", "pap", "qaj", "ps", "paw", "qai", "qah", "fuf", "tsz", "qu", "qya", "raj", "qbj", "rm", "rom", "rtm", "rsl", "qao", "qae", "sm", "sa", "sc", "qay", "sr", "qbo", "srr", "qad", "qau", "sn", "shh", "scn", "sjn", "sd", "si", "sio", "sk", "sl", "so", "son", "snk", "wen", "st", "qbe", "ssp", "srn", "sw", "gsw", "syl", "tl", "tg", "tmh", "ta", "tac", "tt", "te", "qak", "th", "bo", "qan", "tli", "tpi", "to", "ts", "tsc", "tn", "tcy", "tup", "tk", "tyv", "tzo", "qat", "ur", "uz", "vi", "qaa", "was", "cy", "wo", "xh", "sah", "yap", "yi", "yo", "zu" ]
            which = d.multiselect('languages',languages)
            if which:
                languages = [languages[x] for x in which]
                params['languages'] = ",".join(languages)
            else:
                if 'languages' in params:
                    del params['languages']
        elif fields[action] == 'num_votes':
            num_votes = params.get('num_votes','')
            start = ''
            end = ''
            if num_votes:
                start,end= num_votes.split(',')
            which = d.select('Number of Votes',['Low','High'])
            if which == 0:
                start = d.input("Low",start)
            elif which == 1:
                end = d.input("High",end)
            if start or end:
                params['num_votes'] = ",".join([start,end])
            else:
                if 'num_votes' in params:
                    del params['num_votes']
        elif fields[action] == 'plot':
            plot = params.get('plot','')
            plot = d.input("plot",plot)
            if plot:
                params['plot'] = plot
            else:
                if 'plot' in params:
                    del params['plot']
        elif fields[action] == 'production_status':
            production_status = ["released", "post production", "filming", "pre production", "completed", "script", "optioned property", "announced", "treatment outline", "pitch", "turnaround", "abandoned", "delayed", "indefinitely delayed", "active", "unknown"]
            which = d.multiselect('production_status',production_status)
            if which:
                production_status = [production_status[x] for x in which]
                params['production_status'] = ",".join(production_status)
            else:
                if 'production_status' in params:
                    del params['production_status']
        elif fields[action] == 'release_date':
            release_date = params.get('release_date','')
            start = ''
            end = ''
            if release_date:
                start,end= release_date.split(',')
            which = d.select('Release Date',['Start','End'])
            if which == 0:
                start = d.input("Start",start)
            elif which == 1:
                end = d.input("End",end)
            if start or end:
                params['release_date'] = ",".join([start,end])
            else:
                if 'release_date' in params:
                    del params['release_date']
        elif fields[action] == 'sort':
            sort = ["moviemeter,asc", "moviemeter,desc", "alpha,asc", "alpha,desc", "boxoffice_gross_us,asc", "boxoffice_gross_us,desc", "num_votes,asc", "num_votes,desc", "boxoffice_gross_us,asc", "boxoffice_gross_us,desc", "runtime,asc", "runtime,desc", "year,asc", "year,desc", "release_date_us,asc", "release_date_us,desc", "my_ratings", "my_ratings,asc"]
            which = d.select('sort',sort)
            if which > -1:
                params['sort'] = sort[which]
            else:
                if 'sort' in params:
                    del params['sort']
        elif fields[action] == 'title':
            title = params.get('title','')
            title = d.input("Title",title)
            if title:
                params['title'] = title
            else:
                if 'title' in params:
                    del params['title']
        elif fields[action] == 'title_type':
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
        elif fields[action] == 'boxoffice_gross_us':
            boxoffice_gross_us = params.get('boxoffice_gross_us','')
            start = ''
            end = ''
            if boxoffice_gross_us:
                start,end= boxoffice_gross_us.split(',')
            which = d.select('User Rating',['Low','High'])
            if which == 0:
                start = d.input("Low",start)
            elif which == 1:
                end = d.input("High",end)
            if start or end:
                params['boxoffice_gross_us'] = ",".join([start,end])
            else:
                if 'boxoffice_gross_us' in params:
                    del params['boxoffice_gross_us']
        elif fields[action] == 'role':
            crew = []
            while True:
                who = d.input("Cast/Crew")
                if who:
                    id = find_crew(who)
                    if id:
                        crew.append(id)
                else:
                    break
            if crew:
                params['role'] = ','.join(crew)
            else:
                if 'role' in params:
                    del params['role']
        elif fields[action] == 'keywords':
            keywords = []
            while True:
                who = d.input("Keywords")
                if who:
                    id = find_keywords(who)
                    if id:
                        keywords.append(id)
                else:
                    break
            if keywords:
                params['keywords'] = ','.join(keywords)
            else:
                if 'keywords' in params:
                    del params['keywords']
        elif fields[action] == 'boxoffice_gross_us':
            boxoffice_gross_us = params.get('boxoffice_gross_us','')
            start = ''
            end = ''
            if boxoffice_gross_us:
                start,end= boxoffice_gross_us.split(',')
            which = d.select('Box Office Gross US',['Low','High'])
            if which == 0:
                start = d.input("Low",start)
            elif which == 1:
                end = d.input("High",end)
            if start or end:
                params['boxoffice_gross_us'] = ",".join([start,end])
            else:
                if 'boxoffice_gross_us' in params:
                    del params['boxoffice_gross_us']
        elif fields[action] == 'runtime':
            runtime = params.get('runtime','')
            start = ''
            end = ''
            if runtime:
                start,end= runtime.split(',')
            which = d.select('Box Office Gross US',['Low','High'])
            if which == 0:
                start = d.input("Low",start)
            elif which == 1:
                end = d.input("High",end)
            if start or end:
                params['runtime'] = ",".join([start,end])
            else:
                if 'runtime' in params:
                    del params['runtime']
        elif fields[action] == 'locations':
            locations = params.get('locations','')
            locations = d.input("locations",locations)
            if locations:
                params['locations'] = locations
            else:
                if 'locations' in params:
                    del params['locations']
        elif fields[action] == 'companies':
            companies = params.get('companies','')
            companies = d.input("companies",companies)
            if companies:
                params['companies'] = companies
            else:
                if 'companies' in params:
                    del params['companies']
        elif fields[action] == 'user_rating':
            user_rating = params.get('user_rating','')
            start = ''
            end = ''
            if user_rating:
                start,end= user_rating.split(',')
            which = d.select('User Rating',['Low','High'])
            if which == 0:
                start = d.input("Low",start)
            elif which == 1:
                end = d.input("High",end)
            if start or end:
                params['user_rating'] = ",".join([start,end])
            else:
                if 'user_rating' in params:
                    del params['user_rating']

        params = {k: v for k, v in params.items() if v}
        kv = ["%s=%s" % (x,params[x]) for x in params]
        tail = '&'.join(kv)
        url = head+"?"+tail
        log(url)
        searches[name] = url
    xbmc.executebuiltin('Container.Refresh')

def find_crew(name=''):
    dialog = xbmcgui.Dialog()
    if not name:
        name = dialog.input('Search for crew (actor, director etc)', type=xbmcgui.INPUT_ALPHANUM)
    dialog.notification('IMDB:','Finding crew details...')
    if not name:
        dialog.notification('IMDB:','No name!')
        return
    url = "http://www.imdb.com/xml/find?json=1&nr=1&q=%s&nm=on" % urllib.quote_plus(name)
    r = requests.get(url)
    json = r.json()
    crew = []

    if 'name_popular' in json:
        pop = json['name_popular']
        for p in pop:
            crew.append(("[COLOR yellow]%s[/COLOR]" % p['name'],p['id']))
    if 'name_exact' in json:
        pop = json['name_exact']
        for p in pop:
            crew.append(("[COLOR green]%s[/COLOR]" % p['name'],p['id']))
    if 'name_approx' in json:
        approx = json['name_approx']
        for p in approx:
            crew.append(("[COLOR orange]%s[/COLOR]" % p['name'],p['id']))
    if 'name_substring' in json:
        pop = json['name_substring']
        for p in pop:
            crew.append(("[COLOR red]%s[/COLOR]" % p['name'],p['id']))
    names = [item[0] for item in crew]
    if names:
        index = dialog.select('Pick crew member',names)
        if index > -1:
            id = crew[index][1]
            return id
    else:
        dialog.notification('IMDB:','Nothing Found!')

def find_keywords(keyword=''):
    dialog = xbmcgui.Dialog()
    if not keyword:
        keyword = dialog.input('Search for keyword', type=xbmcgui.INPUT_ALPHANUM)
    dialog.notification('IMDB:','Finding keyword matches...')
    if not keyword:
        dialog.notification('IMDB:','No keyword!')
        return
    url = "http://www.imdb.com/xml/find?json=1&nr=1&q=%s&kw=on" % urllib.quote_plus(keyword)
    r = requests.get(url)
    json = r.json()
    keywords = []
    if 'keyword_popular' in json:
        pop = json['keyword_popular']
        for p in pop:
            keywords.append((p['description'],p['keyword']))
    if 'keyword_exact' in json:
        pop = json['keyword_exact']
        for p in pop:
            keywords.append((p['description'],p['keyword']))
    if 'keyword_approx' in json:
        approx = json['keyword_approx']
        for p in approx:
            keywords.append((p['description'],p['keyword']))
    if 'keyword_substring' in json:
        approx = json['keyword_substring']
        for p in approx:
            keywords.append((p['description'],p['keyword']))
    names = [item[0] for item in keywords]
    if keywords:
        index = dialog.select('Pick keywords member',names)
        if index > -1:
            id = keywords[index][1]
            return  id
    else:
        dialog.notification('IMDB:','Nothing Found!')

@plugin.route('/')
def index():
    searches = plugin.get_storage('searches')
    items = []
    for search in searches:
        context_items = []
        context_items.append(('[COLOR yellow]Edit[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('edit_search', name=search))))
        context_items.append(('[COLOR yellow]Rename[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('rename_search', name=search))))
        context_items.append(('[COLOR yellow]Remove[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('remove_search', name=search))))
        context_items.append(('[COLOR yellow]Duplicate[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('duplicate_search', name=search))))
        items.append(
        {
            'label': search,
            'path': plugin.url_for('title_page',url=searches[search]),
            'thumbnail':get_icon_path('search'),
            'context_menu': context_items,
        })

    items.append(
    {
        'label': "[COLOR dimgray]Add Search[/COLOR]",
        'path': plugin.url_for('add_search'),
        'thumbnail':get_icon_path('settings'),

    })
    items.append(
    {
        'label': "[COLOR dimgray]Export Searches[/COLOR]",
        'path': plugin.url_for('export_searches'),
        'thumbnail':get_icon_path('settings'),

    })
    items.append(
    {
        'label': "[COLOR dimgray]Import Searches[/COLOR]",
        'path': plugin.url_for('import_searches'),
        'thumbnail':get_icon_path('settings'),

    })
    return items



if __name__ == '__main__':

    plugin.run()
    if big_list_view == True:
        view_mode = int(plugin.get_setting('view'))
        if view_mode:
            plugin.set_view_mode(view_mode)
            plugin.set_content("episodes")
            #xbmcplugin.setContent(int(sys.argv[1]), 'movies')