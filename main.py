# -*- coding: utf-8 -*-

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
from trakt import Trakt
import SimpleDownloader as downloader


plugin = Plugin()
big_list_view = False

countries_list = (
    ("Argentina","ar"),
    ("Australia","au"),
    ("Austria","at"),
    ("Belgium","be"),
    ("Brazil","br"),
    ("Bulgaria","bg"),
    ("Canada","ca"),
    ("China","cn"),
    ("Colombia","co"),
    ("Costa Rica","cr"),
    ("Czech Republic","cz"),
    ("Denmark","dk"),
    ("Finland","fi"),
    ("France","fr"),
    ("Germany","de"),
    ("Greece","gr"),
    ("Hong Kong","hk"),
    ("Hungary","hu"),
    ("Iceland","is"),
    ("India","in"),
    ("Iran","ir"),
    ("Ireland","ie"),
    ("Italy","it"),
    ("Japan","jp"),
    ("Malaysia","my"),
    ("Mexico","mx"),
    ("Netherlands","nl"),
    ("New Zealand","nz"),
    ("Pakistan","pk"),
    ("Poland","pl"),
    ("Portugal","pt"),
    ("Romania","ro"),
    ("Russia","ru"),
    ("Singapore","sg"),
    ("South Africa","za"),
    ("Spain","es"),
    ("Sweden","se"),
    ("Switzerland","ch"),
    ("Thailand","th"),
    ("United Kingdom","gb"),
    ("United States","us"),
    ("Afghanistan","af"),
    ("&#xC5;land Islands","ax"),
    ("Albania","al"),
    ("Algeria","dz"),
    ("American Samoa","as"),
    ("Andorra","ad"),
    ("Angola","ao"),
    ("Anguilla","ai"),
    ("Antarctica","aq"),
    ("Antigua and Barbuda","ag"),
    ("Armenia","am"),
    ("Aruba","aw"),
    ("Azerbaijan","az"),
    ("Bahamas","bs"),
    ("Bahrain","bh"),
    ("Bangladesh","bd"),
    ("Barbados","bb"),
    ("Belarus","by"),
    ("Belize","bz"),
    ("Benin","bj"),
    ("Bermuda","bm"),
    ("Bhutan","bt"),
    ("Bolivia","bo"),
    ("Bonaire), Sint Eustatius and Saba","bq"),
    ("Bosnia and Herzegovina","ba"),
    ("Botswana","bw"),
    ("Bouvet Island","bv"),
    ("British Indian Ocean Territory","io"),
    ("British Virgin Islands","vg"),
    ("Brunei Darussalam","bn"),
    ("Burkina Faso","bf"),
    ("Burma","bumm"),
    ("Burundi","bi"),
    ("Cambodia","kh"),
    ("Cameroon","cm"),
    ("Cape Verde","cv"),
    ("Cayman Islands","ky"),
    ("Central African Republic","cf"),
    ("Chad","td"),
    ("Chile","cl"),
    ("Christmas Island","cx"),
    ("Cocos (Keeling) Islands","cc"),
    ("Comoros","km"),
    ("Congo","cg"),
    ("Cook Islands","ck"),
    ("C&#xF4;te d&#x27;Ivoire","ci"),
    ("Croatia","hr"),
    ("Cuba","cu"),
    ("Cyprus","cy"),
    ("Czechoslovakia","cshh"),
    ("Democratic Republic of the Congo","cd"),
    ("Djibouti","dj"),
    ("Dominica","dm"),
    ("Dominican Republic","do"),
    ("East Germany","ddde"),
    ("Ecuador","ec"),
    ("Egypt","eg"),
    ("El Salvador","sv"),
    ("Equatorial Guinea","gq"),
    ("Eritrea","er"),
    ("Estonia","ee"),
    ("Ethiopia","et"),
    ("Falkland Islands","fk"),
    ("Faroe Islands","fo"),
    ("Federal Republic of Yugoslavia","yucs"),
    ("Federated States of Micronesia","fm"),
    ("Fiji","fj"),
    ("French Guiana","gf"),
    ("French Polynesia","pf"),
    ("French Southern Territories","tf"),
    ("Gabon","ga"),
    ("Gambia","gm"),
    ("Georgia","ge"),
    ("Ghana","gh"),
    ("Gibraltar","gi"),
    ("Greenland","gl"),
    ("Grenada","gd"),
    ("Guadeloupe","gp"),
    ("Guam","gu"),
    ("Guatemala","gt"),
    ("Guernsey","gg"),
    ("Guinea","gn"),
    ("Guinea-Bissau","gw"),
    ("Guyana","gy"),
    ("Haiti","ht"),
    ("Heard Island and McDonald Islands","hm"),
    ("Holy See (Vatican City State)","va"),
    ("Honduras","hn"),
    ("Indonesia","id"),
    ("Iraq","iq"),
    ("Isle of Man","im"),
    ("Israel","il"),
    ("Jamaica","jm"),
    ("Jersey","je"),
    ("Jordan","jo"),
    ("Kazakhstan","kz"),
    ("Kenya","ke"),
    ("Kiribati","ki"),
    ("Korea","xko"),
    ("Kosovo","xkv"),
    ("Kuwait","kw"),
    ("Kyrgyzstan","kg"),
    ("Laos","la"),
    ("Latvia","lv"),
    ("Lebanon","lb"),
    ("Lesotho","ls"),
    ("Liberia","lr"),
    ("Libya","ly"),
    ("Liechtenstein","li"),
    ("Lithuania","lt"),
    ("Luxembourg","lu"),
    ("Macao","mo"),
    ("Madagascar","mg"),
    ("Malawi","mw"),
    ("Maldives","mv"),
    ("Mali","ml"),
    ("Malta","mt"),
    ("Marshall Islands","mh"),
    ("Martinique","mq"),
    ("Mauritania","mr"),
    ("Mauritius","mu"),
    ("Mayotte","yt"),
    ("Moldova","md"),
    ("Monaco","mc"),
    ("Mongolia","mn"),
    ("Montenegro","me"),
    ("Montserrat","ms"),
    ("Morocco","ma"),
    ("Mozambique","mz"),
    ("Myanmar","mm"),
    ("Namibia","na"),
    ("Nauru","nr"),
    ("Nepal","np"),
    ("Netherlands Antilles","an"),
    ("New Caledonia","nc"),
    ("Nicaragua","ni"),
    ("Niger","ne"),
    ("Nigeria","ng"),
    ("Niue","nu"),
    ("Norfolk Island","nf"),
    ("North Korea","kp"),
    ("North Vietnam","vdvn"),
    ("Northern Mariana Islands","mp"),
    ("Norway","no"),
    ("Oman","om"),
    ("Palau","pw"),
    ("Palestine","xpi"),
    ("Palestinian Territory","ps"),
    ("Panama","pa"),
    ("Papua New Guinea","pg"),
    ("Paraguay","py"),
    ("Peru","pe"),
    ("Philippines","ph"),
    ("Pitcairn","pn"),
    ("Puerto Rico","pr"),
    ("Qatar","qa"),
    ("Republic of Macedonia","mk"),
    ("R&#xE9;union","re"),
    ("Rwanda","rw"),
    ("Saint Barth&#xE9;lemy","bl"),
    ("Saint Helena","sh"),
    ("Saint Kitts and Nevis","kn"),
    ("Saint Lucia","lc"),
    ("Saint Martin (French part)","mf"),
    ("Saint Pierre and Miquelon","pm"),
    ("Saint Vincent and the Grenadines","vc"),
    ("Samoa","ws"),
    ("San Marino","sm"),
    ("Sao Tome and Principe","st"),
    ("Saudi Arabia","sa"),
    ("Senegal","sn"),
    ("Serbia","rs"),
    ("Serbia and Montenegro","csxx"),
    ("Seychelles","sc"),
    ("Siam","xsi"),
    ("Sierra Leone","sl"),
    ("Slovakia","sk"),
    ("Slovenia","si"),
    ("Solomon Islands","sb"),
    ("Somalia","so"),
    ("South Georgia and the South Sandwich Islands","gs"),
    ("South Korea","kr"),
    ("Soviet Union","suhh"),
    ("Sri Lanka","lk"),
    ("Sudan","sd"),
    ("Suriname","sr"),
    ("Svalbard and Jan Mayen","sj"),
    ("Swaziland","sz"),
    ("Syria","sy"),
    ("Taiwan","tw"),
    ("Tajikistan","tj"),
    ("Tanzania","tz"),
    ("Timor-Leste","tl"),
    ("Togo","tg"),
    ("Tokelau","tk"),
    ("Tonga","to"),
    ("Trinidad and Tobago","tt"),
    ("Tunisia","tn"),
    ("Turkey","tr"),
    ("Turkmenistan","tm"),
    ("Turks and Caicos Islands","tc"),
    ("Tuvalu","tv"),
    ("U.S. Virgin Islands","vi"),
    ("Uganda","ug"),
    ("Ukraine","ua"),
    ("United Arab Emirates","ae"),
    ("United States Minor Outlying Islands","um"),
    ("Uruguay","uy"),
    ("Uzbekistan","uz"),
    ("Vanuatu","vu"),
    ("Venezuela","ve"),
    ("Vietnam","vn"),
    ("Wallis and Futuna","wf"),
    ("West Germany","xwg"),
    ("Western Sahara","eh"),
    ("Yemen","ye"),
    ("Yugoslavia","xyu"),
    ("Zaire","zrcd"),
    ("Zambia","zm"),
    ("Zimbabwe","zw"),
)

