import asyncio
import random
import ssl
import struct
import irc3


class XDCCGet(irc3.dcc.client.DCCGet):
    def connection_made(self, transport):
        super(irc3.dcc.client.DCCGet, self).connection_made(transport)
        if self.resume:
            self.bytes_received = self.offset
        else:
            self.bytes_received = 0

    def data_received(self, data):
        self.set_timeout()

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.ws.send_bytes(data))
        task.add_done_callback(lambda t: t.result())

        self.bytes_received += len(data)
        self.transport.write(struct.pack("!Q", self.bytes_received))

    @staticmethod
    async def initiate(xdcc_bot, mask, filepath, filesize, host, port, ws):
        return xdcc_bot.bot.dcc.create(
            XDCCGet, mask, filepath=filepath, filesize=filesize,
            host=host, port=port, ws=ws)


@irc3.plugin
class XDCCBot():
    cfg = {
        "port": 6697,
        "ssl": True,
        "ssl_verify": ssl.CERT_NONE,
        "includes": ["irc3.plugins.core", __name__],
        "client_id": "Irssi 0.8.19 (20160323) - http://irssi.org/",
        "verbose": True,
        "raw": False}

    def __init__(self, bot=None):
        self.bot = bot

    @irc3.event(irc3.rfc.CONNECTED)
    def connected(self, **_):
        self.bot.log.info("Bot connected")

        for channel in self.bot.config["channels"].split(','):
            self.bot.join(channel)

        request = "XDCC GET " + str(self.bot.config["pack_nr"])
        self.bot.privmsg(self.bot.config["peer"], request)

        self.bot.log.info("Pack has been requested")

    @irc3.event(irc3.rfc.CTCP)
    async def on_ctcp(self, mask=None, **kwargs):
        if kwargs["ctcp"] == "VERSION":
            self.bot.send_line("VERSION " + self.bot.config.client_id)
            return

        name, host, port, size, *_ = kwargs["ctcp"].split()[2:]
        self.bot.log.info("%s is offering %s", mask.nick, name)

        ws = self.bot.config.ws
        conn = await self.bot.create_task(
            XDCCGet.initiate(self, mask, 'foo', int(size), host, port, ws))
        await conn.closed

        self.bot.config.file_received.set_result(True)
        self.bot.log.info("file received from %s", mask.nick)

    async def forward(self, pack, websocket):
        loop = asyncio.get_event_loop()
        file_received = asyncio.Future()

        nick = "AcMe" + str(hex(random.randrange(0x1337)))[2:]
        for k in ("nick", "username", "realname"):
            XDCCBot.cfg[k] = nick

        self.receiver = irc3.IrcBot.from_config(
            XDCCBot.cfg,
            host=pack["network"],
            channels=pack["channels"],
            peer=pack["bot"],
            pack_nr=pack["packnum"],
            loop=loop,
            ws=websocket,
            file_received=file_received)

        self.receiver.run(forever=False)

        await file_received

    # TODO fix, this is hacky AF
    async def terminate(self):
        def cb(self): pass
        self.receiver.protocol.connection_lost = cb

        # self.receiver.protocol.close()
        self.receiver.protocol.transport.abort()
        self.receiver.protocol.transport.close()

        # self.receiver.notify('SIGINT')
        # self.receiver.quit('INT')

        for task in asyncio.all_tasks():
            if 'IrcBot' in str(task):
                try:
                    task.cancel()
                    await task
                except asyncio.CancelledError:
                    pass
