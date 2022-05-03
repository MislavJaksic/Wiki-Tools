from typing import List


class AllRevisionStats:
    def __init__(self, revisions: List):
        self.first_timestamp = revisions[-1].timestamp
        self.last_timestamp = revisions[0].timestamp
        pages = [revision.title for revision in revisions]
        unique_pages = set(pages)
        self.count_pages = len(unique_pages)
        self.edits = len(revisions)
        self.non_consecutive_edits = len(set([(revision.title, revision.user) for revision in revisions]))
        editors = [revision.user for revision in revisions]
        self.unique_editors = sorted(set(editors))
        self.count_editors = len(self.unique_editors)

        self.edits_per_page = self.sort_dict_by_value_get_top_10_descending(
            {page: pages.count(page) for page in unique_pages})
        self.edits_per_editor = self.sort_dict_by_value_get_top_10_descending(
            {editor: editors.count(editor) for editor in self.unique_editors})

    def sort_dict_by_value_get_top_10_descending(self, d):
        return dict(sorted(d.items(), key=lambda x: x[1], reverse=True)[:10])

    def __str__(self) -> str:
        return '{}({})'.format(type(self).__name__, ', '.join('%s:%s' % item for item in vars(self).items()))

    def __repr__(self) -> str:
        return self.__str__()
