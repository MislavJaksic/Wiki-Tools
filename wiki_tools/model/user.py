from typing import List, Dict


class User:
    def __init__(self, userid: str, name: str):
        self.userid = userid
        self.name = name

    def __str__(self) -> str:
        return '{}({})'.format(type(self).__name__, ', '.join('%s:%s' % item for item in vars(self).items()))

    def __repr__(self) -> str:
        return self.__str__()


def parse_users(users: List[Dict]) -> List[User]:
    parsed_users = []
    for user in users:
        parsed_users.append(User(user["userid"], user["name"]))
    return parsed_users


def get_duplicate_users(users: List[User]) -> List[str]:
    lower_names = [user.name.lower() for user in users]
    duplicates = set([name for name in lower_names if lower_names.count(name) > 1])
    return sorted(duplicates)
