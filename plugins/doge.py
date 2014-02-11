import config
from pyimgur import Imgur
from errbot import BotPlugin, botcmd


class Doge(BotPlugin):
    @botcmd
    def doge(self, mess, args):
        words = []
        msg = mess.getBody()
        if ',' in msg:
            msg = msg.replace(' ', '')
            msg = msg.replace('%sdoge' % config.__dict__['BOT_PREFIX'], '')
            words = msg.split(',')
        else:
            split_words = ['such', 'many', 'great', 'much', 'very']
            # such power many things great evil wow
            # wow very error parsing such sorry
            line = ''
            for w in msg.split(' '):
                if w in split_words:
                    words.append(line.strip())
                    line = w
                elif w == 'wow':
                    words.append(line.strip())
                    words.append('wow')
                else:
                    line = ''.join([line, w])
        return self.get_link(words)

    def get_link(self, words):
        key = config.__dict__.get(u'IMGUR_ID', False)
        if key:
            imgur = Imgur(key)
            words = '/'.join(words)
            try:
                doge = imgur.upload_image(url="http://dogr.io/%s/wow.png" % words)
                return doge.link
            return "No upload, so unfulfil, much sad, very broken, wow"
