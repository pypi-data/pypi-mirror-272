import aiohttp
import asyncio
from .Types import Response as _Response, Request as _Request, Config as _Config

class Connection:
    def __init__(self, request: _Config):
        self.connector = aiohttp.TCPConnector(limit=request.max_connection_limit)  # Set connection limit
    async def sendRequest(self, request: _Request):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=_Config.timeout)) as session:
            tasks = [self._sendRequest(request=request, session=session) for _ in range(request.amount)]
            return await asyncio.gather(*tasks) ## send Requests, and return them as generator.

    async def _sendRequest(self, session: aiohttp.ClientSession, request: _Request):
        try:
            async with session.request(
                    method=request.method, url=request.url,
                    headers=request.headers, json=request.json,
                    data=request.data, params=request.params
            ) as response:
                response.raise_for_status()
                content_type = response.headers.get('content-type')
                json_content = None
                if content_type and 'application/json' in content_type:
                    json_content = await response.json()
                return _Response(
                    status=response.status, url=str(response.url),
                    headers=response.headers, json=json_content,
                    text=await response.text(), content=await response.read()
                )
        except (aiohttp.ClientError, aiohttp.ServerTimeoutError) as e:
            return _Response(status=609, url=request.url, headers={}, content=str(e), exception=True)
        except Exception as e:
            return _Response(status=609, url=request.url, headers={}, content=str(e), exception=True)

