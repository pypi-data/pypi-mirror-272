-- Slice It Off! v0.4 --


Description:

	Small game where goal is to beat hiscores. Score is gained by
	slicing parts of playing area off. Faster you do it more score you
	get. If you hit smily face while slicing you lose a life. There will
	be also bonuses to boost the scores.


Installing:
	
	Get version on PyPI:
	- `pip install sliceitoff`


License:

	This project uses GPL-2 license. Assets have their licenses and
	copyrights listed on `src/sliceitoff/assets/COPYRIGHTS.txt`.


Developement:
	
	Project makes heavy use of poetry build and dependencies control
	system. Many shortcuts can be run easily from `./dev.sh` script:
	- `./dev.sh`
	- `./dev.sh dev`
	- `./dev.sh pytest`
	- `./dev.sh covff`
	- `./dev.sh all`
	- etc

	One can also use provided `./dev.sh` shell script to build and
	install	any developement version of game:
	- `./dev.sh install`
