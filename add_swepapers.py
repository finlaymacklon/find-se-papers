"""
Read papers from swepapers database then add data to the arxiv-sanity database.
"""
import os
import logging 
from pathlib import Path
from sqlalchemy import create_engine, text
from aslite.db import get_papers_db, get_metas_db
from dotenv import load_dotenv
import re


def setup_logger(file_name, logger_name=None):
    if logger_name is None:
        logger_name = file_name
    else:
        pass
    path_logs = Path("./log")
    path_logs.mkdir(exist_ok=True, parents=True)
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    log_file_name = f'{file_name}.log'
    log_file_path = path_logs / log_file_name
    log_format = logging.Formatter('%(name)s @ %(asctime)s [%(levelname)s] : %(message)s')
    file_handler = logging.FileHandler(log_file_path.as_posix(), mode='w')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger

def grab_paper_entries_from_swepapers():
    """Get a list of papers from swepapers database."""
    load_dotenv()
    engine = create_engine(f"postgresql://{os.environ['POSTGRES_SWEPAPERS_USERNAME']}:{os.environ['POSTGRES_SWEPAPERS_PASSWORD']}@localhost:{os.environ['POSTGRES_SWEPAPERS_PORT']}/swepapers")
    regex_pattern = r"\s+\b\d+\b"

    with engine.connect() as connection:
        result = connection.execute(text("SELECT authors, title, doi, year FROM papers"))
        list_of_papers = []

        for row in result:
            list_authors = row[0]
            string_title = row[1]
            string_doi = row[2]
            year = row[3]
            string_summary = ""

            if (list_authors is not None) and (string_title is not None) and (string_doi is not None) and (year is not None):
                if isinstance(list_authors, list):
                    list_authors = [re.sub(regex_pattern, "", author) for author in list_authors]
                else:
                    list_authors = [re.sub(regex_pattern, "", list_authors)]

                paper = {
                    "authors": list_authors,
                    "title": string_title,
                    "doi": string_doi,
                    "_id": string_doi,
                    "summary": string_summary,
                    "_time": year,
                }
                list_of_papers.append(paper)
            else:
                pass

    list_of_papers = sorted(list_of_papers, key=lambda x: x['_time'], reverse=True)
    return list_of_papers

def save_swepaper_to_arxiv_sanity(paper):
    """Save the papers from the swepapers database to the sqlite arxiv-sanity database"""
    required_keys = ['authors', 'title', 'summary', '_time', '_id']
    pdb = get_papers_db(flag='c')
    pdb[paper['doi']] = { k: paper[k] for k in required_keys }

def save_swepaper_time_to_arxiv_sanity(paper):
    """Save the papers from the swepapers database to the sqlite arxiv-sanity database"""
    mdb = get_metas_db(flag='c')
    mdb[paper['doi']] = {'_time': paper['_time'], "_id": paper["doi"]}

def main():
    """Main function."""
    logger = setup_logger("add_published_papers")
    list_papers = grab_paper_entries_from_swepapers()
    num_papers_swepapers = len(list_papers)
    for itr_i, paper in enumerate(list_papers):
        try:
            save_swepaper_to_arxiv_sanity(paper)
            save_swepaper_time_to_arxiv_sanity(paper)
        except:
            logger.error(f"Failed to process paper {paper['doi']}")

        print(f"Progress: {itr_i}/{num_papers_swepapers}", end="\r")

    print("Finished.")

if __name__ == '__main__':
    main()
