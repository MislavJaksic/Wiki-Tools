"""
    wiki-tools.py
    ------------------

    Runs the project.

    :copyrgiht: 2019 MislavJaksic
    :license: MIT License
"""
import json
import math
import re
import sys
from datetime import datetime

from matplotlib_venn import venn2_circles

from wiki_tools.download.wiki_api import WikiAPI
from wiki_tools.download.wiki_downloader import WikiDownloader
from wiki_tools.model.revision import parse_revision_batch
from wiki_tools.model.user import get_duplicate_users, parse_users
from wiki_tools.secrets_wiki import mediawiki_url, mediawiki_api_path
from wiki_tools.settings import users_filename, revisions_filename, sorted_revisions_filename, \
    user_contributions_filename


def main(args):
    """main() will be run if you run this script directly
    """
    # site = pywikibot.Site('en', '')  # The site we want to run our bot on
    # page = pywikibot.Page(site, '')
    # page.text = page.text.replace('=  =', '==  ==')
    # page.save('Increased section level')  # Saves the page

    wiki_api = WikiAPI(mediawiki_url, mediawiki_api_path)
    wiki_downloader = WikiDownloader(wiki_api)

    wiki_downloader.download_revisions_from_today_to_datetime(datetime.fromisoformat('2022-12-01'))

    # wiki_downloader.download_user_contributions("Evon R'al")

    # members = wiki_downloader.fetch_category_members("", ("subcat",))
    # print(members)

    # members = wiki_downloader.fetch_links_on_page("")
    # print(members)

    # store_sorted_revisions(wiki_downloader)

    # print_duplicate_users(wiki_downloader)

#     page_list = []
#     for cat in categories:
#         members = wiki_downloader.fetch_category_members(cat, ("page",))
#
#         for member in members:
#             page = member["title"]
#             wikitext = wiki_downloader.fetch_page_wikitext(page)
#             if "[[Category:" in wikitext:
#                 page_list.append((page, wikitext))
#
#     with open("output.txt", "w") as file:
#         file.write(json.dumps(page_list))

    # with open("output.txt", "r") as file:
    #     templates = json.load(file)
    #     commands = []
    #     for title, wikitext in templates:
    #         print(title)
    #         match = re.search(r"(Category:.*)\]\]", wikitext) # r"(\[\[Category:.*\]\])"
    #         category = match.group(1)
    #         print(category)
    #
    #         page_list = []
    #         members = wiki_downloader.fetch_category_members(category, ("page",))
    #         for member in members:
    #             page = member["title"]
    #             page_list.append(page)
    #
    #         pages = " ".join(["-page:\"{}\"".format(x) for x in page_list if (x.find("Archive:") == -1 and x.find("User:") == -1 and x.find("Template:") == -1)])
    #         command = "poetry run python pwb.py category add -to:\"{}\" -redirect {}".format(category, pages)
    #         commands.append(command)
    #
    #     with open("commands.txt", "w") as file:
    #         for command in commands:
    #             file.write(command)
    #             file.write("\n")

def store_sorted_revisions(downloader: WikiDownloader) -> None:
    revision_batches = downloader.file_to_jsons("revisions-2022-2021-years.json")
    revisions = parse_revision_batch(revision_batches)
    revisions = sorted(revisions, key=lambda x: x.user)
    with open(sorted_revisions_filename, "w") as output:
        for revision in revisions:
            try:
                output.write("{}${}${}${}${}\n".format(revision.user, revision.timestamp, revision.ns, revision.title, revision.comment.replace('\n', ' ')))
            except:
                print(revision)

def print_duplicate_users(downloader: WikiDownloader) -> None:
    users = downloader.file_to_jsons(users_filename)
    parsed_users = parse_users(users)
    duplicates = get_duplicate_users(parsed_users)
    print(duplicates)
    print(len(duplicates))
    # old_usernames = [duplicate.capitalize() for duplicate in duplicates]
    # old_users_with_pages = [(new, old) for (new, old) in duplicates if downloader.api.is_title_exists("User:{}".format(old))]
    # print(old_users_with_pages)
    # print(len(old_users_with_pages))
    # with open("pairsfile.txt", "w") as file:
    #    for x in old_users_with_pages:
    #        file.write("[[User:{}]]\n[[User:{}/Old user page]]\n".format(x[1], x[0]))


def run():
    """Entry point for the runnable script.
    """
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run().
    """
    run()
