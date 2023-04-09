"""
    wiki-tools.py
    ------------------

    Runs the project.

    :copyrgiht: 2019 MislavJaksic
    :license: MIT License
"""
import csv
import sys
from collections import defaultdict
from datetime import datetime

from wiki_tools.download.wiki_api import WikiAPI
from wiki_tools.download.wiki_downloader import WikiDownloader
from wiki_tools.model.revision import parse_revision_batch
from wiki_tools.model.user import get_duplicate_users, parse_users
from wiki_tools.secrets_wiki import mediawiki_url, mediawiki_api_path
from wiki_tools.settings import users_filename, sorted_revisions_filename, revisions_filename


def main(args):
    """main() will be run if you run this script directly
    """
    # site = pywikibot.Site('en', '')  # The site we want to run our bot on
    # page = pywikibot.Page(site, '')
    # page.text = page.text.replace('=  =', '==  ==')
    # page.save('Increased section level')  # Saves the page

    #wiki_api = WikiAPI(mediawiki_url, mediawiki_api_path)
    #wiki_downloader = WikiDownloader(wiki_api)

    # wiki_downloader.download_revisions_from_today_to_datetime(datetime.fromisoformat('2022-12-01'))

    # wiki_downloader.download_user_contributions("Evon R'al")

    # members = wiki_downloader.fetch_category_members("", ("subcat",))
    # print(members)

    # members = wiki_downloader.fetch_links_on_page("")
    # print(members)

    #store_sorted_revisions(wiki_downloader)

    csv_revisions_to_editor_count_edits()

    # csv_revisions_to_title_user_edit_count()

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

def csv_revisions_to_title_user_edit_count():
    # open the input CSV file with $ as delimiter
    with open('revisions_sorted.csv', 'r') as infile:
        reader = csv.reader(infile, delimiter='$')
        headers = next(reader)  # get the header row

        # find the indices of the 'name', 'title', and 'ns' columns
        name_index = headers.index('name')
        title_index = headers.index('title')
        ns_index = headers.index('ns')

        # initialize a defaultdict to keep track of the edit counts
        edit_counts = defaultdict(lambda: defaultdict(int))

        # loop over each row in the input file and increment the edit count for the corresponding editor, page, and namespace
        for row in reader:
            name = row[name_index]
            title = row[title_index]
            ns = row[ns_index]
            edit_counts[(title, ns)][name] += 1

    # open the output CSV file with $ as delimiter
    with open('output.csv', 'w') as outfile:
        writer = csv.writer(outfile, delimiter='$')

        # write the header row
        writer.writerow(['title', 'ns', 'editors', 'count', 'total_count'])

        # loop over each (page, ns) pair in the edit_counts dictionary and write a row to the output file
        for (title, ns), editor_counts in edit_counts.items():
            # get the total count of edits to this page and namespace
            total_count = sum(editor_counts.values())

            # create a list of editor names and counts in the format 'name x count'
            editor_list = [f'{name} x {count}' for name, count in editor_counts.items()]

            # join the editor list into a single string with commas as separators
            editor_str = ', '.join(editor_list)

            # write the output row
            writer.writerow([title, ns, editor_str, total_count, len(editor_counts)])

def csv_revisions_to_editor_count_edits():
    # open the input CSV file with $ as delimiter
    with open('revisions_sorted.csv', 'r') as infile:
        reader = csv.reader(infile, delimiter='$')
        headers = next(reader)  # get the header row

        # find the indices of the 'name', 'title', and 'ns' columns
        name_index = headers.index('name')
        title_index = headers.index('title')
        ns_index = headers.index('ns')

        # initialize a defaultdict to keep track of the edit counts
        edit_counts = defaultdict(lambda: defaultdict(int))

        # loop over each row in the input file and increment the edit count for the corresponding editor, page, and namespace
        for row in reader:
            name = row[name_index]
            title = row[title_index]
            ns = row[ns_index]
            edit_counts[(name, title, ns)][name] += 1

    # open the output CSV file with $ as delimiter
    with open('output.csv', 'w') as outfile:
        writer = csv.writer(outfile, delimiter='$')

        # write the header row
        writer.writerow(['editor', 'title', 'namespace', 'count'])

        # loop over each (editor, page, namespace) triple in the edit_counts dictionary and write a row to the output file
        for (editor, title, ns), count in edit_counts.items():
            editor_counts = [f"{count}" for name, count in count.items()][0]
            writer.writerow([editor, title, ns, editor_counts])

def store_sorted_revisions(downloader: WikiDownloader) -> None:
    revision_batches = downloader.file_to_jsons(revisions_filename)
    revisions = parse_revision_batch(revision_batches)
    revisions = sorted(revisions, key=lambda x: x.user)
    with open(sorted_revisions_filename, "w") as output:
        for revision in revisions:
            try:
                output.write("{}${}${}${}${}\n".format(revision.user, revision.timestamp, revision.ns, revision.title,
                                                       revision.comment.replace('\n', ' ')))
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
