import os, asyncio
from websockets.asyncio.server import serve
from websockets.datastructures import Headers
from websockets.http11 import Response

TARGETS = {"/vm1": ("10.81.0.10", 22), "/vm2": ("10.81.0.13", 22)}

async def handler(ws):
    path = ws.request.path.split("?")[0]
    host, port = TARGETS.get(path, TARGETS["/vm1"])
    reader, writer = await asyncio.open_connection(host, port)
    async def tcp_to_ws():
        try:
            while True:
                data = await reader.read(65536)
                if not data:
                    break
                await ws.send(data)
        except Exception:
            pass
        try:
            await ws.close()
        except Exception:
            pass
    async def ws_to_tcp():
        try:
            async for msg in ws:
                if isinstance(msg, str):
                    msg = msg.encode()
                writer.write(msg)
                await writer.drain()
        except Exception:
            pass
        try:
            writer.close()
        except Exception:
            pass
    await asyncio.gather(tcp_to_ws(), ws_to_tcp())

async def process_request(connection, request):
    if request.headers.get("Upgrade", "").lower() != "websocket":
        return Response(200, "OK", Headers([("Content-Type", "text/plain")]), b"relay up\n")
    return None

async def main():
    port = int(os.environ.get("PORT", "8080"))
    async with serve(handler, "0.0.0.0", port, process_request=process_request, max_size=None):
        await asyncio.Future()

asyncio.run(main())
