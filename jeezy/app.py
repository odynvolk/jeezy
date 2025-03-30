import asyncio
import os
import random
import time

from dotenv import load_dotenv
from timeit import default_timer as timer
import nodriver as uc


load_dotenv()

class Jeezy(object):
    def __init__(self):
        self.times = int(os.getenv("TIMES"))
        self.user_agents = []
        self.urls = []

        with open(os.getenv("USER_AGENTS"), "r") as file:
            for line in file:
                self.user_agents.append(line.strip())

        with open(os.getenv("URLS"), "r") as file:
            for line in file:
                self.urls.append(line.strip())


    async def run(self):
        print("Run")
        for x in range(self.times):
            user_agent = random.sample(self.user_agents, 1)[0]
            url = random.sample(self.urls, 1)[0]
            print(user_agent)
            print(url)
            print("------------------------------------------")
            try:
                # browser_args = [f'--user-agent={user_agent}', f'--proxy-server={proxy}', "--headless"]
                browser_args = [f'--user-agent={user_agent}', "--headless"]
                driver = await uc.start(browser_args=browser_args)
                tab = await driver.get(url)
                await driver.sleep(7)
                await tab.scroll_down(200)
                await driver.sleep(2)
                reject = await tab.find("Reject all", best_match=True)
                await driver.sleep(2)
                await tab.scroll_down(100)
                await reject.click()
                await driver.sleep(2)
                await tab.scroll_up(300)
                await driver.sleep(1300)
                driver.stop()

                time.sleep(120 * 60)
            except Exception as e:
              print(e)

        print("Done!")


if __name__ == "__main__":
    import traceback

    try:
        jeezy = Jeezy()
        asyncio.run(jeezy.run())
    except Exception:
        print(traceback.format_exc())