languages_list = (
    ("Arabic","ar"),
    ("Bulgarian","bg"),
    ("Chinese","zh"),
    ("Croatian","hr"),
    ("Dutch","nl"),
    ("English","en"),
    ("Finnish","fi"),
    ("French","fr"),
    ("German","de"),
    ("Greek","el"),
    ("Hebrew","he"),
    ("Hindi","hi"),
    ("Hungarian","hu"),
    ("Icelandic","is"),
    ("Italian","it"),
    ("Japanese","ja"),
    ("Korean","ko"),
    ("Norwegian","no"),
    ("Persian","fa"),
    ("Polish","pl"),
    ("Portuguese","pt"),
    ("Punjabi","pa"),
    ("Romanian","ro"),
    ("Russian","ru"),
    ("Spanish","es"),
    ("Swedish","sv"),
    ("Turkish","tr"),
    ("Ukrainian","uk"),
    ("Abkhazian","ab"),
    ("Aboriginal","qac"),
    ("Ach&#xE9;","guq"),
    ("Acholi","qam"),
    ("Afrikaans","af"),
    ("Aidoukrou","qas"),
    ("Akan","ak"),
    ("Albanian","sq"),
    ("Algonquin","alg"),
    ("American Sign Language","ase"),
    ("Amharic","am"),
    ("Apache languages","apa"),
    ("Aragonese","an"),
    ("Aramaic","arc"),
    ("Arapaho","arp"),
    ("Armenian","hy"),
    ("Assamese","as"),
    ("Assyrian Neo-Aramaic","aii"),
    ("Athapascan languages","ath"),
    ("Australian Sign Language","asf"),
    ("Awadhi","awa"),
    ("Aymara","ay"),
    ("Azerbaijani","az"),
    ("Bable","ast"),
    ("Baka","qbd"),
    ("Balinese","ban"),
    ("Bambara","bm"),
    ("Basque","eu"),
    ("Bassari","bsc"),
    ("Belarusian","be"),
    ("Bemba","bem"),
    ("Bengali","bn"),
    ("Berber languages","ber"),
    ("Bhojpuri","bho"),
    ("Bicolano","qbi"),
    ("Bodo","qbh"),
    ("Bosnian","bs"),
    ("Brazilian Sign Language","bzs"),
    ("Breton","br"),
    ("British Sign Language","bfi"),
    ("Burmese","my"),
    ("Cantonese","yue"),
    ("Catalan","ca"),
    ("Central Khmer","km"),
    ("Chaozhou","qax"),
    ("Chechen","ce"),
    ("Cherokee","chr"),
    ("Cheyenne","chy"),
    ("Chhattisgarhi","hne"),
    ("Cornish","kw"),
    ("Corsican","co"),
    ("Cree","cr"),
    ("Creek","mus"),
    ("Creole","qal"),
    ("Creoles and pidgins","crp"),
    ("Crow","cro"),
    ("Czech","cs"),
    ("Danish","da"),
    ("Dari","prs"),
    ("Desiya","dso"),
    ("Dinka","din"),
    ("Djerma","qaw"),
    ("Dogri","doi"),
    ("Dyula","dyu"),
    ("Dzongkha","dz"),
    ("East-Greenlandic","qbc"),
    ("Eastern Frisian","frs"),
    ("Egyptian (Ancient)","egy"),
    ("Esperanto","eo"),
    ("Estonian","et"),
    ("Ewe","ee"),
    ("Faliasch","qbg"),
    ("Faroese","fo"),
    ("Filipino","fil"),
    ("Flemish","qbn"),
    ("Fon","fon"),
    ("French Sign Language","fsl"),
    ("Fulah","ff"),
    ("Fur","fvr"),
    ("Gaelic","gd"),
    ("Galician","gl"),
    ("Georgian","ka"),
    ("German Sign Language","gsg"),
    ("Grebo","grb"),
    ("Greek), Ancient (to 1453)","grc"),
    ("Greenlandic","kl"),
    ("Guarani","gn"),
    ("Gujarati","gu"),
    ("Gumatj","gnn"),
    ("Gunwinggu","gup"),
    ("Haitian","ht"),
    ("Hakka","hak"),
    ("Haryanvi","bgc"),
    ("Hassanya","qav"),
    ("Hausa","ha"),
    ("Hawaiian","haw"),
    ("Hmong","hmn"),
    ("Hokkien","qab"),
    ("Hopi","hop"),
    ("Iban","iba"),
    ("Ibo","qag"),
    ("Icelandic Sign Language","icl"),
    ("Indian Sign Language","ins"),
    ("Indonesian","id"),
    ("Inuktitut","iu"),
    ("Inupiaq","ik"),
    ("Irish Gaelic","ga"),
    ("Japanese Sign Language","jsl"),
    ("Jola-Fonyi","dyo"),
    ("Ju&#x27;hoan","ktz"),
    ("Kaado","qbf"),
    ("Kabuverdianu","kea"),
    ("Kabyle","kab"),
    ("Kalmyk-Oirat","xal"),
    ("Kannada","kn"),
    ("Karaj&#xE1;","kpj"),
    ("Karbi","mjw"),
    ("Karen","kar"),
    ("Kazakh","kk"),
    ("Khanty","kca"),
    ("Khasi","kha"),
    ("Kikuyu","ki"),
    ("Kinyarwanda","rw"),
    ("Kirundi","qar"),
    ("Klingon","tlh"),
    ("Kodava","kfa"),
    ("Konkani","kok"),
    ("Korean Sign Language","kvk"),
    ("Korowai","khe"),
    ("Kriolu","qaq"),
    ("Kru","kro"),
    ("Kudmali","kyw"),
    ("Kuna","qbb"),
    ("Kurdish","ku"),
    ("Kwakiutl","kwk"),
    ("Kyrgyz","ky"),
    ("Ladakhi","lbj"),
    ("Ladino","lad"),
    ("Lao","lo"),
    ("Latin","la"),
    ("Latvian","lv"),
    ("Limbu","lif"),
    ("Lingala","ln"),
    ("Lithuanian","lt"),
    ("Low German","nds"),
    ("Luxembourgish","lb"),
    ("Macedonian","mk"),
    ("Macro-J&#xEA;","qbm"),
    ("Magahi","mag"),
    ("Maithili","mai"),
    ("Malagasy","mg"),
    ("Malay","ms"),
    ("Malayalam","ml"),
    ("Malecite-Passamaquoddy","pqm"),
    ("Malinka","qap"),
    ("Maltese","mt"),
    ("Manchu","mnc"),
    ("Mandarin","cmn"),
    ("Mandingo","man"),
    ("Manipuri","mni"),
    ("Maori","mi"),
    ("Mapudungun","arn"),
    ("Marathi","mr"),
    ("Marshallese","mh"),
    ("Masai","mas"),
    ("Masalit","mls"),
    ("Maya","myn"),
    ("Mende","men"),
    ("Micmac","mic"),
    ("Middle English","enm"),
    ("Min Nan","nan"),
    ("Minangkabau","min"),
    ("Mirandese","mwl"),
    ("Mizo","lus"),
    ("Mohawk","moh"),
    ("Mongolian","mn"),
    ("Montagnais","moe"),
    ("More","qaf"),
    ("Morisyen","mfe"),
    ("Nagpuri","qbl"),
    ("Nahuatl","nah"),
    ("Nama","qba"),
    ("Navajo","nv"),
    ("Naxi","nbf"),
    ("Ndebele","nd"),
    ("Neapolitan","nap"),
    ("Nenets","yrk"),
    ("Nepali","ne"),
    ("Nisga&#x27;a","ncg"),
    ("None","zxx"),
    ("Norse), Old","non"),
    ("North American Indian","nai"),
    ("Nushi","qbk"),
    ("Nyaneka","nyk"),
    ("Nyanja","ny"),
    ("Occitan","oc"),
    ("Ojibwa","oj"),
    ("Ojihimba","qaz"),
    ("Old English","ang"),
    ("Oriya","or"),
    ("Papiamento","pap"),
    ("Parsee","qaj"),
    ("Pashtu","ps"),
    ("Pawnee","paw"),
    ("Peul","qai"),
    ("Polynesian","qah"),
    ("Pular","fuf"),
    ("Purepecha","tsz"),
    ("Quechua","qu"),
    ("Quenya","qya"),
    ("Rajasthani","raj"),
    ("Rawan","qbj"),
    ("Romansh","rm"),
    ("Romany","rom"),
    ("Rotuman","rtm"),
    ("Russian Sign Language","rsl"),
    ("Ryukyuan","qao"),
    ("Saami","qae"),
    ("Samoan","sm"),
    ("Sanskrit","sa"),
    ("Sardinian","sc"),
    ("Scanian","qay"),
    ("Serbian","sr"),
    ("Serbo-Croatian","qbo"),
    ("Serer","srr"),
    ("Shanghainese","qad"),
    ("Shanxi","qau"),
    ("Shona","sn"),
    ("Shoshoni","shh"),
    ("Sicilian","scn"),
    ("Sindarin","sjn"),
    ("Sindhi","sd"),
    ("Sinhala","si"),
    ("Sioux","sio"),
    ("Slovak","sk"),
    ("Slovenian","sl"),
    ("Somali","so"),
    ("Songhay","son"),
    ("Soninke","snk"),
    ("Sorbian languages","wen"),
    ("Sotho","st"),
    ("Sousson","qbe"),
    ("Spanish Sign Language","ssp"),
    ("Sranan","srn"),
    ("Swahili","sw"),
    ("Swiss German","gsw"),
    ("Sylheti","syl"),
    ("Tagalog","tl"),
    ("Tajik","tg"),
    ("Tamashek","tmh"),
    ("Tamil","ta"),
    ("Tarahumara","tac"),
    ("Tatar","tt"),
    ("Telugu","te"),
    ("Teochew","qak"),
    ("Thai","th"),
    ("Tibetan","bo"),
    ("Tigrigna","qan"),
    ("Tlingit","tli"),
    ("Tok Pisin","tpi"),
    ("Tonga (Tonga Islands)","to"),
    ("Tsonga","ts"),
    ("Tswa","tsc"),
    ("Tswana","tn"),
    ("Tulu","tcy"),
    ("Tupi","tup"),
    ("Turkmen","tk"),
    ("Tuvinian","tyv"),
    ("Tzotzil","tzo"),
    ("Ungwatsi","qat"),
    ("Urdu","ur"),
    ("Uzbek","uz"),
    ("Vietnamese","vi"),
    ("Visayan","qaa"),
    ("Washoe","was"),
    ("Welsh","cy"),
    ("Wolof","wo"),
    ("Xhosa","xh"),
    ("Yakut","sah"),
    ("Yapese","yap"),
    ("Yiddish","yi"),
    ("Yoruba","yo"),
    ("Zulu","zu")
)

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

