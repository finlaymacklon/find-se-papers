
# I run this to update the database with newest papers every day or so or etc.
update:
	python3 arxiv_daemon.py --num 2000
	python3 compute.py

# I use this to run the server
run:
	export FLASK_APP=serve.py; flask run

# Insert entries from swepapers to the database and re-train (only needed once)
add_swepapers:
	python3 add_swepapers.py
	python3 compute.py
