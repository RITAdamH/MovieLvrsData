# Users can sort tools by category or name (ascending and descending)

from typing import List


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
