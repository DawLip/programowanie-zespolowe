[**account_manager**](../../../../../../README.md)

***

[account_manager](../../../../../../modules.md) / [(screens)/(base)/group-settings/\[groupId\]/page](../README.md) / default

# Function: default()

> **default**(`props`): `Element`

Defined in: [(screens)/(base)/group-settings/\[groupId\]/page.tsx:22](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/group-settings/[groupId]/page.tsx#L22)

Strona ustawień grupy GroupSettings
Umożliwia zarządzanie ustawieniami grupy, w tym:
- wyświetlanie i edycję nazwy i opisu grupy,
- dodawanie i usuwanie członków,
- zmiana ról członków,
- filtrowanie członków według ról (OWNER, ADMIN, USER).

## Parameters

### props

Właściwości komponentu

#### params

`Promise`\<\{ `groupId`: `string`; \}\>

Promise zawierający ID grupy

## Returns

`Element`

JSX element strony ustawień grupy
