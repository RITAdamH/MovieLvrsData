# Users can sort tools by category or name (ascending and descending)

from typing import List


# Command: search b (barcode)
def inspect_tools(b: int) -> List[str]:
    tools = []
    # SQL

    # SELECT *
    # FROM tools
    # WHERE barcode = b
    # ORDER BY name ASC
    return tools


# Command: search n (name)
def inspect_tools(n: str) -> List[str]:
    tools = []
    # SQL

    # SELECT *
    # FROM tools
    # WHERE name = n
    # ORDER BY name ASC
    return tools


# Command: search c (category)
def inspect_tools(c: str) -> List[str]:
    tools = []
    # SQL

    # SELECT *
    # FROM tools
    # WHERE barcode =
    #   SELECT barcode
    #   FROM tool_categs
    #   WHERE cid =
    #       SELECT cid
    #       FROM categories
    #       where name = c
    # ORDER BY name ASC
    return tools


# Given status
def inspect_tools(s: int) -> List[str]:
    tools = []
    # Available SQL:

    # SELECT *
    # FROM tools
    # WHERE barcode =
    #   SELECT barcode
    #   FROM tool_reqs
    #   WHERE status = s
    # ORDER BY name ASC

    # Lent SQL:

    # SELECT *
    # FROM tools
    # WHERE barcode =
    #   SELECT barcode
    #   FROM tool_reqs
    #   WHERE status = s
    # ORDER BY (lend date)
    # (show the user that currently has tool)
    # (highlight overdue)

    # Borrowed SQL:

    # SELECT *
    # FROM tools
    # WHERE barcode =
    #   SELECT barcode
    #   FROM tool_reqs
    #   WHERE status = s
    # ORDER BY (lend date)
    # (show the user that owns the tool)
    # (highlight overdue)

    return tools
