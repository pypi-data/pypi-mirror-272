import json
import os
from pydantic import BaseModel

# ENVIRONMENT VARIABLES
airtable_token = os.environ.get("AIRTABLE_TOKEN")
airtable_base_id = os.environ.get("AIRTABLE_BASE_ID")
airtable_table_id = os.environ.get("AIRTABLE_TABLE_ID")

# Notion ENVIRONMENT VARIABLES
notion_token = os.environ.get("NOTION_TOKEN")
notion_database_id = os.environ.get("NOTION_DATABASE_ID")


# SCHEMAS
def base_model_schema_to_json(model: BaseModel):
    """
    Converts the JSON schema of a base model to a formatted JSON string.

    Args:
        model (BaseModel): The base model for which to generate the JSON schema.

    Returns:
        str: The JSON schema of the base model as a formatted JSON string.
    """
    return json.dumps(model.model_json_schema(), indent=2)


class AirtableTableUpdate(BaseModel):
    """
    Represents an update to an Airtable table.

    Attributes:
        airtable_token (str): The Airtable API token.
        airtable_table_id (str): The ID of the Airtable table.
        airtable_base_id (str): The ID of the Airtable base.
        value (str): The value to be updated in the table.
    """

    airtable_token: str = airtable_token
    airtable_table_id: str = airtable_table_id
    airtable_base_id: str = airtable_base_id
    value: str


class NotionToolSchema(BaseModel):
    """
    Represents a schema for a Notion tool.

    Attributes:
        notion_token (str): The Notion token.
        notion_database_id (str): The Notion database ID.
        value (str): The value of the tool schema.
    """

    notion_token: str = notion_token
    notion_database_id: str = notion_database_id
    value: str


airtable_schema = base_model_schema_to_json(AirtableTableUpdate)

notion_tool_schema = base_model_schema_to_json(NotionToolSchema)
print(notion_tool_schema)
print(airtable_schema)
