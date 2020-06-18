#!/usr/bin/env python3

import sys, subprocess, string, re

print("Scanning deps for " + sys.argv[1])

base_target = sys.argv[1]


def graph_for_target(target):
    p = subprocess.run(["bazel", "query", "deps(" + target + ")", "--output=graph"], capture_output=True)
    # print(p.stdout)
    graph_entries = p.stdout.decode("ascii").split("\n")
    return graph_entries


def make_mappings(graph_entries):
    SINGLE_ITEM = re.compile('^\s*\\"([^\\"]*)\\"$')
    TWO_ITEMS = re.compile('^\s*\\"([^\\"]*)\\"\s*->\s*\\"([^\\"]*)\\"$')
    root = None
    mappings = {}
    for entry in graph_entries:
        if root is None:
            if SINGLE_ITEM.match(entry):
                root = SINGLE_ITEM.search(entry).group(1)
                print("Root: " + root)

        groups = TWO_ITEMS.search(entry)
        if groups is not None:
            left = groups.group(1)
            right = groups.group(2)
            if left in mappings:
                mappings[left].append(right)
            else:
                mappings[left] = [right]

    return root, mappings


PRINTED_ROOTS = []


def print_tree(root, mappings, depth):
    pad = (' ' * (depth * 4))
    print(pad + root)
    if root in PRINTED_ROOTS:
        print(pad + '   ** Already printed elsewhere in tree')
    else:
        PRINTED_ROOTS.append(root)
        if root in mappings:
            for dep in mappings[root]:
                print_tree(dep, mappings, depth + 1)


def main():
    entries = graph_for_target(base_target)
    root, mappings = make_mappings(entries)
    print_tree(root, mappings, 0)


if __name__ == "__main__":
    main()
