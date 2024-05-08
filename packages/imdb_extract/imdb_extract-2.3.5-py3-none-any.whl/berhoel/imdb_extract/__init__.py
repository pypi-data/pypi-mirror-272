#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract series information from the IMDB web page.
"""

# Standard library imports.
import os
import re
import csv
import argparse
from pathlib import Path
from contextlib import suppress

# Third party library imports.
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# Local library imports.
from .unicodewriter import UnicodeWriter

__date__ = "2024/05/08 01:03:55 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2011,2013,2023 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"
__version__ = __import__("importlib.metadata", fromlist=["version"]).version(
    "imdb_extract"
)


EPISODE_HEADER = re.compile(r"Season (?P<season>\d+), Episode (?P<episode>\d+):")


class IMDBEntry(object):
    "Handle IMDB episodes information for TV series."
    line = 2
    TITLE_MATCH = re.compile(r"S(?P<season>\d+)\.E(?P<episode>\d+) ∙ (?P<title>.+)")

    def __init__(self, season, href_text, href, desc):
        self.season = season
        _match = self.TITLE_MATCH.match(href_text)
        assert int(_match.group("season")) == self.season
        self.episode = int(_match.group("episode"))
        self.title = _match.group("title")
        self.url = href
        self.url = self.url[: self.url.rfind("?")]
        self.descr = desc

    def list(self):
        "Return information list."
        IMDBEntry.line += 1
        return (
            None,
            self.season,
            self.episode,
            None,
            None,
            None,
            f'=HYPERLINK("{self.url}";"{self.title}")',
            self.descr,
            f"=WENN(ODER(ISTLEER(F{IMDBEntry.line});"
            f'ISTLEER(A{IMDBEntry.line}));"";'
            f"SVERWEIS(F{IMDBEntry.line};F$3:J$10000;5;0)/"
            f"SUMMENPRODUKT(((A$3:A$10000)>0)*((F$3:F$10000)="
            f"F{IMDBEntry.line})))",
        )

    def __lt__(self, other):
        return self.episode < other.episode

    def __le__(self, other):
        return self.episode <= other.episode

    def __eq__(self, other):
        return self.episode == other.episode

    def __ne__(self, other):
        return self.episode != other.episode

    def __gt__(self, other):
        return self.episode > other.episode

    def __ge__(self, other):
        return self.episode >= other.episode


class IMDBInfo(object):
    "Process html page from IMDB"

    def __init__(self, args):
        self.url = self.get_url(args.url[0])

        options = Options()
        options.add_argument("--headless")
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference("intl.accept_languages", args.language)
        firefox_profile.set_preference("javascript.enabled", True)
        options.profile = firefox_profile
        self.driver = webdriver.Firefox(options=options)

        self.series = " ".join(args.title)
        if len(self.series) == 0:
            self.series = self.get_series()

        self.driver.get(self.url)

    def __del__(self):
        self.driver.quit()

    def get_url(self, url):
        path = Path(url)
        res = url
        if path.is_file():
            with path.open() as csvfile:
                inforeader = csv.reader(csvfile)
                res = next(inforeader)[0].split('"')[1]
        while res.endswith("/"):
            res = res[:-1]
        if not res.endswith("/episodes"):
            res += "/episodes"
        return res

    def __call__(self):
        self.process_data()

    def process_data(self):
        "Generate the csv file."

        wait = WebDriverWait(self.driver, 10)

        is_num = re.compile("[0-9]+")
        seasons = [
            int(i.get_attribute("href").split("=")[-1])
            for i in wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[contains(@class,"ipc-tabs--display-chip")]')
                )
            ).find_elements(
                By.XPATH, '//div[contains(@class,"ipc-tabs--display-chip")]//a'
            )
        ]

        tbl = "".maketrans("/", "_")
        with open(f"{self.series.strip().translate(tbl)}.csv", "w") as filep:
            writer = UnicodeWriter(filep, delimiter=";", quoting=csv.QUOTE_MINIMAL)

            writer.writerow(
                [f'=HYPERLINK("{self.url.strip()[:-9]}";"{self.series.strip()}")']
            )
            writer.writerow(
                [
                    '=HYPERLINK("#Übersicht";"Datum")',
                    None,
                    None,
                    "Disk",
                    "Index",
                    "Diskset",
                    "IMDB URL",
                    None,
                    "=MITTELWERT(I3:I10000)",
                    "=SUMME(J3:J10000)",
                ]
            )

            for season in seasons:
                self.driver.get(f"{self.url}/?season={season}")
                wait = WebDriverWait(self.driver, 10)

                print(f"Season {season}")

                elem = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//article[contains(@class,"episode-item-wrapper")]',
                        )
                    )
                )
                articles = elem.find_elements(
                    By.XPATH,
                    '//article[contains(@class,"episode-item-wrapper")]',
                )

                episodes = []

                for article in articles:
                    description = article.find_elements(
                        By.XPATH, './/div[@class="ipc-html-content-inner-div"]'
                    )
                    if not description:
                        description = ""
                    else:
                        description = description[0].text
                    link = article.find_element(
                        By.XPATH, './/a[@class="ipc-title-link-wrapper"]'
                    )
                    episodes.append(
                        IMDBEntry(
                            season, link.text, link.get_attribute("href"), description
                        )
                    )

                episodes.sort()

                for i in episodes:
                    writer.writerow(
                        [j.strip() if isinstance(j, str) else j for j in i.list()]
                    )

    def get_series(self):
        url = self.url[:-9]
        driver = self.driver
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        wrapper = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        res = wrapper.find_element(
            By.XPATH, '//h1[contains(@data-testid, "hero__pageTitle")]'
        ).text
        with suppress(Exception):
            res = wrapper.find_element(
                By.XPATH,
                '//div[contains(@data-testid, "hero-title-block__original-title")]',
            ).text.strip()
            if res.endswith(" (original title)"):
                res = res[:-17]
            if res.startswith("Original title: "):
                res = res[16:]
            if res.startswith("Originaltitel: "):
                res = res[15:]
        return res.strip()


def get_parser():
    "Create CLI parser."
    parser = argparse.ArgumentParser(
        description="""Extract IMDB information for TV series. Generates file
<Title>.csv. If existing CSV file is given as argument, URL is read from
previously generated CSV file."""
    )
    parser.add_argument(
        "url", metavar="URL", type=str, nargs=1, help="URL string / existing CSV file"
    )
    parser.add_argument(
        "title", metavar="TITLE", type=str, nargs="*", help="title string", default=""
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="en",
        help="Language to use for download, default: %(default)s",
    )
    return parser


def main():
    "Main program."
    args = get_parser().parse_args()

    prog = IMDBInfo(args)

    print(f"URL   : {prog.url}")
    print(f"series: {prog.series}")

    prog()

    raise SystemExit


if __name__ == "__main__":
    main()

# Local Variables:
# mode: python
# compile-command: "cd ../../ && python setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
