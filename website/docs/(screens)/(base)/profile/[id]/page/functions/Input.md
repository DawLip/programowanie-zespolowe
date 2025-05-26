[**account_manager**](../../../../../../README.md)

***

[account_manager](../../../../../../modules.md) / [(screens)/(base)/profile/\[id\]/page](../README.md) / Input

# Function: Input()

> **Input**(`props`): `Element`

Defined in: [(screens)/(base)/profile/\[id\]/page.tsx:103](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/profile/[id]/page.tsx#L103)

Komponent Input wyświetlający etykietę oraz pole tekstowe lub tekst tylko do odczytu.

## Parameters

### props

Właściwości komponentu

#### editable?

`boolean`

Flaga czy pole jest edytowalne

#### label

`string`

Etykieta pola

#### long?

`boolean`

Flaga czy pole ma być długie (textarea) czy jednolinijkowe (input)

#### placeholder

`string`

Tekst zastępczy pola

#### setValue

`Function`

Funkcja aktualizująca wartość

#### value

`string`

Wartość pola

## Returns

`Element`

JSX z etykietą oraz odpowiednim polem (textarea/input lub span)
