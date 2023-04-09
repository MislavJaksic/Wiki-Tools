import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict

from mwapi.errors import APIError

from wiki_tools.download.wiki_api import WikiAPI
from wiki_tools.settings import users_filename, categories_filename, categories_wikitext_filename, revisions_filename, \
    user_contributions_filename


class WikiDownloader:
    def __init__(self, wiki_api: WikiAPI):
        self.api = wiki_api

    def download_user_contributions(self, user: str) -> None:
        jsons = []
        parameters = {"action": "query", "list": "usercontribs", "ucuser": user, "continuation": True}
        for json in self.api.get_next_json_batch_for_action_list_continuation(parameters):
            jsons.append(json)
        self.jsons_to_file(jsons, user_contributions_filename)

    def download_revisions_from_today_to_datetime(self, earliest_date: datetime) -> None:
        jsons = []
        parameters = {"action": "query", "list": "allrevisions", "continuation": True}
        for revision in self.api.get_next_json_batch_for_action_list_continuation(parameters):
            revision_utc_date = self.wiki_timestamp_to_utc_python_timestamp(
                revision["revisions"][0]["timestamp"][:-1])
            if earliest_date > revision_utc_date:
                break
            jsons.append(revision)
        revisions = []
        for json in jsons:
            for revision in json["revisions"]:
                revisions.append(
                    {"pageid": json["pageid"], "revid": revision["revid"], "parentid": revision["parentid"],
                     "user": revision["user"], "timestamp": revision["timestamp"], "comment": revision["comment"],
                     "ns": json["ns"], "title": json["title"]})
        self.jsons_to_file(revisions, revisions_filename)

    def download_users(self) -> None:
        jsons = []
        parameters = {"action": "query", "list": "allusers", "continuation": True}
        for user in self.api.get_next_json_batch_for_action_list_continuation(parameters):
            jsons.append(user)
        self.jsons_to_file(jsons, users_filename)

    def download_categories(self) -> None:
        jsons = []
        parameters = {"action": "query", "list": "allcategories", "continuation": True}
        for category in self.api.get_next_json_batch_for_action_list_continuation(parameters):
            jsons.append(category)
        self.jsons_to_file(jsons, categories_filename)

    def download_categories_wikitext(self) -> None:
        with open("categories.json", "r") as file:
            categories = json.load(file)
            jsons = []
            for category in categories:
                page = "Category:{}".format(category["*"])
                jsons.append({page: self.fetch_page_wikitext(page)})
            self.jsons_to_file(jsons, categories_wikitext_filename)

    def fetch_links_on_page(self, page: str) -> List[str]:
        links = []
        parameters = {"action": "query", "prop": "links", "titles": page, "continuation": True}
        for data in self.api.get_action_list_continuation_batch(parameters):
            pages = data[parameters["action"]]["pages"]
            for k, v in pages.items():
                for link in v[parameters["prop"]]:
                    links.append(link["title"])
        return links

    def fetch_page_wikitext(self, page: str) -> str:
        try:
            parameters = {"action": "parse", "page": page, "prop": "wikitext"}
            wikitext = self.api.session.get(**parameters)["parse"]["wikitext"]["*"]
        except APIError:
            wikitext = None
        return wikitext

    def fetch_category_members(self, category: str, member_types: Tuple = ("page", "subcat", "file")) -> List[str]:
        pages = []
        parameters = {"action": "query", "list": "categorymembers", "cmtitle": category, "cmtype": member_types,
                      "continuation": True}
        for page in self.api.get_next_json_batch_for_action_list_continuation(parameters):
            pages.append(page)
        return pages

    def wiki_timestamp_to_utc_python_timestamp(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp)

    def jsons_to_file(self, jsons: List, filename: str) -> None:
        file_path = Path.cwd() / "downloads" / filename
        with open(Path(file_path), "w") as file:
            file.write(json.dumps(jsons))

    def file_to_jsons(self, filename: str) -> List[Dict]:
        file_path = Path.cwd() / "downloads" / filename
        with open(Path(file_path), "r") as file:
            return json.load(file)