def load_people():
    f = xbmcvfs.File('special://profile/addon_data/plugin.video.imdb.search/people.json','rb')
    if not f:
        return
    s = f.read()
    f.close()
    if s:
        return json.loads(s)

def save_people(people):
    f = xbmcvfs.File('special://profile/addon_data/plugin.video.imdb.search/people.json','wb')
    s = json.dumps(people)
    f.write(s)
    f.close()

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

@plugin.route('/name_page/<url>')
def name_page(url):
    global big_list_view
    big_list_view = True
    #people = plugin.get_storage('people')
    people = load_people()
    if not people:
        people = {}
    r = requests.get(url, headers=headers)
    html = r.content
    #html = HTMLParser.HTMLParser().unescape(html)
    #log(html)
    match = re.findall('<a href="/name/(nm[0-9]*)/" title="(.*?)"><img src="(.*?)"',html,flags=(re.DOTALL | re.MULTILINE))
    items = []
    for (id,name,img) in match:
        #log(name)
        #log(len(name))
        #name = name.decode('utf-8')
        #log(name)
        people[id] = name
        url = "http://www.imdb.com/search/title?count=50&production_status=released&role=%s" % id
        img = re.sub(r'S[XY].*_.jpg','SX344_.jpg',img) #NOTE 344 is Confluence List View width
        items.append({
            'label' :  name,
            'path' : plugin.url_for('browse',url=url),
            'thumbnail' : img
        })

    match = re.search('<a href="(.*?)">Next',html)
    #log(match)
    if match:
        next_page = "http://www.imdb.com" + match.group(1)
        items.append(
        {
            'label': "Next Page >>",
            'path': plugin.url_for('name_page', url=next_page),
            'thumbnail': get_icon_path('nextpage'),
        })
    save_people(people)
    return items



