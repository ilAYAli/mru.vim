#! /usr/bin/env python3
import os
import sys
import hashlib
import subprocess
import configargparse
import signal
import git
import json
from collections import OrderedDict
from devicons import get_devicon

class Meta():
    def __repr__(self):
        return str(vars(self))
    def add(self, path):
        #print("root =", self.git_root, " path =", path)
        if os.path.isabs(path):
            # ignore non-repo files
            if not path.startswith(self.git_root):
                return
            else:
                # make path relative to repo root:
                path = path[1 + len(self.git_root):]
                #print("new path: ", path)

        if len(self.mru) == 0:
            self.mru[path] = 1
        else:
            it = max(self.mru, key=self.mru.get)
            maxval = int(self.mru[it])
            self.mru[path] = maxval +1

    def delete(self, path):
        #print("delete: ", path)
        try:
            del self.mru[path]
        except KeyError:
            print("key not found:", path)
    max_elements = 200
    mru = dict()
    git_root = ""

def main(argv):
    m = Meta()
    home = os.path.expanduser('~')
    git_root = ""
    try:
        git_repo = git.Repo(".", search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")
    except:
        pass
    if not git_root:
        mru_db = os.path.join(home, '.cache/mru.tx')
    else:
        mru_db = os.path.join(home, '.cache/mru-')
        hash_obj = hashlib.md5(git_root.encode())
        mru_db += hash_obj.hexdigest()
        mru_db += '.txt'

    try:
        with open(mru_db, 'r') as fp:
            m.mru = json.load(fp)
    except OSError:
        pass

    m.git_root = git_root

    parser = configargparse.ArgParser(default_config_files=['~/.mru.conf'])
    parser.add_argument("-a", "--add",      help="add file to MRU", metavar='')
    parser.add_argument("-d", "--delete",   help="delete file from MRU", metavar='')
    parser.add_argument("-m", "--max",      help="max MRU size", action='store', type=int, metavar='')
    parser.add_argument("-e", "--exclude",  help=configargparse.SUPPRESS, metavar='')
    parser.add_argument("-v", "--verbose",  help="verbose", action='store_true')
    parser.add_argument("-c", "--colors",   help="print with colors", action='store_true')
    parser.add_argument("-i", "--icons",    help="show icons (requires NERD fonts)", action='store_true')
    parser.add_argument("-C", "--nocolors", help="disable colors", action='store_true')
    parser.add_argument("-I", "--noicons",  help="disable icons", action='store_true')
    parser.add_argument("-R", "--norel",    help="only show mru files", action='store_true')

    dump_mru = True
    args = parser.parse_args()
    if args.add:
        m.add(args.add)
        dump_mru = False
    if args.delete:
        m.delete(args.delete)
        dump_mru = False
    if args.max:
        m.max_elements = args.max

    if args.verbose:
        print("config: ~/.mru.conf")
        print("database: ", mru_db)

    #if not sys.stdout.isatty():
    #    args.colors = False

    if args.nocolors:
        args.colors = False

    if args.noicons:
        args.icons = False

    if dump_mru:
        color_normal = '\33[0m'
        color_blue =   '\33[38;5;4m'
        color_orange = '\33[38;5;11m'

        sorted_mru = [(k, m.mru[k]) for k in sorted(m.mru, key=m.mru.get, reverse=True)]
        index = 0
        for path, v in sorted_mru:
            if args.exclude:
                if args.exclude in path:
                    continue

            if ".git/" in path:
                continue

            if not os.path.isfile(path):
                continue
            s = get_devicon(path) + " " if args.icons else ""
            s += color_orange if args.colors else ""
            s += "mru: "
            s += color_normal if args.colors else ""
            s += path
            if args.verbose:
                s += " [" + str(v) + "]"
            try:
                print(s)
            except:
                pass
            index += 1
            if index > m.max_elements:
                break

        if args.norel:
            return

        if not git_root:
            out = subprocess.getoutput("find . -type f | head -n 1000")
        else:
            out = subprocess.getoutput("git ls-files")

        for path in out.splitlines():
            s = get_devicon(path) + " " if args.icons else ""
            s += color_blue if args.colors else ""
            s += "rel: "
            s += color_normal if args.colors else ""
            s += path
            try:
                print(s)
            except:
                pass

    with open(mru_db, 'w') as fp:
        json.dump(m.mru, fp)

if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main(sys.argv[1:])
