from errbot import BotPlugin, botcmd
from httplib import responses


class Http(BotPlugin):
    @botcmd(split_args_with=' ')
    def http(self, mess, args):
        if int(args[0]) in responses:
            return 'http %s means: %s' % (args[0], responses[int(args[0])])
        else:
            return "You silly goose! %s isn't in the http spec, maybe a non-standard one?" % (args[0])
