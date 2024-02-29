from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (
    DRIVE_SERVICE, DRIVE_SERVICE_VERSION,
    FORMAT, SHEETS, SHEETS_SERVICE,
    SHEETS_SERVICE_VERSION, TABLE_HEADERS,
    TABLE_TITLE, TITLE
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:

    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_services.discover(
        SHEETS_SERVICE, SHEETS_SERVICE_VERSION
    )

    spreadsheet_body = {
        'properties': {'title': TITLE.format(now_date_time=now_date_time),
                       'locale': 'ru_RU'},
        'sheets': SHEETS
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover(
        DRIVE_SERVICE, DRIVE_SERVICE_VERSION
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        SHEETS_SERVICE, SHEETS_SERVICE_VERSION
    )

    table_values = [
        ['Отчёт от', now_date_time],
        [TABLE_TITLE],
        TABLE_HEADERS
    ]

    for res in charity_projects:
        new_row = [str(res['name']), str(res['duration']),
                   str(res['description'])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
