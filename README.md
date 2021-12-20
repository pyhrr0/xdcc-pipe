# Introduction
This microservice allows you to fetch XDCC packs.

# Usage

```
usage: xdcc-pipe [-h] [-f OUTPUT_FILE] [-n NETWORK] [-c CHANNEL] [-b BOT] [-p PACK_NUM] [-u WS_URL] [-v] {server,client}

positional arguments:
  {server,client}       mode

options:
  -h, --help            show this help message and exit
  -f OUTPUT_FILE, --output-file OUTPUT_FILE
  -n NETWORK, --network NETWORK
                        network to connect to
  -c CHANNEL, --channel CHANNEL
                        channel(s) to join
  -b BOT, --bot BOT     bot to request pack from
  -p PACK_NUM, --pack-num PACK_NUM
                        pack number to request
  -u WS_URL, --ws-url WS_URL
                        address to serve on / connect to
  -v, --verbose         verbose output
```

## Installation

Create and load a virtualenv:
``` bash
python3 -m venv ~/my_env
source ~/my_env/bin/activate
```

Fetch sources:
``` bash
git clone https://github.com/pyhrr0/xdcc-pipe ~/my_env/
```

Install package and its dependencies:
``` bash
pip install ~/my_env/xdcc-pipe
```
