all:
	@echo "Run 'make install' to install json-wrap to /usr/local/bin"

install:
	install json-wrap.py /usr/local/bin/json-wrap

uninstall:
	rm -f /usr/local/bin/json-wrap