from random import choice
from errbot import BotPlugin, botcmd


class Doge(BotPlugin):
    @botcmd
    def duck(self, mess, args):
        suggestions = [
            "ok...",
            "tell me more",
            "hmm, odd",
            "interesting",
            "oh, odd...",
            "have you tried adding prints?",
            "have you tried firing up the debugger?",
            "have you tried telling someone who actually cares?",
            "you realise you're talking to a bot, right?"
        ]
        return choice(suggestions)
