from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEETS_BODY = {
    "properties": {
        "title": "",
        "locale": "ru_RU"
    },
    "sheets": [{
        "properties": {
            "sheetType": "GRID",
            "sheetId": 0,
            "title": "Отчет",
            "gridProperties": {"rowCount": 20, "columnCount": 4}
        }
    }]
}
PERMISSIONS_BODY = {
    "type": "user",
    "role": "writer",
    "emailAddress": settings.email
}
TABLE_VALUES = [
    ["Отчёт от", ""],
    ["ТОП выполненных проектов (время сбора)"],
    ["Название проекта", "Время сбора", "Описание", "Сумма"]
]
UPDATE_BODY = {
    "majorDimension": "ROWS",
    "values": TABLE_VALUES
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover("sheets", "v4")
    SPREADSHEETS_BODY["properties"]["title"] = "Инвестирование"
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEETS_BODY)
    )
    spreadsheet_id = response["spreadsheetId"]
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=PERMISSIONS_BODY, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, project_list: list, wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    TABLE_VALUES[0][1] = now_date_time
    for project in project_list:
        new_row = [
            str(project[0]),
            str(project[2]),
            str(project[3]),
            str(project[4]),
        ]
        TABLE_VALUES.append(new_row)

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range="A1:D100",
            valueInputOption="USER_ENTERED",
            json=UPDATE_BODY,
        )
    )
