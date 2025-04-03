import asyncio
import datetime
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
        self.stay_on_page_in_minutes = int(os.getenv("STAY_ON_PAGE_IN_MINUTES"))
        self.sleep_between_runs_in_minutes = int(os.getenv("SLEEP_BETWEEN_RUNS_IN_MINUTES"))
        self.user_agents = []
        self.urls = []

        with open(os.getenv("USER_AGENTS"), "r") as file:
            for line in file:
                self.user_agents.append(line.strip())

        with open(os.getenv("URLS"), "r") as file:
            for line in file:
                self.urls.append(line.strip())

    async def run(self):
        self.log("STARTING!")
        start = timer()

        for x in range(self.times):
            user_agent = random.sample(self.user_agents, 1)[0]
            url = random.sample(self.urls, 1)[0]
            self.log(f'USER AGENT: {user_agent}')
            self.log(f'URL: {url}')
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
                if reject:
                  await driver.sleep(2)
                  await tab.scroll_down(100)
                  await reject.click()
                  await driver.sleep(2)

                await tab.scroll_up(300)
                self.log(f'STAYING ON PAGE {self.stay_on_page_in_minutes} MINUTES')
                await driver.sleep(self.stay_on_page_in_minutes * 60)
                driver.stop()

                time.sleep(self.sleep_between_runs_in_minutes * 60)
            except Exception as e:
              print(e)

        self.log("DONE!")

        end = timer()
        self.log(f"DURATION: {int(end - start) / 60} MINUTES.")

    def log(self, message):
      now = datetime.datetime.now()
      print(f'{now.strftime("%Y-%m-%dT%H:%M:%SZ")} {message}')

if __name__ == "__main__":
    import traceback

    try:
        jeezy = Jeezy()
        asyncio.run(jeezy.run())
    except Exception:
        print(traceback.format_exc())
