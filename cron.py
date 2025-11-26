import asyncio
import sys
import time

try:
    import aiohttp
except Exception:
    print("Missing dependency: aiohttp is not installed. Install it with `pip install aiohttp`.")
    sys.exit(1)

URL = 'https://benefitsmart.online/'
COMPLETED = 0
REQUEST_PER_SECOND = 1

TEST_DURATION = 720 # 3 minute

DATA = {

}

class GetTest:

    def __init__(self):
        self.session = None
    # for get request
    async def send_request(self, session, url):
        try:
            async with session.get(url) as response:
                return response.status
        except Exception as e:
            print(f"Request failed: {e}")
            return None
        

    # for load test

    async def load_test(self, session, url, num_requests):
        tasks = [self.send_request(session=session, url=url) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        success_count = sum(1 for result in results if result is not None)
        failure_count = num_requests - success_count
        return success_count, failure_count

    async def main(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            start_time = time.time()
            while time.time() - start_time < TEST_DURATION:
                success_count, failure_count = await self.load_test(session=session, url=URL, num_requests=REQUEST_PER_SECOND)
                print(f"Success count: {success_count}, Failure count: {failure_count}")
                print(f'send {REQUEST_PER_SECOND} requests in 1 second')
                done = COMPLETED + success_count
                print(done)
                await asyncio.sleep(max(0, 1 - (time.time() % 1)))

            print("Load test completed.")


    async def main2(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            start_time = time.time()
            while time.time() - start_time < TEST_DURATION:
                success_count, failure_count = await self.load_test(session=session, url='https://cusbank.com', num_requests=REQUEST_PER_SECOND)
                print(f"Success count: {success_count}, Failure count: {failure_count}")
                print(f'send {REQUEST_PER_SECOND} requests in 1 second')
                done = COMPLETED + success_count
                print(done)
                await asyncio.sleep(max(0, 1 - (time.time() % 1)))

            print("Load test completed.")

    # Check how much a server can handle a post request
    async def send_post_request(self, session, url, data):
        try:
            async with session.post(url, json=data) as response:
                return response.status
        except Exception as e:
            print(f"POST request failed: {e}")
            return None

    async def post_load_test(self, session, url, num_requests, data):
        tasks = [self.send_post_request(session=session, url=url, data=data) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        success_count = sum(1 for result in results if result is not None)
        failure_count = num_requests - success_count
        return success_count, failure_count

async def _runner():
    tester = GetTest()
    # run main then main2 sequentially in the same event loop
    await tester.main()
    await tester.main2()

if __name__ == "__main__":
    asyncio.run(_runner())
