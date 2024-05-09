from typing import Any, Optional
import urllib.parse

from ...auth import (
    EditAccessRequest,
    GetAccessResponse,
    Permissions,
)
from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)
from ...query import QuerySpecification
from ...serde import pydantic_jsonable_dict
from ...updates import (
    MetadataChangeset,
    UpdateCondition,
)
from ..files import FileRecord
from .delegate import Credentials, DatasetDelegate
from .http_resources import (
    CreateDatasetRequest,
    QueryDatasetFilesRequest,
    UpdateDatasetRequest,
)
from .record import (
    Administrator,
    DatasetRecord,
    StorageLocation,
)


class DatasetHttpDelegate(DatasetDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def headers(
        self,
        org_id: Optional[str] = None,
        user_id: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> dict[str, str]:
        return roboto_headers(
            org_id=org_id,
            user_id=user_id,
            resource_owner_id=resource_owner_id,
            additional_headers={"Content-Type": "application/json"},
        )

    def create_dataset(
        self,
        administrator: Administrator = Administrator.Roboto,
        metadata: Optional[dict[str, Any]] = None,
        storage_location: StorageLocation = StorageLocation.S3,
        tags: Optional[list[str]] = None,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
        description: Optional[str] = None,
    ) -> DatasetRecord:
        """
        Create a new dataset.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets"
        request_body = CreateDatasetRequest(
            metadata=metadata if metadata is not None else {},
            description=description,
            tags=tags if tags is not None else [],
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body),
                headers=self.headers(org_id, created_by),
            )

        return DatasetRecord.model_validate(response.from_json(json_path=["data"]))

    def delete_dataset(self, record: DatasetRecord) -> None:
        """
        Delete a dataset.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}"

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url,
                headers=self.headers(),
            )

    def get_dataset_by_id(
        self,
        dataset_id: str,
    ) -> DatasetRecord:
        """
        Get a dataset by its primary key (org_id, dataset_id)
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=self.headers())

        return DatasetRecord.model_validate(response.from_json(json_path=["data"]))

    def get_temporary_credentials(
        self,
        record: DatasetRecord,
        permissions: Permissions,
        caller: Optional[str] = None,
        transaction_id: Optional[str] = None,
    ) -> Credentials:
        """
        Get temporary credentials to access a dataset.
        """
        query_params = {"mode": permissions.value}
        encoded_qs = urllib.parse.urlencode(query_params)
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}/credentials?{encoded_qs}"

        if transaction_id:
            url += f"&transaction_id={transaction_id}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, self.headers(user_id=caller))

        return Credentials.model_validate(response.from_json(json_path=["data"]))

    def list_files(
        self,
        dataset_id: str,
        page_token: Optional[str] = None,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> PaginatedList[FileRecord]:
        """
        List files associated with dataset.

        Files are associated with datasets in an eventually-consistent manner,
        so there will likely be delay between a file being uploaded and it appearing in this list.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}/files/query"
        if page_token:
            encoded_qs = urllib.parse.urlencode({"page_token": str(page_token)})
            url = f"{url}?{encoded_qs}"

        request_body = QueryDatasetFilesRequest(
            page_token=page_token,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )
        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(),
                idempotent=True,
            )

        unmarshalled = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[FileRecord.model_validate(file) for file in unmarshalled["items"]],
            next_token=unmarshalled["next_token"],
        )

    def query_datasets(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[DatasetRecord]:
        url = f"{self.__roboto_service_base_url}/v1/datasets/query"
        post_body = pydantic_jsonable_dict(query, exclude_none=True)
        with RobotoHttpExceptionParse():
            res = self.__http_client.post(
                url,
                data=post_body,
                headers=self.headers(resource_owner_id=org_id),
                idempotent=True,
            )

        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                DatasetRecord.model_validate(dataset)
                for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def update(
        self,
        record: DatasetRecord,
        metadata_changeset: Optional[MetadataChangeset] = None,
        conditions: Optional[list[UpdateCondition]] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> DatasetRecord:
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}"
        payload = UpdateDatasetRequest(
            metadata_changeset=metadata_changeset,
            description=description,
            conditions=conditions,
        )
        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(payload, exclude_none=True),
                headers=self.headers(user_id=updated_by),
            )

        return DatasetRecord.model_validate(response.from_json(json_path=["data"]))

    def get_access(self, record: DatasetRecord) -> GetAccessResponse:
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}/access"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=self.headers())

        return GetAccessResponse.model_validate(response.from_json(json_path=["data"]))

    def edit_access(
        self, record: DatasetRecord, edit: EditAccessRequest
    ) -> GetAccessResponse:
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}/access"

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url, data=edit.model_dump(mode="json"), headers=self.headers()
            )

        return GetAccessResponse.model_validate(response.from_json(json_path=["data"]))
