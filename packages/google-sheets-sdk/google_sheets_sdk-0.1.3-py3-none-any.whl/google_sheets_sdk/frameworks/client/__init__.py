from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, ClassVar

from entities import Settings, Sheet, Token
from entities import spreadsheet as spreadsheet_entity
from pydantic import BaseModel
from pydantic.fields import Field

if TYPE_CHECKING:
    from httpx import AsyncClient, HTTPStatusError


class BatchUpdateValuesResponse(BaseModel):
    spreadsheet_id: str = Field(
        ...,
        alias="spreadsheetId",
    )
    total_updated_rows: int = Field(
        ...,
        alias="totalUpdatedRows",
    )
    total_updated_columns: int = Field(
        ...,
        alias="totalUpdatedColumns",
    )
    total_updated_cells: int = Field(
        ...,
        alias="totalUpdatedCells",
    )
    total_updated_sheets: int = Field(
        ...,
        alias="totalUpdatedSheets",
    )


@dataclass
class Client:
    _base_url: ClassVar[str] = "https://sheets.googleapis.com/"

    _http_client: "AsyncClient"
    _token: Token = field(
        init=False,
    )
    settings: InitVar[Settings]

    def __post_init__(
        self,
        settings: Settings,
    ):
        self._token = Token(
            email=settings.CLIENT_EMAIL,
            base_url=self._base_url,
            scope=settings.SCOPE.unicode_string(),
            private_key=settings.PRIVATE_KEY.replace(r"\n", "\n"),
            private_key_id=settings.PRIVATE_KEY_ID,
        )

    async def batch_clear_values(
        self,
        spreadsheet_id: spreadsheet_entity.Id,
        ranges: list[str],
    ) -> None:
        try:
            response = await self._http_client.post(
                url=f"{self._base_url}v4/spreadsheets/{spreadsheet_id}/values:batchClear",
                json={
                    "ranges": ranges,
                },
                headers={
                    "Authorization": f"Bearer {self._token.encoded}",
                },
            )
            response.raise_for_status()
        except HTTPStatusError as exc:
            raise exc

    async def batch_update_values(
        self,
        spreadsheet_id: spreadsheet_entity.Id,
        sheets: list[Sheet],
    ) -> BatchUpdateValuesResponse:
        try:
            response = await self._http_client.post(
                url=f"{self._base_url}v4/spreadsheets/{spreadsheet_id}/values:batchUpdate",
                json={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        sheet.model_dump(
                            mode="json",
                        )
                        for sheet in sheets
                    ],
                },
                headers={
                    "Authorization": f"Bearer {self._token.encoded}",
                },
            )
            response.raise_for_status()
        except HTTPStatusError as exc:
            raise exc
        else:
            return BatchUpdateValuesResponse(**response.json())
