"""
Main interface for resiliencehub service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_resiliencehub import (
        Client,
        ListAppAssessmentResourceDriftsPaginator,
        ResilienceHubClient,
    )

    session = Session()
    client: ResilienceHubClient = session.client("resiliencehub")

    list_app_assessment_resource_drifts_paginator: ListAppAssessmentResourceDriftsPaginator = client.get_paginator("list_app_assessment_resource_drifts")
    ```
"""

from .client import ResilienceHubClient
from .paginator import ListAppAssessmentResourceDriftsPaginator

Client = ResilienceHubClient

__all__ = ("Client", "ListAppAssessmentResourceDriftsPaginator", "ResilienceHubClient")
