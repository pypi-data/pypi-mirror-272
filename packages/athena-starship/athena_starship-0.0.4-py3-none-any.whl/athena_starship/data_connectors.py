import os

import requests
from llama_index import download_loader
from swarms import create_file
from swarms.tools import tool


@tool
def load_airtable_data(table_id: str, base_id: str):
    """
    Loads data from Airtable using the provided credentials.

    Args:
        airtable_token (str): The API token for accessing Airtable.
        table_id (str): The ID of the table to load data from.
        base_id (str): The ID of the base containing the table.

    Returns:
        list: A list of documents retrieved from Airtable.
    """
    airtable_token = os.getenv("AIRTABLE_TOKEN")
    AirtableReader = download_loader("AirtableReader")
    reader = AirtableReader(airtable_token)
    documents = reader.load_data(table_id=table_id, base_id=base_id)

    return documents


# # Usage:
# airtable_token = os.getenv("AIRTABLE_TOKEN")
# table_id = os.getenv("TABLE_ID")
# base_id = os.getenv("BASE_ID")
# data = load_airtable_data(airtable_token, table_id, base_id)


def get_notion_pages(
    num_pages: int = None,
):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    DATABASE_ID = os.getenv("DATABASE_ID")

    notion_headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(
        url, json=payload, headers=notion_headers
    )

    data = response.json()

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {
            "page_size": page_size,
            "start_cursor": data["next_cursor"],
        }
        url = (
            f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        )
        response = requests.post(
            url, json=payload, headers=notion_headers
        )
        data = response.json()
        results.extend(data["results"])

    create_file(results, "notion_blob.txt")

    return results
