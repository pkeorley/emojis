import os
import urllib
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from errors import EmojisNotFound, FailedDownload


class Emojis:
    def __init__(self):
        self.ENDPOINT = "https://discadia.com/emojis"

    def __get_soup(self, query: str):
        response = requests.get(self.ENDPOINT + f"/?q={query}")
        return BeautifulSoup(response.text, "lxml")

    def search(self, query: str):
        soup = self.__get_soup(query)
        emojis = []

        for emoji in soup.find_all("emoji-card"):
            img = emoji.find("img").get("src")
            name = emoji.find("span").text.strip(":")
            emojis.append({
                "name": name,
                "img": img
            })

        if not emojis:
            raise EmojisNotFound("No emojis were found for '%s'" % query)

        return emojis


if __name__ == "__main__":
    import json
    import argparse

    emojis_parser = Emojis()
    parser = argparse.ArgumentParser(description="Parse all emojis from site discadia.com.")

    parser.add_argument('query', help="Get all images by topic.")
    parser.add_argument('--json', help="Save all data to json file.")
    parser.add_argument('--print', action='store_true', help="Print parsed emojis to screen.")
    parser.add_argument('--download', action='store_true', help="Download add files to directory")

    args = parser.parse_args()
    parsed_emojis = emojis_parser.search(args.query)

    if args.json:
        with open(args.json.replace(".", "") + ".json", "w") as file:
            json.dump(parsed_emojis, file, indent=4, ensure_ascii=False)

    if args.print:
        pprint(parsed_emojis)

    if args.download:
        downloaded = []

        def download_emoji(url: str, filename: str = "emoji") -> None:
            filename = "".join(s for s in filename if s.isascii()) + ".gif"

            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                filename = f"{args.query}/{filename}"
                with open(filename, "wb") as gif:
                    gif.write(response.content)

            except FailedDownload as error:
                raise FailedDownload("Couldn't upload the file '%s': %s" % (filename, error))

        if args.query not in os.listdir():
            os.makedirs(args.query)

        for emoji in parsed_emojis:
            try:
                download_emoji(url=emoji["img"], filename=emoji["name"])
            except FailedDownload as failed_download_error:
                print("{0.__class__.__name__}: {0}".format(failed_download_error))

        print(f"{len(os.listdir(args.query))}/{len(parsed_emojis)}")
