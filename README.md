For studying the differences between prior tmux versions to check compatibility with legacy
versions.

Get source:

```bash
$ git clone https://github.com/tmux/tmux
$ cd tmux
```

Converted with:

```bash
$ git checkout <version>
$ ./autogen.sh
$ ./configure
$ make
$ groff -t -e -mandoc -Tascii tmux.1 | col -bx > manpage.txt
```

repeat for versions.

Create a git-diff style diff of version manuals:

```bash
$ diff -u manual/1.6.txt manual/1.8.txt
```
