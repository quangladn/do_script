install-unix:
	cp src/doS.py ~/../usr/bin/doS
	cp src/debug.do.py ~/../usr/bin/doS.de
install-linux:
	cp src/doS.py ~/../usr/local/bin/doS
	cp src/debug.do.py ~/../usr/local/bin/doS
build-exe:
	pyinstaller src/doS.py --onefile -w
	pyinstaller src/debug.do.py --onefile -w