@plugin.route('/title_page/<url>')
def title_page(url):
    for i in re.findall('date\[(\d+)\]', url):
        url = url.replace('date[%s]' % i, (datetime.datetime.now() - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))
    global big_list_view
    big_list_view = True
    r = requests.get(url, headers=headers)
    html = r.content
    #html = HTMLParser.HTMLParser().unescape(html)

    lister_items = html.split('<div class="lister-item ')
    items = []
    for lister_item in lister_items:
        if not re.search(r'^mode-advanced">',lister_item):
            continue
        title_type = ''
        trakt_type = ''
        #loadlate="http://ia.media-imdb.com/images/M/MV5BMjIyMTg5MTg4OV5BMl5BanBnXkFtZTgwMzkzMjY5NzE@._V1_UX67_CR0,0,67,98_AL_.jpg"
        img_url = ''
        img_match = re.search(r'<img.*?loadlate="(.*?)"', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if img_match:
            img = img_match.group(1)
            if plugin.get_setting('enhance') == '2':
                img_url = re.sub(r'U[XY].*_.jpg','SX344_.jpg',img) #NOTE 344 is Confluence List View width
            else:
                if plugin.get_setting('enhance') == '0':
                    img_url = img
                else:
                    img_url = re.sub(r'UX67_CR(.*?),0,67,98','UX182_CR\g<1>,0,182,268',img)
                    img_url = re.sub(r'UY98_CR(.*?),0,67,98','UY268_CR\g<1>,0,182,268',img_url)

        title = ''
        imdbID = ''
        year = ''
        #<a href="/title/tt1985949/?ref_=adv_li_tt"\n>Angry Birds</a>
        title_match = re.search(r'<a href="/title/(tt[0-9]*)/\?ref_=adv_li_tt".>(.*?)</a>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            imdbID = title_match.group(1)
            title = title_match.group(2)
            #log((imdbID,title))
        else:
            #log(lister_item)
            pass

        info_type = ''
        #<span class="lister-lister_item-year text-muted unbold">(2016)</span>
        #title_match = re.search(r'<span class="lister-lister_item-year text-muted unbold">.*?\(([0-9]*?)\)<\/span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        title_match = re.search(r'<span class="lister-item-year text-muted unbold">.*?\(([0-9]{4})\)<\/span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            year = title_match.group(1)
            title_type = "movie"
            trakt_type = 'movies'
            info_type = 'extendedinfo'
            #log(year)
        else:
            #log(lister_item)
            #pass

            title_match = re.search(r'<span class="lister-item-year text-muted unbold">.*?\(([0-9]{4}).*?\)<\/span>', lister_item, flags=(re.DOTALL | re.MULTILINE))
            if title_match:
                year = title_match.group(1)
                title_type = "tv_series"
                trakt_type = 'shows'
                info_type = 'extendedtvinfo'
                #log(year)
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
            trakt_type = 'episodes'

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
            plot = re.sub('<a.*?</a>','',plot)

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
            #log(title_type)
            if title_type == "tv_series" or title_type == "mini_series":
                trakt_type = 'shows'
                meta_url = "plugin://plugin.video.imdb.search/meta_tvdb/%s/%s" % (id,urllib.quote_plus(title.encode("utf8")))
                #meta_url = "plugin://%s/tv/search_term/%s/1" % (plugin.get_setting('catchup.plugin').lower(),urllib.quote_plus(title))
            elif title_type == "tv_episode":
                vlabel = "%s - %s" % (title, episode)
                vlabel = urllib.quote_plus(vlabel.encode("utf8"))
                meta_url = "plugin://plugin.video.imdb.search/?action=episode&imdb_id=%s&episode_id=%s&title=%s" % (imdbID,episode_id,vlabel) #TODO
                id = episode_id
            else:
                meta_url = 'plugin://%s/movies/play/imdb/%s/select' % (plugin.get_setting('catchup.plugin').lower(),imdbID)
            #log(meta_url)
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
            context_items = []
            context_items.append(('Information', 'XBMC.Action(Info)'))
            try:
                if info_type and xbmcaddon.Addon('script.extendedinfo'):
                    context_items.append(('Extended Info', "XBMC.RunScript(script.extendedinfo,info=%s,imdb_id=%s)" % (info_type,imdbID)))
            except:
                pass
            context_items.append(('Add to Trakt Watchlist', 'XBMC.RunPlugin(%s)' % (plugin.url_for('add_to_trakt_watchlist', type=trakt_type, imdb_id=imdbID, title=title))))
            try:
                if title_type == 'movie' and xbmcaddon.Addon('plugin.video.couchpotato_manager'):
                    context_items.append(('Add to Couch Potato', "XBMC.RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add-by-id/%s)" % imdbID))
            except:
                pass
            if title_type == "tv_series" or title_type == "mini_series":
                try:
                    if xbmcaddon.Addon('plugin.video.sickrage'):
                        context_items.append(('Add to Sickrage', "XBMC.RunPlugin(plugin://plugin.video.sickrage?action=addshow&&show_name=%s)" % title))
                except:
                    context_items.append(('Add to Sickrage', 'XBMC.RunPlugin(%s)' % (plugin.url_for('sickrage_addshow', title=title))))

            item.add_context_menu_items(context_items)
            items.append(item)

    #href="?count=50&sort=moviemeter,asc&production_status=released&languages=en&release_date=2015,2016&boxoffice_gross_us=6.0,10.0&start=1&num_votes=100,&title_type=feature&page=2&ref_=adv_nxt"
    pagination_match = re.findall('<a href="([^"]*?&ref_=adv_nxt)"', html, flags=(re.DOTALL | re.MULTILINE))
    if pagination_match:
        next_page = 'http://www.imdb.com/search/title?'+pagination_match[-1].strip('?')
        #log(next_page)
        items.append(
        {
            'label': "Next Page >>",
            'path': plugin.url_for('title_page', url=next_page),
            'thumbnail': get_icon_path('nextpage'),
        })

    return items

def get_tvdb_id(imdb_id):
    tvdb_url = "http://thetvdb.com//api/GetSeriesByRemoteID.php?imdbid=%s" % imdb_id
    r = requests.get(tvdb_url)
    tvdb_html = r.text
    tvdb_id = ''
    tvdb_match = re.search(r'<seriesid>(.*?)</seriesid>', tvdb_html, flags=(re.DOTALL | re.MULTILINE))
    if tvdb_match:
        tvdb_id = tvdb_match.group(1)
    return tvdb_id

@plugin.route('/meta_tvdb/<imdb_id>/<title>')
def meta_tvdb(imdb_id,title):
    tvdb_id = get_tvdb_id(imdb_id)
    #log((imdb_id,tvdb_id,title))
    meta_url = "plugin://%s/tv/tvdb/%s" % (plugin.get_setting('catchup.plugin').lower(),tvdb_id)

    item ={'label':title, 'path':meta_url, 'thumbnail': get_icon_path('meta')}
    #TODO launch into Meta seasons view
    return [item]

@plugin.route('/sickrage_addshow/<title>')
def sickrage_addshow(title):
    import resources.lib.common as common
    import resources.lib.settings as settings
    import resources.lib.sickbeard as sickbeard
    import resources.lib.addshow as addshow
    addshow.AddShow(title)

@plugin.route('/feature')
def feature():
    url = 'http://www.imdb.com/search/title?count=50&production_status=released&title_type=feature'
    return title_page(url)


@plugin.route('/tv_movie')
def tv_movie():
    url = 'http://www.imdb.com/search/title?count=50&production_status=released&title_type=tv_movie'
    return title_page(url)

@plugin.route('/export_searches')
def export_searches():
    searches = plugin.get_storage('searches')
    f = xbmcvfs.File("special://profile/addon_data/plugin.video.imdb.search/searches.json","wb")
    s = dict((x,searches[x]) for x in searches)
    j = json.dumps(s,indent=2)
    f.write(j)
    f.close()
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/import_searches')
def import_searches():
    searches = plugin.get_storage('searches')
    f = xbmcvfs.File("special://profile/addon_data/plugin.video.imdb.search/searches.json","rb")
    j = f.read()
    s = json.loads(j)
    f.close()
    for name in s:
        searches[name] = s[name]
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/add/<name>/<url>')
def add(name,url):
    searches = plugin.get_storage('searches')
    d = xbmcgui.Dialog()
    name = d.input("Name - %s" % name,name)
    if not name:
        return
    searches[name] = url

@plugin.route('/add_subscription/<name>/<url>')
def add_subscription(name,url):
    subscriptions = plugin.get_storage('subscriptions')
    subscriptions[name] = url
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/remove_subscription/<name>')
def remove_subscription(name):
    subscriptions = plugin.get_storage('subscriptions')
    del subscriptions[name]
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/add_search')
def add_search():
    searches = plugin.get_storage('searches')
    d = xbmcgui.Dialog()
    name = d.input("Name")
    if not name:
        return
    url = d.input("URL",'http://www.imdb.com/search/title?count=50&user_rating=6.0,&production_status=released&title_type=feature')
    if not url:
        return
    searches[name] = url
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/remove_search/<name>')
def remove_search(name):
    searches = plugin.get_storage('searches')
    del searches[name]
    remove_subscription(name)
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

@plugin.route('/browse_search/<name>')
def browse_search(name):
    searches = plugin.get_storage('searches')
    url = searches[name]
    url = 'Container.Update(%s,replace)' % plugin.url_for('browse',url=url)
    xbmc.executebuiltin(url)
    #xbmc.executebuiltin("RunPlugin(%s)" % plugin.url_for('browse',url=url))

@plugin.route('/edit_search/<name>')
def edit_search(name):
    searches = plugin.get_storage('searches')
    url = searches[name]
    fields = ["boxoffice_gross_us", "certificates", "companies", "count", "countries", "genres", "groups", "keywords", "languages", "locations", "num_votes", "plot", "production_status", "release_date", "role", "runtime", "sort", "title", "title_type", "user_rating"]
    labels = ["Boxoffice Gross US", "Certificates", "Companies", "Count", "Countries", "Genres", "Groups", "Keywords", "Languages", "Locations", "Num Votes", "Plot", "Production Status", "Release Date", "Role", "Runtime", "Sort", "Title", "Title Type", "User Rating"]
    label_field = zip(labels,fields)
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
        actions = ["%s - %s" % (l,params.get(f,'')) for l,f in label_field]
        action = d.select(name,actions)
        if action < 0:
            break
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
            countries = [x[0] for x in countries_list]
            which = d.multiselect('countries',countries)
            if which:
                countries = [countries_list[x][1] for x in which]
                params['countries'] = ",".join(countries)
            else:
                if 'countries' in params:
                    del params['countries']

            for k,v in params.items():
                if not v:
                    del params[k]
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
            languages = [x[0] for x in languages_list]
            which = d.multiselect('languages',languages)
            if which:
                languages = [languages_list[x][1] for x in which]
                params['languages'] = ",".join(languages)
            else:
                if 'languages' in params:
                    del params['languages']

            for k,v in params.items():
                if not v:
                    del params[k]
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
            sort = ["moviemeter,asc", "moviemeter,desc", "alpha,asc", "alpha,desc", "user_rating,asc", "user_rating,desc", "boxoffice_gross_us,asc", "boxoffice_gross_us,desc", "num_votes,asc", "num_votes,desc", "boxoffice_gross_us,asc", "boxoffice_gross_us,desc", "runtime,asc", "runtime,desc", "year,asc", "year,desc", "release_date_us,asc", "release_date_us,desc", "my_ratings", "my_ratings,asc"]
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
            rating = ["-"] + [str(float(x)/10.0) for x in range(10,101,1)]
            if which == 0:
                selected = d.select("Low",rating)
                if selected == 0:
                    start = ''
                elif selected > 0:
                    start = rating[selected]
            elif which == 1:
                selected = d.select("High",rating)
                if selected == 0:
                    end = ''
                elif selected > 0:
                    end = rating[selected]
            if start or end:
                params['user_rating'] = ",".join([start,end])
            else:
                if 'user_rating' in params:
                    del params['user_rating']

        for k,v in params.items():
            if not v:
                del params[k]
        kv = ["%s=%s" % (x,params[x]) for x in params]
        tail = '&'.join(kv)
        url = head+"?"+tail
        #log(url)
        searches[name] = url

    xbmc.executebuiltin('Container.Refresh')


def find_crew(name=''):
    #people = plugin.get_storage('people')
    people = load_people()
    if not people:
        people = {}
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
    id_name = {}
    if 'name_popular' in json:
        pop = json['name_popular']
        for p in pop:
            id_name[p['id']] = p['name']
            crew.append(("[COLOR yellow]%s[/COLOR]" % p['name'],p['id']))
    if 'name_exact' in json:
        pop = json['name_exact']
        for p in pop:
            id_name[p['id']] = p['name']
            crew.append(("[COLOR green]%s[/COLOR]" % p['name'],p['id']))
    if 'name_approx' in json:
        approx = json['name_approx']
        for p in approx:
            id_name[p['id']] = p['name']
            crew.append(("[COLOR orange]%s[/COLOR]" % p['name'],p['id']))
    if 'name_substring' in json:
        pop = json['name_substring']
        for p in pop:
            id_name[p['id']] = p['name']
            crew.append(("[COLOR red]%s[/COLOR]" % p['name'],p['id']))
    names = [item[0] for item in crew]
    if names:
        index = dialog.select('Pick crew member',names)
        if index > -1:
            id = crew[index][1]
            people[id] = id_name[id]
            save_people(people)
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

@plugin.route('/title_type/<url>')
def title_type(url):
    params = {}
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

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/genres/<url>')
def genres(url):
    params = {}
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
    genres = ["action", "adventure", "animation", "biography",  "comedy", "crime", "documentary", "drama", "family", "fantasy", "film_noir", "game_show", "history", "horror", "music", "musical", "mystery", "news", "reality_tv", "romance", "sci_fi", "sport", "talk_show", "thriller", "war", "western"]
    which = d.multiselect('Genres',genres)
    if which:
        genress = [genres[x] for x in which]
        params['genres'] = ",".join(genress)
    else:
        if 'genres' in params:
            del params['genres']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/certificates/<url>')
def certificates(url):
    params = {}
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
    certificates = ["us:g","us:pg","us:pg_13","us:r","us:nc_17","gb:u" ,"gb:pg" ,"gb:12" ,"gb:12a","gb:15" ,"gb:18" ,"gb:r18"]
    which = d.multiselect('Certificates',certificates)
    if which:
        certificates = [certificates[x] for x in which]
        params['certificates'] = ",".join(certificates)
    else:
        if 'certificates' in params:
            del params['certificates']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/countries/<url>')
def countries(url):
    params = {}
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

    countries = [x[0] for x in countries_list]
    which = d.multiselect('countries',countries)
    if which:
        countries = [countries_list[x][1] for x in which]
        params['countries'] = ",".join(countries)
    else:
        if 'countries' in params:
            del params['countries']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/groups/<url>')
def groups(url):
    params = {}
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
    groups = ["top_100", "top_250", "top_1000", "now-playing-us", "oscar_winners", "oscar_best_picture_winners", "oscar_best_director_winners", "oscar_nominees", "emmy_winners", "emmy_nominees", "golden_globe_winners", "golden_globe_nominees", "razzie_winners", "razzie_nominees", "national_film_registry", "bottom_100", "bottom_250", "bottom_1000"]
    which = d.multiselect('groups',groups)
    if which:
        groups = [groups[x] for x in which]
        params['groups'] = ",".join(groups)
    else:
        if 'groups' in params:
            del params['groups']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/languages/<url>')
def languages(url):
    params = {}
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
    languages = [x[0] for x in languages_list]
    which = d.multiselect('languages',languages)
    if which:
        languages = [languages_list[x][1] for x in which]
        params['languages'] = ",".join(languages)
    else:
        if 'languages' in params:
            del params['languages']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/num_votes/<url>')
def num_votes(url):
    params = {}
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

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/release_date/<url>')
def release_date(url):
    params = {}
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

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/sort/<url>')
def sort(url):
    params = {}
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
    sort = ["moviemeter,asc", "moviemeter,desc", "alpha,asc", "alpha,desc", "user_rating,asc", "user_rating,desc", "boxoffice_gross_us,asc", "boxoffice_gross_us,desc", "num_votes,asc", "num_votes,desc", "boxoffice_gross_us,asc", "boxoffice_gross_us,desc", "runtime,asc", "runtime,desc", "year,asc", "year,desc", "release_date_us,asc", "release_date_us,desc", "my_ratings", "my_ratings,asc"]

    which = d.select('sort',sort)
    if which > -1:
        params['sort'] = sort[which]
    else:
        if 'sort' in params:
            del params['sort']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/user_rating/<url>')
def user_rating(url):
    params = {}
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
    user_rating = params.get('user_rating','')
    start = ''
    end = ''
    if user_rating:
        start,end= user_rating.split(',')
    which = d.select('User Rating',['Low','High'])
    rating = ["-"] + [str(float(x)/10.0) for x in range(10,101,1)]
    if which == 0:
        selected = d.select("Low",rating)
        if selected == 0:
            start = ''
        elif selected > 0:
            start = rating[selected]
    elif which == 1:
        selected = d.select("High",rating)
        if selected == 0:
            end = ''
        elif selected > 0:
            end = rating[selected]
    if start or end:
        params['user_rating'] = ",".join([start,end])
    else:
        if 'user_rating' in params:
            del params['user_rating']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/count/<url>')
def count(url):
    params = {}
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
    count = ["50","100"]
    which = d.select('count',count)
    if which > -1:
        params['count'] = count[which]

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))


