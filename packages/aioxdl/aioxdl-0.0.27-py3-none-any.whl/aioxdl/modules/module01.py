import time, aiohttp, asyncio
from ..functions import Hkeys
from ..scripts import Scripted
from yt_dlp import YoutubeDL, DownloadError
#=========================================================================================================

class Aioxdl:

    def __init__(self, chunk=1024, timeout=1000, message=None):
        self.dsizes = 0
        self.tsizes = 0
        self.errors = None
        self.chunks = chunk
        self.otimes = timeout
        self.mesage = message
        self.stimes = time.time()
        self.comand = Hkeys.DATA01
        self.fnames = Hkeys.DATA02

#=========================================================================================================

    async def download(self, url, location, progress):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=self.otimes) as response:
                self.tsizes += await self.getsizes(response)
                with open(location, "wb") as handlexo:
                    while True:
                        chunks = await response.content.read(self.chunks)
                        if not chunks:
                            break
                        handlexo.write(chunks)
                        self.dsizes += self.chunks
                        try: await self.display(progress)
                        except ZeroDivisionError: pass
                        except Exception as errors:
                            self.errors = errors
                            break

                await response.release()
                return location if location else None

#=========================================================================================================

    async def filename(self, filelink):
        with YoutubeDL(self.comand) as ydl:
            try:
                resultse = ydl.extract_info(filelink, download=False)
                filename = ydl.prepare_filename(resultse, outtmpl=self.fnames)
            except DownloadError:
                filename = Scripted.DATA02
            except Exception:
                filename = Scripted.DATA02

            return filename

#=========================================================================================================

    async def getsizes(self, response):
        return int(response.headers.get("Content-Length", 0))

#=========================================================================================================

    async def display(self, progress):
        if progress and self.mesage:
            await progress(self.stimes, self.tsizes, self.dsizes, self.mesage)
        elif progress:
            await progress(self.stimes, self.tsizes, self.dsizes)
        else: pass

#=========================================================================================================

    async def start(self, url, location, progress=None):
        try:
            location = await self.download(url, location, progress)
        except aiohttp.ClientConnectorError as errors:
            self.errors = errors
        except asyncio.TimeoutError:
            self.errors = Scripted.DATA01
        except Exception as errors:
            self.errors = errors

        return location

#=========================================================================================================
