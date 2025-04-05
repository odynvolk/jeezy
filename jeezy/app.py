import asyncio
import datetime
import os
import random
import time
from timeit import default_timer as timer

from dotenv import load_dotenv
import nodriver as uc


load_dotenv()

choices = [True, False]

pixels = [100, 200, 300]

resolutions = [{"width": 1280, "height": 1024}, {"width": 1440, "height": 900}]

class Jeezy(object):
    def __init__(self):
        self.times = int(os.getenv("TIMES"))
        self.stay_on_page_in_minutes = int(os.getenv("STAY_ON_PAGE_IN_MINUTES"))
        self.stay_on_recommended_page_in_minutes = int(os.getenv("STAY_ON_RECOMMENDED_PAGE_IN_MINUTES"))
        self.sleep_between_runs_in_minutes = int(os.getenv("SLEEP_BETWEEN_RUNS_IN_MINUTES"))
        self.headless = bool(os.getenv("HEADLESS"))
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
            self.log("------------------------------------------")
            user_agent = random.choice(self.user_agents)
            url = random.choice(self.urls)
            resolution = random.choice(resolutions)
            self.log(f'USER AGENT: {user_agent}')
            self.log(f'URL: {url}')
            browser_args = [f'--user-agent={user_agent}']
            if self.headless:
                browser_args.append("--headless")

            try:
                driver = await uc.start(browser_args=browser_args)
                tab = await driver.get("about:blank")
                await tab.sleep(2)

                await tab.set_window_size(width=resolution["width"], height=resolution["height"])

                await driver.get(url, new_tab=False)

                await tab.sleep(7)

                await self.random_scroll_down(tab)

                await self.reject(tab)

                await self.random_scroll_up(tab)

                await self.sleep_on_page(tab)

                await self.random_click_recommended(tab)

                driver.stop()
                self.log(f'SLEEPING FOR {self.sleep_between_runs_in_minutes} MINUTES')
                time.sleep(self.sleep_between_runs_in_minutes * 60)
            except Exception as e:
                print(e)

        self.log("DONE!")
        self.log("------------------------------------------")

        end = timer()
        self.log(f"DURATION: {int(end - start) / 60} MINUTES.")

    async def sleep_on_page(self, tab):
        self.log(f'STAYING ON PAGE FOR {self.stay_on_page_in_minutes} MINUTES')
        await tab.sleep(self.stay_on_page_in_minutes * 60)

    async def random_click_recommended(self, tab):
        if random.choice(choices):
            recommendations = await tab.select_all("[id=video-title]")
            number_recommendations = len(recommendations)
            if number_recommendations > 0:
              self.log("RANDOMLY CLICKING RECOMMENDED!")
              await tab.scroll_down(random.choice(pixels))
              await tab.sleep(5)
              await recommendations[random.randrange(0, number_recommendations - 1)].click()
              self.log("CLICKED RECOMMENDATION!")
              await tab.sleep(self.stay_on_page_in_minutes * 60)

    async def random_scroll_down(self, tab):
        if random.choice(choices):
            self.log("RANDOMLY SCROLLING DOWN!")
            await tab.scroll_down(random.choice(pixels))
            await tab.sleep(4)

    async def random_scroll_up(self, tab):
        if random.choice(choices):
            self.log("RANDOMLY SCROLLING UP!")
            await tab.scroll_up(random.choice(pixels))
            await tab.sleep(4)

    async def reject(self, tab):
        reject = await tab.find("Reject all", best_match=True)
        if reject:
            self.log("REJECTING CONSENT!")
            await reject.click()
            await tab.sleep(5)
            await tab.scroll_up(random.choice(pixels))

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
