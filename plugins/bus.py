from errbot import BotPlugin, botcmd
from apscheduler.scheduler import Scheduler
from BeautifulSoup import BeautifulSoup
import logging
import requests
import posixpath
import arrow


STOPS = {
    'centre': 'bstgajt',
}


class Bus(BotPlugin):
    def activate(self):
        super(Bus, self).activate()
        self.sched = Scheduler(coalesce=True)
        self.sched.start()
        logging.info(self.sched.get_jobs())

    @botcmd
    def bus(self, mess, args):
        logging.info(args)
        return self.response(*args.split())

    @botcmd
    def remind(self, mess, args):
        logging.info(self.sched.get_jobs())

    def parse_timetable(self, stop, route):
        url = posixpath.join(
            "http://www.nextbuses.mobi",
            "WebView/BusStopSearch/BusStopSearchResults/",
            STOPS[stop]
        )

        res = requests.get(
            url,
            params={'searchType': 'route', 'searchFilter': route}
        )

        soup = BeautifulSoup(res.text)
        bus_stops = soup.findAll('table', {'class': 'BusStops'})
        times = bus_stops[0].findAll('p', {'class': 'Stops'})
        return times

    def response(self, stop, route, time=0):
        times = self.parse_timetable(stop, route)
        now = arrow.now()
        then = now.replace(minutes=int(time))

        for i in times:
            t = i.text.split('in ')[-1].split('at ')[-1].strip()
            if time > 0:
                if ';at ' in i.text:
                    t = i.text.split('at ')[-1].strip().split(':')
                    next = now.replace(hours=int(t[0]), minutes=int(t[1]))
                else:
                    t = i.text.split('in ')[-1].strip().split()
                    next = now.replace(minutes=int(t[0]))
                # work out the delta
                if next > then:
                    return 'The next no. %s bus leaves from %s in %s' % (
                        route,
                        stop,
                        next.humanize(now)
                    )
            else:
                #return the first item
                return 'The next no. %s bus leaves from %s in %s' % (
                    route,
                    stop,
                    t
                )
