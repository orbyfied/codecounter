#
# Code Counter by Orbyfied (2023)
# codecounter.py
#

import sys
import os
import re

############################
### Utility
############################

# walks the file tree of directories
# matching the given dir filter and
# executes the given function for
# each file matching the given file filter
# and returns the amount of files and dirs walked
def checked_recursive_walk(root_dir : str, dir_filter, file_filter, func):
    wFiles = 0
    wDirs  = 0
    
    for fn in os.listdir(root_dir):
        pth = os.path.join(root_dir, fn)

        # filter and walk directory
        if os.path.isdir(pth):
            if (dir_filter(pth, fn)):
                wDir += 1
                f, d = checked_recursive_walk(pth, dir_filter, file_filter, func)
                wFiles += f
                wDirs += d
        else: # filter and pass file
            if (file_filter(pth, fn)):
                wFiles += 1
                func(pth, fn)

    return wFiles, wDirs

############################
### CC
############################

class Counted:
    def __init__(self, file) -> None:
        self.file = file

        self.total_lines = 0
        self.not_ws_lines = 0

class CContext:
    def __init__(self, work_dir) -> None:
        self.work_dir = work_dir

        self.dir_filter  = re.compile(".*")
        self.file_filter = re.compile(".*")

        self.counted = { }

    def filter_file(self, path, name):
        return re.match(self.file_filter, name)
    
    def filter_dir(self, path, name):
        return re.match(self.file_filter, name)
    
def count_lines_in_file(context : CContext, file : str) -> Counted:
    c = Counted(file)
    with open(file, "r+") as f:
        for ln in f.readlines():
            # classify line
            c.total_lines += 1
            if not ln.isspace():
                c.not_ws_lines += 1

    print("codecounter: counted file(" + file + ") ln_total(" + str(c.total_lines) + ") ln_not_ws(" + str(c.not_ws_lines) + ")")

    return c

def print_help():
    pass # todo

def print_results(context : CContext):
    s_total_lines = 0
    s_not_ws_lines = 0
    for _, r in context.counted.items():
        s_total_lines += r.total_lines
        s_not_ws_lines += r.not_ws_lines

    print("codecounter: {")
    print("   total lines: " + str(s_total_lines))
    print("   non-blank lines: " + str(s_not_ws_lines))
    print("}")
    pass # todo

# entry point #
def main(argv):
    work_dir = None
    if len(argv) < 2:
        print("codecounter: setting ./ as work dir")
        work_dir = "./"
    else:
        if argv[1] == '?': # display help
            print_help()
            return
        work_dir = argv[1]
        print("codecounter: work dir(" + work_dir + ")")

    context = CContext(work_dir)

    # parse rest of argv
    if (len(argv) > 2):
        for argIdx in range(2, len(argv)):
            arg = argv[argIdx]
            argSplit = str(arg).split(":")

            name = argSplit[0]
            value = argSplit[1]

            match name:
                case "file-filter", "filefilter", "ff":
                    context.file_filter = re.compile(value)
                    print("codecounter: file-filter(" + value + ")")
                    continue
                case "dir-filter", "dirfilter", "df":
                    context.dir_filter = re.compile(value)
                    print("codecounter: dir-filter(" + value + ")")
                    continue

    # recursively iterate from work dir
    def _dir_filter(pth, fn):
        return context.filter_dir(pth, fn)
    def _file_filter(pth, fn):
        return context.filter_file(pth, fn)
    def _file_func(pth, fn):
        context.counted[pth] = count_lines_in_file(context, pth)

    checked_recursive_walk(work_dir, _dir_filter, _file_filter, _file_func)

    # print results
    print_results(context)

if __name__ == "__main__":
    main(sys.argv)