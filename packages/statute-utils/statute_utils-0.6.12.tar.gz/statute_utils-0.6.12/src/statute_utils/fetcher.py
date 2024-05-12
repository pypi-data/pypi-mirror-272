import datetime
from enum import StrEnum, auto
from http import HTTPStatus
from pathlib import Path

import httpx
from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse
from markdownify import markdownify

from statute_utils import StatuteTitle, StatuteTitleCategory

from .components import list_sections

"""
Each tag can create a Statute object via `create_statute(tag)`.
The Statute object can then be converted to a yaml file via:

```py
tags = Listing.Apr.fetch_tags(year=2024)
stat = Statute.from_web(tag=tag)
stat.to_file_from_web(basepath=STATUTES)
```
"""

STATUTES = Path().home().joinpath("code/corpus-statutes")
ELIB = "https://elibrary.judiciary.gov.ph/thebookshelf"


def url_to_content(url: str) -> bytes | None:
    """Get contents of `url`, e.g. html or PDF."""
    res = httpx.get(url, follow_redirects=True, timeout=90.0)
    if res.status_code == HTTPStatus.OK:
        return res.content
    return None


def url_to_soup(url: str) -> BeautifulSoup | None:
    """Creates a soup object from the response of the `url`."""
    content = url_to_content(url=url)
    if content:
        return BeautifulSoup(content, "lxml")
    return None


class Listing(StrEnum):
    """Contains month names which can pe paired with a year."""

    Jan = auto()
    Feb = auto()
    Mar = auto()
    Apr = auto()
    May = auto()
    Jun = auto()
    Jul = auto()
    Aug = auto()
    Sep = auto()
    Oct = auto()
    Nov = auto()
    Dec = auto()

    def set_url(self, year: int):
        return f"{ELIB}/docmonth/{self.name}/{year}/2"

    def fetch_url(self, year: int):
        return url_to_soup(url=self.set_url(year))

    def fetch_tags(self, year: int) -> list[Tag]:
        soup = self.fetch_url(year)
        if not soup:
            raise Exception(f"Missing content from {self.name=} on {year=}")
        return soup(id="container_title")[0]("li")


def extract_link_from_tag(tag: Tag) -> str:
    return tag("a")[0]["href"].replace("showdocs", "showdocsfriendly")


def extract_serial_title_from_tag(tag: Tag) -> str:
    return tag("strong")[0].text.strip().title()


def extract_official_title_from_tag(tag: Tag) -> str:
    return tag("small")[0].text.strip().title()


def extract_date_from_tag(tag: Tag) -> datetime.date:
    dt = tag("a")[0].find_all(string=True, recursive=False)[-1].strip()
    return parse(dt).date()


def extract_statute_titles(tag: Tag) -> list[StatuteTitle]:
    return [
        StatuteTitle(
            category=StatuteTitleCategory.Serial,
            text=extract_serial_title_from_tag(tag),
        ),
        StatuteTitle(
            category=StatuteTitleCategory.Official,
            text=extract_official_title_from_tag(tag),
        ),
    ]


def clean_units(units: list[dict]) -> list[dict]:
    for unit in units:
        unit.pop("order")
        raw = unit.pop("content")
        unit["content"] = markdownify(html=raw)
    return units


def remove_extraneous_text(units: list[dict]) -> list[dict]:
    last_unit = units[-1]["content"]
    marker = "Approved,\n"
    if marker in last_unit:
        idx = last_unit.index("Approved,\n")
        units[-1]["content"] = units[-1]["content"][:idx]
        print("Removing extra area")
    return units


def extract_units_from_tag(tag: Tag) -> list[dict]:
    link = extract_link_from_tag(tag)
    soup = url_to_soup(link)
    if not soup:
        raise Exception(f"Missing soup from {tag=}")
    units = list_sections(raw=str(soup))
    units = clean_units(units)
    units = remove_extraneous_text(units)
    return units
