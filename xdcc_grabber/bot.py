import asyncio
import random
import ssl
import struct
import os
import irc3


class XDCCGet(irc3.dcc.client.DCCGet):
    def data_received(self, data):
        self.set_timeout()
        self.fd.write(data)
        self.bytes_received += len(data)
        self.transport.write(struct.pack("!Q", self.bytes_received))

    @staticmethod
    async def initiate(bot, mask, target, size, host, port):
        return bot.context.dcc.create(
            XDCCGet, mask, filepath=target, filesize=int(size),
            host=host, port=port)


@irc3.plugin
class XDCCBot:
    def __init__(self, context):
        self.context = context

    @irc3.event(irc3.rfc.CONNECTED)
    def connected(self, **_):
        self.context.log.info("Bot connected")

        channel = self.context.config["channel"]
        self.context.join(channel)

        request = "XDCC GET " + str(self.context.config["pack_nr"])
        self.context.privmsg(self.context.config["peer"], request)
        self.context.log.info("Pack has been requested")

    @irc3.event(irc3.rfc.CTCP)
    async def on_ctcp(self, mask=None, **kwargs):
        if kwargs["ctcp"] == "VERSION":
            self.context.send_line("VERSION " + self.context.config.client_id)
            return

        name, host, port, size, *_ = kwargs["ctcp"].split()[2:]
        self.context.log.info("%s is offering %s", mask.nick, name)

        target = os.path.join('/tmp', name)

        conn = await self.context.create_task(
            XDCCGet.initiate(self, mask, target, size, host, port))
        await conn.closed

        self.context.log.info("file received from %s", mask.nick)
        self.context.config.file_received.set_result(True)

    @ staticmethod
    def fetch(pack):
        loop = asyncio.get_event_loop()
        file_received = asyncio.Future()

        nick = "AcMe" + str(hex(random.randrange(0x1337)))[2:]
        cfg = {
            "host": pack["network"],
            "port": 6697,
            "channel": pack["channel"],
            "peer": pack["bot"],
            "pack_nr": pack["packnum"],
            "ssl": True,
            "ssl_verify": ssl.CERT_NONE,
            "includes": ["irc3.plugins.core", __name__],
            "loop": loop,
            "file_received": file_received,
            "client_id": "Irssi 0.8.19 (20160323) - http://irssi.org/",
            "verbose": False,
            "raw": False}

        for k in ("nick", "username", "realname"):
            cfg[k] = nick

        receiver = irc3.IrcBot.from_config(cfg)
        loop.call_soon(receiver.run, False)
        loop.run_until_complete(file_received)
