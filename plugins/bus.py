import logging
import posixpath
import requests
import arrow
from functools import partial
from errbot import BotPlugin, botcmd
from apscheduler.scheduler import Scheduler
from BeautifulSoup import BeautifulSoup


STOPS = {
    'xmassteps': 'bstgajt',
    'centre': 'bstgajp',
    'hippodrome': 'bstdwmd',
    'kennave': 'bstjawt',
    'peache': 'sglgdgd',
    'rupert' : 'bstpaga'
}


class Bus(BotPlugin):
    def activate(self):
        super(Bus, self).activate()
        self.sched = Scheduler(coalesce=True)
        self.sched.start()

    @botcmd(split_args_with=' ')
    def bus(self, mess, args):
        
        argsLength = len(args)
        if argsLength < 2 :
            route = 49
        else :
            route = args[1]
        now = arrow.now()
        t = self.next_bus(*args)
        if t:
            return 'The next no. %s bus leaves from %s %s' % (
                route,
                args[0],
                t.humanize(now)
            )

    @botcmd(split_args_with=' ')
    def bus_remind(self, mess, args):
        t = self.next_bus(*args)
        reminder = t.replace(minutes=-10)
        remind = partial(self.remind, mess, args)
        self.sched.add_date_job(remind, reminder.naive)
        return "%s: you'll be reminded %s" % (
            mess.getMuckNick(),
            reminder.humanize()
        )

    def remind(self, mess, args):
        now = arrow.now()
        t = self.next_bus(args[0], args[1])
        if t:
            self.send(
                mess.getFrom(),
                '%s: the next no. %s bus leaves from %s %s' % (
                    mess.getMuckNick(),
                    args[1],
                    args[0],
                    t.humanize(now)
                ),
                message_type=mess.getType()
            )

    def parse_timetable(self, stop, route):
        if stop in STOPS:
            stop = STOPS[stop]

        url = posixpath.join(
            "http://www.nextbuses.mobi",
            "WebView/BusStopSearch/BusStopSearchResults/",
            stop
        )

        res = requests.get(
            url,
            params={'searchType': 'route', 'searchFilter': route}
        )

        soup = BeautifulSoup(res.text)
        bus_stops = soup.findAll('table', {'class': 'BusStops'})
        times = bus_stops[0].findAll('p', {'class': 'Stops'}) #should loop instead of return one
        return times

    def next_bus(self, stop, route=49, time=0):
        times = self.parse_timetable(stop, route)
        now = arrow.now()
        then = now.replace(minutes=+int(time))

        for i in times:
            logging.info(i.text)
            if 'DUE' in i.text:
                continue
            elif ';at ' in i.text:
                t = i.text.split('at ')[-1].strip().split(':')
                next = now.replace(hour=int(t[0]), minute=int(t[1]))
            else:
                t = i.text.split('in ')[-1].strip().split()
                next = now.replace(minutes=int(t[0]))
            if next > then:
                return next
        return False
