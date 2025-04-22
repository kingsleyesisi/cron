import asyncio
import aiohttp
import time

URL = 'url:url//url'
COMPLETED = 0
REQUEST_PER_SECOND = 1000

TEST_DURATION = 6000 # 1 minute

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
        task = [self.send_request(session=session, url=url) for _ in range(num_requests)]
        await asyncio.gather(*task)
        success_count = sum(1 for result in task if result is not None)
        failure_count = num_requests - success_count
        return success_count, failure_count

    async def main(self):
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            while time.time() - start_time < TEST_DURATION:
                success_count, failure_count = await self.load_test(session=session, url=URL, num_requests=REQUEST_PER_SECOND)
                print(f"Success count: {success_count}, Failure count: {failure_count}")
                print(f'send {REQUEST_PER_SECOND} requests in 1 second')
                done = COMPLETED + success_count
                print(done)
                await asyncio.sleep(1- (time.time() % 1))

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
    await asyncio.gather(*tasks)
    success_count = sum(1 for result in tasks if result is not None)
    failure_count = num_requests - success_count
    return success_count, failure_count

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetTest().main())
    loop.close()
