import os.path
import subprocess


def count_lines(filename):
    s = sum(1 for _ in open(filename, encoding="utf8"))
    return s


def count_symbol(filename):
    file_n = open(filename, encoding="utf8")
    s = len(file_n.read())
    return s


if __name__ == '__main__':
    out = subprocess.run(["git", "ls-files"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    ls = out.split("\n")[0:-1]
    lines = 0
    symbols = 0
    for file in ls:
        lines += count_lines(os.path.abspath(file))
        symbols += count_symbol(os.path.abspath(file))
    print(str(lines))
    print(str(symbols))