@plugin.route('/plot/<url>')
def plot(url):
    params = {}
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
    plot = params.get('plot','')
    plot = d.input("plot",plot)
    if plot:
        params['plot'] = plot
    else:
        if 'plot' in params:
            del params['plot']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/production_status/<url>')
def production_status(url):
    params = {}
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
    production_status = ["released", "post_production", "filming", "pre_production", "completed", "script", "optioned_property", "announced", "treatment_outline", "pitch", "turnaround", "abandoned", "delayed", "indefinitely_delayed", "active", "unknown"]
    which = d.multiselect('production_status',production_status)
    if which:
        production_status = [production_status[x] for x in which]
        params['production_status'] = ",".join(production_status)
    else:
        if 'production_status' in params:
            del params['production_status']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/role/<url>')
def role(url):
    params = {}
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

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/keywords/<url>')
def keywords(url):
    params = {}
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

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/runtime/<url>')
def runtime(url):
    params = {}
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

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))


@plugin.route('/locations/<url>')
def locations(url):
    params = {}
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
    locations = params.get('locations','')
    locations = d.input("locations",locations)
    if locations:
        params['locations'] = locations
    else:
        if 'locations' in params:
            del params['locations']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/companies/<url>')
def companies(url):
    params = {}
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
    companies = params.get('companies','')
    companies = d.input("companies",companies)
    if companies:
        params['companies'] = companies
    else:
        if 'companies' in params:
            del params['companies']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/title/<url>')
