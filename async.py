import asyncio
import aiohttp
import time
from typing import Tuple
URLS = [
    "https://www.baidu.com",
    "https://www.bilibili.com",
    "https://github.com",
    "https://www.csdn.net",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/status/500",
    "https://not-exist-site.example.invalid"
]

result_queue = asyncio.Queue(maxsize=10)
SEMAPHORE = asyncio.Semaphore(3)

async def fetch(session ,url):
    async with SEMAPHORE:
        start=time.time()
        try :
            async with session.get(url) as resp:
                await resp.text()
                cost = time.time() -start
            return  url,cost , resp.status ,"ok"
        except Exception as e:
            cost = time.time() -start
            return url, cost , None ,str(e)

async def worker (url):
    async with aiohttp.ClientSession() as session:
        result=await fetch(session , url)
        await result_queue.put(result)

async def log_printer():
    """独立协程：消费队列，打印结果 + 统计信息"""
    success = 0
    fail = 0
    total = len(URLS)
    while success + fail < total:
        url, status, cost, msg = await result_queue.get()
        if msg == "ok":
            print(f"✅ 成功 | {url:40} status={status}, 耗时={cost:.2f}s")
            success +=1
        else:
            print(f"❌ 失败 | {url:40} err={msg}")
            fail +=1
        result_queue.task_done()
    print(f"\n===== 汇总：成功{success} 失败{fail} =====")

async def main ():
    print("开始异步站点监控...\n")
    tasks = [asyncio.create_task(worker(url)) for url in URLS]
    log_task = asyncio.create_task(log_printer())
    await asyncio.gather(*tasks)
    await log_task


if __name__ == "__main__":
    asyncio.run(main())
