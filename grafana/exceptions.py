"""
Module for Grafana related exceptions
"""


class GrafanaAPIError(Exception):
    """
    Class representing inexistence of Grafana API key.
    """

    def __str__(self) -> str:
        return """
            No Grafana API key was found. Please either directly input one, or run method
            create_api_key
            """


class NoDataSourceError(Exception):
    """
    Class representing inexistence of a Grafana DataSource.
    """

    def __str__(self) -> str:
        return """
            No Grafana Datasource was found. The method `add_database_source` can help solve
            this issue.
            """
