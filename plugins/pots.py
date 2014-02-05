from errbot import BotPlugin
from random import choice
from apscheduler.scheduler import Scheduler
import logging


class FreshPots(BotPlugin):

    pots = [
        'http://i.imgur.com/Q2b54vc.jpg',
        'http://i.imgur.com/SYsdsew.jpg',
        'http://i.imgur.com/caIbQMh.png',
        'http://i.imgur.com/MCwiikl.jpg',
        'http://i.imgur.com/g4sFHwz.jpg',
        'http://i.imgur.com/vnuJQ4S.gif',
        'http://i.imgur.com/cm3Y6jX.jpg',
        'http://i.imgur.com/ZcKZTFU.jpg',
        'http://i.imgur.com/4mEaNIp.jpg',
        'http://i.imgur.com/gDukRFu.png',
        'http://i.imgur.com/1MDO9fV.png',
        'http://i.imgur.com/U5cFX3M.jpg'
    ]

    def activate(self):
        super(FreshPots, self).activate()
        sched = Scheduler(coalesce=True)
        sched.start()
        sched.add_cron_job(
            self.fresh_pots,
            kwargs={'message': 'fresh pots time'},
            day_of_week='mon-fri',
            hour=11)
        sched.add_cron_job(
            self.fresh_pots,
            kwargs={'message': 'fresh pots time'},
            day_of_week='mon-fri',
            hour=15)
        logging.info(sched.get_jobs())

    def callback_message(self, conn, mess):
        body = mess.getBody().lower()
        if body.find('coffee') != -1 or body.find('fresh pots') != -1:
            self.fresh_pots(mess.getFrom())

    def fresh_pots(self, channel='#cloudant-bristol', message=None):
            if message:
                self.send(
                    channel,
                    message,
                    message_type='groupchat'
                )

            self.send(
                channel,
                choice(self.pots),
                message_type='groupchat'
            )
