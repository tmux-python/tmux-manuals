ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

start:
	ls parse_formats.py | entr -c '${ROOT_DIR}/parse_formats.py'
