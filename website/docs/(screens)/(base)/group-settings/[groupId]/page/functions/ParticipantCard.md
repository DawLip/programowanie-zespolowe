[**account_manager**](../../../../../../README.md)

***

[account_manager](../../../../../../modules.md) / [(screens)/(base)/group-settings/\[groupId\]/page](../README.md) / ParticipantCard

# Function: ParticipantCard()

> **ParticipantCard**(`props`): `Element`

Defined in: [(screens)/(base)/group-settings/\[groupId\]/page.tsx:236](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/group-settings/[groupId]/page.tsx#L236)

## Parameters

### props

Propsy komponentu

#### id

`string`

ID użytkownika

#### isActive

`boolean`

Status aktywności użytkownika

#### name

`string`

Imię użytkownika

#### removeMember

(`id`) => `void`

Funkcja do usuwania członka z grupy

#### role

`string`

Rola użytkownika (OWNER, ADMIN, USER)

#### setRole

(`id`, `role`) => `void`

Funkcja do zmiany roli użytkownika

#### surname

`string`

Nazwisko użytkownika

#### userRole

`string`

Rola aktualnego użytkownika

## Returns

`Element`
