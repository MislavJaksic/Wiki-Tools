"""
    wiki-tools.py
    ------------------

    Runs the project.

    :copyrgiht: 2019 MislavJaksic
    :license: MIT License
"""
import sys

from wiki_tools.download.wiki_api import WikiAPI
from wiki_tools.download.wiki_downloader import WikiDownloader
from wiki_tools.model.revision import parse_revision_batch
from wiki_tools.model.user import get_duplicate_users, parse_users
from wiki_tools.secrets import mediawiki_url, mediawiki_api_path
from wiki_tools.settings import users_filename, revisions_filename, sorted_revisions_filename


def main(args):
    """main() will be run if you run this script directly
    """

    wiki_api = WikiAPI(mediawiki_url, mediawiki_api_path)
    wiki_downloader = WikiDownloader(wiki_api)

    # members = wiki_downloader.fetch_category_members("Category:EVE University", ("subcat",))
    # print(members)


def store_sorted_revisions(downloader: WikiDownloader) -> None:
    revision_batches = downloader.file_to_jsons(revisions_filename)
    revisions = parse_revision_batch(revision_batches)
    revisions = sorted(revisions, key=lambda x: x.user)
    with open(sorted_revisions_filename, "w") as output:
        for revision in revisions:
            output.write("{},{},{},{}\n".format(revision.user, revision.timestamp, revision.title, revision.comment))


def print_duplicate_users(downloader: WikiDownloader) -> None:
    users = downloader.file_to_jsons(users_filename)
    parsed_users = parse_users(users)
    duplicates = get_duplicate_users(parsed_users)
    print(duplicates)
    print(len(duplicates))
    # old_usernames = [duplicate.capitalize() for duplicate in duplicates]
    # old_users_without_pages = [x for x in old_usernames if not wiki_api.is_title_exists("User:{}".format(x))]


def run():
    """Entry point for the runnable script.
    """
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run().
    """
    run()
