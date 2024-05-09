__version__="0.1.3"

new_features = [
    "New:",
    [
    ],
]

feature_changes = [
    "Changes:",
    [
        "Updated README to include installation instructions that were accidentally deleted in version 0.1.2.",
    ],
]

bug_fixes = [
    "Bug fixing:",
    [
    ],
]

def version_change_writer(iterable, recursion_depth = 0):
    list_of_strings = []
    for i in iterable:
        if type(i) == str:
            list_of_strings.append("    " * recursion_depth + i)
        elif type(i) in [list, tuple]:
            list_of_strings.extend(version_change_writer(i, recursion_depth + 1))
    return list_of_strings

all_changes = []
if len(new_features) > 1:
    all_changes += new_features + [""]
if len(feature_changes) > 1:
    all_changes += feature_changes + [""]
if len(bug_fixes) > 1:
    all_changes += bug_fixes

version_changes_list = version_change_writer(all_changes)
version_changes_str = "\n".join(version_changes_list)

def version_changes():
    print(version_changes_str)

