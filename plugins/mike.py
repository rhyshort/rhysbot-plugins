from errbot import BotPlugin
from random import randint
import config


class Mike(BotPlugin):
    count = 0

    def callback_message(self, conn, mess):
        if mess:
            nick = mess.getMuckNick()
            if nick:
                s = nick.find(
                    config.__dict__['BOT_IDENTITY']['nickname']
                )
                if mess.getBody().find('mikewallace') != -1 and s == -1:
                    self.count += 1
                    if self.count > 1 and randint(1, 5) == 1:
                        for i in xrange(randint(3, 15)):
                            self.send(
                                mess.getFrom(),
                                "mikewallace",
                                message_type=mess.getType()
                            )
                        self.count = 0
                else:
                    self.count = 0
