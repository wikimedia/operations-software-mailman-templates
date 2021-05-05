install:
	python3 make.py export --destdir=$(DESTDIR)

sync:
	python3 make.py sync

test:
	python3 make.py test
