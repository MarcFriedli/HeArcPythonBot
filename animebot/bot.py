import asyncio
import json
import aiohttp
import configparser


URL = "https://discordapp.com/api"
config = configparser.ConfigParser()
config.read('../config.ini')
token = config['animebot']['TOKEN']

async def api_call_main(path):
    """Return the JSON body of a call to Discord REST API (need some refactoring)."""
    with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}{path}") as response:
            if 200 == response.status:
                return await response.json()
            elif 204 == response.status:
                return {}
            else:
                body = await response.text()
                raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")

async def api_call(path, method="GET", **kwargs):
    """Return the JSON body of a call to Discord REST API (need refactoring."""
    defaults = {
        "headers": {
            "Authorization": f"Bot {token}",
            "User-Agent": "dBot (https://discordapp.com/api, 0.1)"
        }
    }
    kwargs = dict(defaults, **kwargs)
    print(kwargs)
    with aiohttp.ClientSession() as session:
        async with session.request(method, path, **kwargs) as response:
            if 200 == response.status:
                return await response.json()
            elif 204 == response.status:
                return {}
            else:
                body = await response.text()
                raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")

async def start(url):
    with aiohttp.ClientSession() as session:
        async with session.ws_connect(
                f"{url}?v=6&encoding=json") as ws:
            async for msg in ws:
                data = json.loads(msg.data)
                if data["op"] == 10:  # Hello
                    asyncio.ensure_future(heartbeat(
                        ws,
                        data['d']['heartbeat_interval']))
                    await ws.send_json({
                        "op": 2,  # Identify
                        "d": {
                            "token": token,
                            "properties": {},
                            "compress": False,
                            "large_threshold": 250
                        }
                    })
                elif data["op"] == 11:  # Heartbeat ACK
                    pass
                elif data["op"] == 0:  # Dispatch
                    print(data['t'], data['d'])
                else:
                    print(data)

last_sequence = None

async def heartbeat(ws, interval):
    """Send every interval ms the heatbeat message."""
    while True:
        await asyncio.sleep(interval / 1000)  # seconds
        await ws.send_json({
            "op": 1,  # Heartbeat
            "d": last_sequence
        })

async def send_message(recipient_id, content):
    """Send a message with content to the recipient_id."""
    channel = await api_call("/users/@me/channels", "POST",
                             json={"recipient_id": recipient_id})
    return await api_call(f"/channels/{channel['id']}/messages",
                          "POST",
                          json={"content": content})

async def main():
    """Main program."""
    response = await api_call_main('/gateway')
    await start(response["url"])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