def title(url):
    params = {}
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
    title = params.get('title','')
    title = d.input("Title",title)
    if title:
        params['title'] = title
    else:
        if 'title' in params:
            del params['title']

    for k,v in params.items():
        if not v:
            del params[k]

    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/boxoffice_gross_us/<url>')
def boxoffice_gross_us(url):
    params = {}
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

    for k,v in params.items():
        if not v:
            del params[k]
    kv = ["%s=%s" % (x,params[x]) for x in params]
    tail = '&'.join(kv)
    url = head+"?"+tail

    xbmc.executebuiltin('Container.Update(%s,replace)' % plugin.url_for('browse',url=url))

@plugin.route('/browse/<url>')
def browse(url):
    #people = plugin.get_storage('people')
    people = load_people()
    if not people:
        people = {}
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

    items = []
    values = []

    for p in sorted(params):
        v = params[p]
        if p == "role":
            ids = v.split(',')
            names = []
            for id in ids:
                names.append(people.get(id,id).encode("utf8"))
                #log(names)
            v = ','.join(names)
        if v:
            values.append(v)

    label = 'IMDb Search - %s' % ' '.join(values)
    context_items = []
    context_items.append(('[COLOR yellow]Add[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('add', name=label, url=url))))
    items.append(
    {
        'label': label,
        'path': plugin.url_for('title_page',url=url),
        'thumbnail':get_icon_path('search'),
        'context_menu': context_items,
    })

    iitems = []
    iitems.append(
    {
        'label': 'Certificates - ' + params['certificates'],
        'path': plugin.url_for('certificates',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Count - ' + params['count'],
        'path': plugin.url_for('count',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Countries - ' + params['countries'],
        'path': plugin.url_for('countries',url=url),
        'thumbnail':get_icon_path('settings'),
    })

    iitems.append(
    {
        'label': 'Genres - ' + params['genres'],
        'path': plugin.url_for('genres',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Languages - ' + params['languages'],
        'path': plugin.url_for('languages',url=url),
        'thumbnail':get_icon_path('settings'),
    })

    iitems.append(
    {
        'label': 'Number of Votes - ' + params['num_votes'],
        'path': plugin.url_for('num_votes',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Plot - ' + params['plot'],
        'path': plugin.url_for('plot',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Production Status - ' + params['production_status'],
        'path': plugin.url_for('production_status',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Release Date - ' + params['release_date'],
        'path': plugin.url_for('release_date',url=url),
        'thumbnail':get_icon_path('settings'),
    })

    iitems.append(
    {
        'label': 'Title - ' + params['title'],
        'path': plugin.url_for('title',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Title Type - ' + params['title_type'],
        'path': plugin.url_for('title_type',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Sort - ' + params['sort'],
        'path': plugin.url_for('sort',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Boxoffice Gross US - ' + params['boxoffice_gross_us'],
        'path': plugin.url_for('boxoffice_gross_us',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'User Rating - ' + params['user_rating'],
        'path': plugin.url_for('user_rating',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Role - ' + params['role'],
        'path': plugin.url_for('role',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Keywords - ' + params['keywords'],
        'path': plugin.url_for('keywords',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Runtime - ' + params['runtime'],
        'path': plugin.url_for('runtime',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Locations - ' + params['locations'],
        'path': plugin.url_for('locations',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Companies - ' + params['companies'],
        'path': plugin.url_for('companies',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    iitems.append(
    {
        'label': 'Groups - ' + params['groups'],
        'path': plugin.url_for('groups',url=url),
        'thumbnail':get_icon_path('settings'),
    })
    return items + sorted(iitems, key=lambda x: x["label"])

@plugin.route('/movie_search')
def movie_search():
    d = xbmcgui.Dialog()
    who = d.input("Movie Title")
    if who:
        url = "http://www.imdb.com/search/title?count=50&production_status=released&title_type=feature,tv_movie&title=%s" % who.replace(' ','+')
        return title_page(url)

@plugin.route('/tv_search')
def tv_search():
    d = xbmcgui.Dialog()
    who = d.input("TV Show Title")
    if who:
        url = "http://www.imdb.com/search/title?count=50&production_status=released&title_type=tv_series&title=%s" % who.replace(' ','+')
        return title_page(url)

@plugin.route('/name')
def name():
    d = xbmcgui.Dialog()
    who = d.input("Name")
    if who:
        url = "http://www.imdb.com/search/name?name=%s&sort=%s" % (who,plugin.get_setting('people.sort'))
        return name_page(url)

@plugin.route('/people_search')
def people_search():
    items = []
    items.append(
    {
        'label': "Name Search",
        'path': plugin.url_for('name'),
        'thumbnail':get_icon_path('unknown'),

    })

    for search in ["oscar_winners", "oscar_best_actor_nominees", "oscar_best_actor_winners", "oscar_best_actress_nominees", "oscar_best_actress_winners", "oscar_best_director_nominees", "oscar_best_director_winners", "oscar_best_supporting_actor_nominees", "oscar_best_supporting_actor_winners", "oscar_best_supporting_actress_nominees", "oscar_best_supporting_actress_winners"]:
        url = "http://www.imdb.com/search/name?count=50&groups=%s&sort=%s" % (search,plugin.get_setting('people.sort'))
        items.append(
        {
            'label': search.replace('_',' ').title(),
            'path': plugin.url_for('name_page',url=url),
            'thumbnail':get_icon_path('search'),
        })

    return items

def on_token_refreshed(response):
    plugin.set_setting( "authorization", json.dumps(response))

def authenticate():
    dialog = xbmcgui.Dialog()
    pin = dialog.input('Open a web browser at %s' % Trakt['oauth'].pin_url(), type=xbmcgui.INPUT_ALPHANUM)
    if not pin:
        return False
    authorization = Trakt['oauth'].token_exchange(pin, 'urn:ietf:wg:oauth:2.0:oob')
    if not authorization:
        return False
    plugin.set_setting( "authorization", json.dumps(authorization))
    return True


@plugin.route('/add_to_trakt_watchlist/<type>/<imdb_id>/<title>')
def add_to_trakt_watchlist(type,imdb_id,title):
    Trakt.configuration.defaults.app(
        id=8835
    )
    Trakt.configuration.defaults.client(
        id="aa1c239000c56319a64014d0b169c0dbf03f7770204261c9edbe8ae5d4e50332",
        secret="250284a95fd22e389b565661c98d0f33ac222e9d03c43b5931e03946dbf858dc"
    )
    Trakt.on('oauth.token_refreshed', on_token_refreshed)
    if not plugin.get_setting('authorization'):
        if not authenticate():
            return
    authorization = json.loads(plugin.get_setting('authorization'))
    with Trakt.configuration.oauth.from_response(authorization, refresh=True):
        result = Trakt['sync/watchlist'].add({
            type: [
                {
                    'ids': {
                        'imdb': imdb_id
                    }
                }
            ]
        })
        dialog = xbmcgui.Dialog()
        dialog.notification("Trakt: add to watchlist",title)

@plugin.route('/update_subscriptions/<kodi>')
def update_subscriptions(kodi):
    xbmcvfs.mkdirs('special://profile/addon_data/plugin.video.imdb.search/Movies')
    xbmcvfs.mkdirs('special://profile/addon_data/plugin.video.imdb.search/TV')

    subscriptions = plugin.get_storage('subscriptions')
    for w in sorted(subscriptions):
        url = subscriptions[w]
        subscription_movie_search(url,'all',"True")

    if kodi == "True":
        xbmc.executebuiltin('UpdateLibrary(video)')

@plugin.route('/subscription_movie_search/<url>/<type>/<export>')
def subscription_movie_search(url,type,export):
    count = 0
    while url:
        html = requests.get(url,headers=headers).content
        matches = re.findall('<a href="/title/(tt[0-9]*)/\?ref_=adv_li_tt"\n>(.*?)</a>\n    <span class="lister-item-year text-muted unbold">\((.*?)\)</span>',html,flags=(re.DOTALL | re.MULTILINE))
        for match in matches:
            imdb_id = match[0]
            type = "movie"
            title = match[1]
            year = match[2]
            if year.isdigit():
                add_to_library(imdb_id, type, urllib.quote_plus(title), year)
        match = re.search('<a href="(.*?)&ref_=adv_nxt"',html)
        if match:
            url = "http://www.imdb.com/search/title" + match.group(1)
        count = count + 1
        if count >= int(plugin.get_setting('search.pages')):
            break

@plugin.route('/add_to_library/<imdb_id>/<type>/<title>/<year>')
def add_to_library(imdb_id,type,title,year):
    xbmcvfs.mkdirs('special://profile/addon_data/plugin.video.imdb.search/Movies')
    xbmcvfs.mkdirs('special://profile/addon_data/plugin.video.imdb.search/TV')
    if type == "series":
        try: xbmcvfs.mkdirs('special://profile/addon_data/plugin.video.imdb.search/TV/%s' % imdb_id)
        except: pass
        update_tv_series(imdb_id)
    else:
        if plugin.get_setting('duplicates') == "false" and existInKodiLibrary(imdb_id):
            pass
        else:
            f = xbmcvfs.File('special://profile/addon_data/plugin.video.imdb.search/Movies/%s.strm' % (imdb_id), "wb")
            movie_library_url = plugin.get_setting('movie.library.url')
            meta_url = plugin.get_setting('movie.library')
            if movie_library_url == "true" and meta_url:
                meta_url = meta_url.replace("%Y",year)
                meta_url = meta_url.replace("%I",imdb_id)
                meta_url = meta_url.replace("%T",title)
            else:
                meta_url = 'plugin://%s/movies/play/imdb/%s/library' % (plugin.get_setting('catchup.plugin').lower(),imdb_id)
            f.write(meta_url.encode("utf8"))
            f.close()
            f = xbmcvfs.File('special://profile/addon_data/plugin.video.imdb.search/Movies/%s.nfo' % (imdb_id), "wb")
            str = "http://www.imdb.com/title/%s/" % imdb_id
            f.write(str.encode("utf8"))
            f.close()

def delete(path):
    dirs, files = xbmcvfs.listdir(path)
    for file in files:
        xbmcvfs.delete(path+file)
    for dir in dirs:
        delete(path + dir + '/')
    xbmcvfs.rmdir(path)

@plugin.route('/reset_folders')
def reset_folders():
    for path in ['special://profile/addon_data/plugin.video.imdb.search/Movies/','special://profile/addon_data/plugin.video.imdb.search/TV/']:
        delete(path)



@plugin.route('/update_tv')
def update_tv():
    xbmcvfs.mkdirs('special://profile/addon_data/plugin.video.imdb.search/Movies')
    xbmcvfs.mkdirs('special://profile/addon_data/plugin.video.imdb.search/TV')
    try:
        last_run  = datetime.fromtimestamp(time.mktime(time.strptime(plugin.get_setting('update_tv_time').encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        last_run = datetime(1970,1,1)
    now = datetime.now()
    next_day = last_run + timedelta(hours=24)
    next_week = last_run + timedelta(days=7)
    if now > next_week:
        update_all = True
        period = "all"
    elif now > next_day:
        update_all = False
        period = "week"
    else:
        update_all = False
        period = "day"

    plugin.set_setting('update_tv_time', str(datetime.now()).split('.')[0])

    if update_all == False:
        url = 'http://thetvdb.com/api/77DDC569F4547C45/updates/updates_%s.zip' % period
        results = requests.get(url)
        data = results.content
        try:
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            z = zip.open('updates_%s.xml'  % period)
            xml = z.read()
        except:
            return
        match = re.compile(
        '<Series><id>(.*?)</id><time>(.*?)</time></Series>',
        flags=(re.DOTALL | re.MULTILINE)
        ).findall(xml)
        ids = [id[0] for id in match]
    root = 'special://profile/addon_data/plugin.video.imdb.search/TV'
    dirs, files = xbmcvfs.listdir(root)
    for imdb_id in dirs:
        if update_all:
            update_tv_series(imdb_id)
        else:
            if imdb_id in ids:
                update_tv_series(imdb_id)


def update_tv_series(imdb_id):
    tvdb_id = get_tvdb_id(imdb_id)
    meta_url = "plugin://%s/tv/tvdb/%s" % (plugin.get_setting('catchup.plugin').lower(),tvdb_id)
    f = xbmcvfs.File('special://profile/addon_data/plugin.video.imdb.search/TV/%s/tvshow.nfo' % imdb_id,"wb")
    str = "http://thetvdb.com/index.php?tab=series&id=%s" % tvdb_id
    f.write(str.encode("utf8"))
    f.close()
    url = 'http://thetvdb.com/api/77DDC569F4547C45/series/%s/all/en.zip' % tvdb_id
    results = requests.get(url)
    data = results.content
    try:
        zip = zipfile.ZipFile(StringIO.StringIO(data))
        z = zip.open('en.xml')
        xml = z.read()
    except:
        return

    match = re.search('<FirstAired>([0-9]{4}).*?</FirstAired>',xml)
    if match:
        series_year = match.group(1)
    else:
        series_year = "1900"
    match = re.search('<SeriesName>(.*?)</SeriesName>',xml)
    if match:
        series_name = match.group(1)
    else:
        series_name = "unknown"

    tv_past = plugin.get_setting('tv_past')
    since = None
    if tv_past == "0":
        since = None
    elif tv_past == "1":
        since = timedelta(weeks=52)
    elif tv_past == "2":
        since = timedelta(weeks=4)
    elif tv_past == "3":
        since = timedelta(weeks=1)

    match = re.compile(
        '<Episode>.*?<id>(.*?)</id>.*?<EpisodeNumber>(.*?)</EpisodeNumber>.*?<FirstAired>(.*?)</FirstAired>.*?<SeasonNumber>(.*?)</SeasonNumber>.*?</Episode>',
        flags=(re.DOTALL | re.MULTILINE)
        ).findall(xml)
    for id,episode,aired,season in match:
        if (season == "0") and (plugin.get_setting('specials') == "false"):
            continue
        if aired:
            match = re.search(r'([0-9]*?)-([0-9]*?)-([0-9]*)',aired)
            if match:
                year = match.group(1)
                month = match.group(2)
                day = match.group(3)
                aired = datetime(year=int(year), month=int(month), day=int(day))
                today = datetime.today()
                if aired <= today:
                    if not since or (aired > (today - since)):
                        if plugin.get_setting('duplicates') == "false" and existInKodiLibrary(id,season,episode):
                            pass
                        else:
                            tv_library_url = plugin.get_setting('tv.library.url')
                            meta_url = plugin.get_setting('tv.library')
                            if tv_library_url == "true" and meta_url:
                                meta_url = meta_url.replace("%Y",series_year)
                                meta_url = meta_url.replace("%I",imdb_id)
                                meta_url = meta_url.replace("%T","unknown")
                                meta_url = meta_url.replace("%W",urllib.quote_plus(series_name))
                                meta_url = meta_url.replace("%S",season)
                                meta_url = meta_url.replace("%E",episode)
                                meta_url = meta_url.replace("%V",tvdb_id)
                            else:
                                meta_url = "plugin://%s/tv/play/%s/%d/%d/library" % (plugin.get_setting('catchup.plugin').lower(),tvdb_id,int(season),int(episode))
                            f = xbmcvfs.File('special://profile/addon_data/plugin.video.imdb.search/TV/%s/S%02dE%02d.strm' % (imdb_id,int(season),int(episode)),"wb")
                            f.write(meta_url.encode("utf8"))
                            f.close()


@plugin.route('/')
def index():
    searches = plugin.get_storage('searches')
    subscriptions = plugin.get_storage('subscriptions')
    items = []
    for search in searches:
        context_items = []
        context_items.append(('[COLOR yellow]Edit[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('edit_search', name=search))))
        context_items.append(('[COLOR yellow]Rename[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('rename_search', name=search))))
        context_items.append(('[COLOR yellow]Remove[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('remove_search', name=search))))
        context_items.append(('[COLOR yellow]Duplicate[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('duplicate_search', name=search))))
        context_items.append(('[COLOR yellow]Browse[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('browse_search', name=search))))
        if search in subscriptions:
            context_items.append(('[COLOR yellow]Remove Subscription[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('remove_subscription', name=search))))
        else:
            context_items.append(('[COLOR yellow]Add Subscription[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('add_subscription', name=search, url=searches[search]))))
        items.append(
        {
            'label': search,
            'path': plugin.url_for('title_page',url=searches[search]),
            'thumbnail':get_icon_path('search'),
            'context_menu': context_items,
        })
    context_items = []
    context_items.append(('[COLOR yellow]Update IMDb Library[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('update_subscriptions',kodi=True))))
    context_items.append(('[COLOR yellow]Delete Movie/TV Folders[/COLOR]', 'XBMC.RunPlugin(%s)' % (plugin.url_for('reset_folders'))))
    items.append(
    {
        'label': "Browse",
        'path': plugin.url_for('browse', url="http://www.imdb.com/search/title?count=50&production_status=released"),
        'thumbnail':get_icon_path('unknown'),
        'context_menu': context_items,
    })
    items.append(
    {
        'label': "People",
        'path': plugin.url_for('people_search'),
        'thumbnail':get_icon_path('unknown'),

    })
    items.append(
    {
        'label': "Simple Movie Title Search",
        'path': plugin.url_for('movie_search'),
        'thumbnail':get_icon_path('search'),

    })
    items.append(
    {
        'label': "Simple TV Show Title Search",
        'path': plugin.url_for('tv_search'),
        'thumbnail':get_icon_path('search'),

    })
    items.append(
    {
        'label': "[COLOR dimgray]Add Search[/COLOR]",
        'path': plugin.url_for('add_search'),
        'thumbnail':get_icon_path('settings'),

    })
    if plugin.get_setting('export') == 'true':
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
    #sort_methods = ['label', 'title', ('date', '%D')]
    #plugin.finish(items, sort_methods=sort_methods,cache_to_disc=False,view_mode="thumbnail")
    #plugin.finish(items, cache_to_disc=False)


if __name__ == '__main__':

    plugin.run()
    if big_list_view == True:
        view_mode = int(plugin.get_setting('view'))
        if view_mode:
            #pass
            plugin.set_view_mode(view_mode)
            #plugin.set_content("episodes")
            #xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    #content = "movies"
    #xbmcplugin.setContent(int(sys.argv[1]), content)
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_MPAA_RATING)
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    #plugin.set_view_mode(51)