# Quickstart

How to set up and run an instance of this website.

## Setting up database

1. Seperately set up the SWE Papers database using instructions in `ZeinabAk/DatasetSEVenues`
2. Set up the `.env` file (referencing `.env.example`) for this repository
3. Run `python3 arxiv_daemon.py --num 2000` to get the arXiv entries (`data/papers.db`)
    - Adjust the `--num` parameter to get more arXiv entries, if desired
4. Run `python3 add_swepapers.py` to add the swepapers entries (to `data/papers.db`)
5. Run `python3 compute.py` to train the TF-IDF features (`data/features.p`)

### Searching other fields of research on arXiv

This project can also be used to search other fields of research that are listed on arXiv. To do so, the following adjustments would be required before/while setting up the database:

- Before setting up the database:
    - In the file `arxiv_daemon.py`, around line 33 (`q = 'cat:cs.SE'`) replace `cat:cs.SE` with your desired category (or categories).
        - Examples:
            - Replace `cat:cs.SE` with `cat:eess.SP` to index and search papers in the "Signal Processing" category.
            - Replace `cat:cs.SE` with `cat:cs.SE+OR+cat:cs.PL` to index and search papers across both the "Software Engineering" and "Programming Languages" categories.

- When setting up the database (as outlined above):
    - Only perform step 3 and step 5.

## Hosting a public version on Linode - Config 

A public version of this website can be hosted on, for example, Linode.
The documentation links below may be helpful if setting up a public version hosted on Linode.

### Linode (Flask with GUnicorn, Supervisord, and Certbot)

- https://www.linode.com/docs/guides/flask-and-gunicorn-on-ubuntu/
- https://www.linode.com/docs/guides/enabling-https-using-certbot-with-nginx-on-debian/
