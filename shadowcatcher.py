#!/usr/bin/env python3

import argparse
import subprocess
import sys
import xml.etree.ElementTree as ET


def graph_for_target(target):
    p = subprocess.run(["bazel", "query", "deps(" + target + ")", "--output=xml"], capture_output=True)
    xml = p.stdout
    return xml


def parse_tree(tree):
    MAVEN_COORD_PREFIX = "maven_coordinates="
    deps = {}
    rdeps = {}
    mcoords = {}
    for rule in tree.findall(".//rule"):

        name = rule.get('name')
        ruledeps = []
        for el in rule:
            if el.tag == 'list' and el.get('name') == 'deps':
                for eld in el:
                    v = eld.get('value')
                    if v not in ruledeps:
                        ruledeps.append(v)

            if el.tag == 'list' and el.get('name') == 'tags':
                for elt in el:
                    if elt.get('value').startswith('maven_coordinates='):
                        mcoord = elt.get('value')[len(MAVEN_COORD_PREFIX):]
                        if mcoord not in mcoords:
                            mcoords[mcoord] = []
                        mcoords[mcoord].append(name)

            if el.tag == 'rule-input':
                n = el.get('name')
                if n not in ruledeps:
                    ruledeps.append(n)

        deps[name] = ruledeps

        for target in ruledeps:
            if target not in rdeps:
                rdeps[target] = []
            if name not in rdeps[target]:
                rdeps[target].append(name)

    return deps, rdeps, mcoords


def get_prefix_matches(mccords, prefix):
    matches = []
    for c in mcoords:
        if c.startswith(prefix + ":"):
            matches.append(c)
    return matches


def find_dupes(mcoords):
    prefixes = []
    dupes = {}
    for c in mcoords:
        # Get everything before the second colon
        # i.e. "com.google.guava:listenablefuture:9999.0" becomes
        # "com.google.guava:listenablefuture:9999.0-empty-to-avoid-conflict-with-guava"
        prefix = c[0:c.find(":", c.find(":") + 1)]
        if prefix not in prefixes:
            prefixes.append(prefix)

    for prefix in prefixes:
        matches = get_prefix_matches(mcoords, prefix)
        if len(matches) > 1:
            dupes[prefix] = matches
    return dupes


def recursive_get_rdep_paths(target, rdeps, path):
    paths = []
    path.append(target)
    if target in rdeps:
        for t in rdeps[target]:
            paths.extend(recursive_get_rdep_paths(t, rdeps, path.copy()))
    else:
        paths.append(path)
    return paths


def indent(level):
    str = ""
    for i in range(0, level):
        str += "    "
    return str


def print_output(dupes, deps, rdeps, mcoords, PRINT_ALL):
    for prefix, matches in dupes.items():
        print("Found a duplicate")
        print("")
        print("Artifact")
        print("  " + prefix)
        print("")
        print("has differing versions")
        for match in matches:
            print("    " + match)

            for target in mcoords[match]:
                rdeppaths = recursive_get_rdep_paths(target, rdeps, [])
                if PRINT_ALL:
                    for path in rdeppaths:
                        path.reverse()
                        indentlevel = 0
                        for pathel in path:
                            indentlevel = indentlevel + 1
                            print(indent(indentlevel) + pathel)
                else:
                    path = rdeppaths[0]
                    path.reverse()
                    indentlevel = 0
                    for pathel in path:
                        indentlevel = indentlevel + 1
                        print(indent(indentlevel) + pathel)
                    if len(rdeppaths) > 1:
                        print("    and " + str(len(rdeppaths) - 1) + " more. Use --all to print all")
            print()
        print("================")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scan a bazel target for shadowed dependencies')
    parser.add_argument("-a", "--all", dest="print_all", action='store_true',
                        help="Print all paths to a given dependency", default=False)
    parser.add_argument("-t", "--target", dest="target", help="The bazel target to scan for duplicates", required=True)
    parser.set_defaults(print_all=False)

    args = parser.parse_args()
    base_target = args.target
    print("Scanning deps for " + base_target)
    xml = graph_for_target(base_target)
    tree = ET.fromstring(xml)
    deps, rdeps, mcoords = parse_tree(tree)
    dupes = find_dupes(mcoords)
    print_output(dupes, deps, rdeps, mcoords, args.print_all)
    if len(dupes) > 0:
        sys.exit(1)
    else:
        print("No duplicates found!")
