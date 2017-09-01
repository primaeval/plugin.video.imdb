# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcvfs, xbmcaddon
import time
import requests
import base64
import time, datetime

ADDON = xbmcaddon.Addon('plugin.video.imdb.search')

def log(x):
    xbmc.log(repr(x))

def Service():
    xbmc.log("[plugin.video.imdb.search] Background Update Starting...", xbmc.LOGNOTICE)
    time.sleep(1)
    xbmc.log('[IMDb Advanced Search] Updating Subscriptions', level=xbmc.LOGNOTICE)
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.imdb.search/update_subscriptions/False)')
    if ADDON.getSetting('update.tv') == "true":
        xbmc.log('[IMDb Advanced Search] Updating TV Shows', level=xbmc.LOGNOTICE)
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.imdb.search/update_tv)')
    now = datetime.datetime.now()
    if ADDON.getSetting('update.main') == "true":
        while (xbmc.getCondVisibility('Library.IsScanningVideo') == True):
            time.sleep(1)
            if xbmc.abortRequested:
                return
        xbmc.log('[IMDb Advanced Search] Updating Kodi Library', level=xbmc.LOGNOTICE)
        xbmc.executebuiltin('UpdateLibrary(video)')
    if ADDON.getSetting('update.clean') == "true":
        time.sleep(1)
        while (xbmc.getCondVisibility('Library.IsScanningVideo') == True):
            time.sleep(1)
            if xbmc.abortRequested:
                return
        xbmc.log('[IMDb Advanced Search] Cleaning Kodi Library', level=xbmc.LOGNOTICE)
        xbmc.executebuiltin('CleanLibrary(video)')



if __name__ == '__main__':

    try:
        if ADDON.getSetting('login.update') == 'true':
            Service()
            ADDON.setSetting('last.background.update', str(time.time()))
        if ADDON.getSetting('service.type') != '0':
            monitor = xbmc.Monitor()
            xbmc.log("[plugin.video.imdb.search] Background service started...", xbmc.LOGDEBUG)
            while not monitor.abortRequested():
                if ADDON.getSetting('service.type') == '1':
                    interval = int(ADDON.getSetting('service.interval'))
                    waitTime = 3600*interval
                    ts = ADDON.getSetting('last.background.update') or "0.0"
                    lastTime = datetime.datetime.fromtimestamp(float(ts))
                    now = datetime.datetime.now()
                    nextTime = lastTime + datetime.timedelta(seconds=waitTime)
                    td = nextTime - now
                    timeLeft = td.seconds + (td.days * 24 * 3600)
                    xbmc.log("[plugin.video.imdb.search] Service waiting for interval %s" % waitTime, xbmc.LOGDEBUG)
                else:
                    next_time = ADDON.getSetting('service.time')
                    if next_time:
                        hour,minute = next_time.split(':')
                        now = datetime.datetime.now()
                        next_time = now.replace(hour=int(hour),minute=int(minute),second=0,microsecond=0)
                        if next_time < now:
                            next_time = next_time + datetime.timedelta(hours=24)
                        td = next_time - now
                        timeLeft = td.seconds + (td.days * 24 * 3600)
                if timeLeft < 0:
                    timeLeft = 0
                xbmc.log("[plugin.video.imdb.search] Service waiting for %d seconds" % timeLeft, xbmc.LOGDEBUG)
                if timeLeft and monitor.waitForAbort(timeLeft):
                    break
                xbmc.log("[plugin.video.imdb.search] Service now triggered...", xbmc.LOGDEBUG)
                Service()
                now = time.time()
                ADDON.setSetting('last.background.update', str(now))

    except Exception, ex:
        xbmc.log('[plugin.video.imdb.search] Uncaught exception in service.py: %s' % str(ex), xbmc.LOGDEBUG)
