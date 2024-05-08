"""
Type annotations for resiliencehub service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_resiliencehub.client import ResilienceHubClient
    from mypy_boto3_resiliencehub.paginator import (
        ListAppAssessmentResourceDriftsPaginator,
    )

    session = Session()
    client: ResilienceHubClient = session.client("resiliencehub")

    list_app_assessment_resource_drifts_paginator: ListAppAssessmentResourceDriftsPaginator = client.get_paginator("list_app_assessment_resource_drifts")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListAppAssessmentResourceDriftsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListAppAssessmentResourceDriftsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAppAssessmentResourceDriftsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Paginator.ListAppAssessmentResourceDrifts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/paginators/#listappassessmentresourcedriftspaginator)
    """

    def paginate(
        self, *, assessmentArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAppAssessmentResourceDriftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Paginator.ListAppAssessmentResourceDrifts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/paginators/#listappassessmentresourcedriftspaginator)
        """
