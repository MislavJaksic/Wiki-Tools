from datetime import datetime
from typing import Dict, List, Set


class Revision:
    def __init__(self, pageid, revision: Dict, ns, title):
        self.pageid = pageid
        self.ns = ns
        self.minor = True if revision.get("minor") is not None else False
        self.user = revision["user"]
        self.timestamp = datetime.fromisoformat(revision["timestamp"][:-1])
        self.comment = revision["comment"]
        self.title = title

    def __str__(self) -> str:
        return '{}({})'.format(type(self).__name__, ', '.join('%s:%s' % item for item in vars(self).items()))

    def __repr__(self) -> str:
        return self.__str__()


def parse_revision_batch(revision_batchs: List) -> List[Revision]:
    revisions = []
    for revision_batch in revision_batchs:
        pageid = revision_batch["pageid"]
        ns = revision_batch["ns"]
        title = revision_batch["title"]
        for revision in revision_batch["revisions"]:
            revisions.append(Revision(pageid, revision, ns, title))
    return revisions


def get_signed_up_users(revisions: List) -> Set:
    return set([revision.user for revision in revisions if "WE" in revision.comment])


def get_sign_up_revisions(revisions: List) -> List[Revision]:
    return [revision for revision in revisions if "WE" in revision.comment]
