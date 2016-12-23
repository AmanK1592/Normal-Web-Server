all:
	echo '#!/usr/bin/env python' | cat - multi.py > normal_web_server
	chmod +x normal_web_server
