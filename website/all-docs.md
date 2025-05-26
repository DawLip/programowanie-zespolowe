[**account_manager**](README.md)

***

# account_manager

## Modules

- [(screens)/(auth)/login/page]((screens)/(auth)/login/page/README.md)
- [(screens)/(auth)/register/page]((screens)/(auth)/register/page/README.md)
- [(screens)/(base)/chat/\[chatType\]/\[id\]/page]((screens)/(base)/chat/[chatType]/[id]/page/README.md)
- [(screens)/(base)/group-settings/\[groupId\]/page]((screens)/(base)/group-settings/[groupId]/page/README.md)
- [(screens)/(base)/layout]((screens)/(base)/layout/README.md)
- [(screens)/(base)/page]((screens)/(base)/page/README.md)
- [(screens)/(base)/profile/\[id\]/page]((screens)/(base)/profile/[id]/page/README.md)
- [(screens)/(base)/settings/page]((screens)/(base)/settings/page/README.md)
- [(screens)/layout]((screens)/layout/README.md)
- [colors](colors/README.md)
- [components](components/README.md)
- [components/Aside](components/Aside/README.md)
- [components/Button](components/Button/README.md)
- [components/Divider](components/Divider/README.md)
- [components/Header](components/Header/README.md)
- [components/Icon](components/Icon/README.md)
- [components/Message](components/Message/README.md)
- [components/ProfileImage](components/ProfileImage/README.md)
- [components/Section](components/Section/README.md)
- [components/TextInput](components/TextInput/README.md)
- [components/UserCard](components/UserCard/README.md)
- [config](config/README.md)
- [layout](layout/README.md)
- [socket](socket/README.md)



**account_manager**

***

# ChatApp
### Project: Web Application for User Communication 
- The application allows user database management through a login system. Users can only edit or delete their own accounts. They can send private messages to each other and create group chats. The project emphasizes simplicity, security, and an intuitive interface.  
### Key Features:  
- **User Database Management**: Secure login/authentication system.  
- **Account Control**: Users can only modify or delete their own accounts.  
- **Communication Tools**: Private messaging and group chat functionality.  
- **Design Principles**: Focus on simplicity, security, and user-friendly interface.
## Instalation and run
### Frontend:
Instalation:
```
cd website
npm i
```
Run for development ```npm run dev```  

### Backend
#### Requirements  
- Python 3.9+  
- SQLite

#### Installation  
```bash
cd backend\utils  
pip install -r requirements.txt
```

#### Run Server  
```bash
flask run --port=5000 --debug
```



[**account_manager**](../README.md)

***

[account_manager](../modules.md) / colors

# colors

## Variables

- [default](variables/default.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [colors](../README.md) / default

# Variable: default

> `const` **default**: `object`

Defined in: [colors.tsx:5](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/colors.tsx#L5)

Obiekt colors zawierający stałe kolory używane w aplikacji

## Type declaration

### border

> **border**: `string` = `"#7B7B7B"`

### on\_surface\_gray

> **on\_surface\_gray**: `string` = `"#565656"`

### on\_surface\_light\_gray

> **on\_surface\_light\_gray**: `string` = `"#A0A0A0"`

### on\_surface\_white

> **on\_surface\_white**: `string` = `"#EAE5E5"`

### primary

> **primary**: `string` = `"#680B8A"`

### red

> **red**: `string` = `"#FF0000"`



[**account_manager**](../README.md)

***

[account_manager](../modules.md) / components

# components

## Functions

- [Header](functions/Header.md)
- [Icon](functions/Icon.md)
- [Message](functions/Message.md)
- [ProfileImage](functions/ProfileImage.md)
- [Section](functions/Section.md)
- [TextInput](functions/TextInput.md)
- [UserCard](functions/UserCard.md)

## References

### Aside

Renames and re-exports [default](Aside/functions/default.md)

***

### Button

Renames and re-exports [default](Button/functions/default.md)

***

### Divider

Renames and re-exports [default](Divider/functions/default.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/Aside

# components/Aside

## Functions

- [default](functions/default.md)
- [FriendsGroupButton](functions/FriendsGroupButton.md)
- [UserCard](functions/UserCard.md)



[**account_manager**](../../../README.md)

***

[account_manager](../../../modules.md) / [components/Aside](../README.md) / default

# Function: default()

> **default**(`props`): `Element`

Defined in: [components/Aside.tsx:21](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Aside.tsx#L21)

Komponent Aside wyświetlający listę użytkowników lub grup oraz przycisk do tworzenia grup

## Parameters

### props

obiekt właściwości komponentu

#### groups

`any`

lista grup do wyświetlenia

#### users

`any`

lista użytkowników do wyświetlenia

## Returns

`Element`

- komponent



[**account_manager**](../../../README.md)

***

[account_manager](../../../modules.md) / [components/Aside](../README.md) / FriendsGroupButton

# Function: FriendsGroupButton()

> **FriendsGroupButton**(`props`): `Element`

Defined in: [components/Aside.tsx:101](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Aside.tsx#L101)

Przycisk wyboru pomiędzy listą przyjaciół a listą grup

## Parameters

### props

obiekt właściwości komponentu

#### callback

`Function`

funkcja zmieniająca widok (przyjaciele/grupy)

#### checked

`boolean`

czy przycisk jest aktualnie wybrany

#### label

`string`

etykieta przycisku ("Friends" lub "Groups")

## Returns

`Element`

- komponent



[**account_manager**](../../../README.md)

***

[account_manager](../../../modules.md) / [components/Aside](../README.md) / UserCard

# Function: UserCard()

> **UserCard**(`props`): `Element`

Defined in: [components/Aside.tsx:78](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Aside.tsx#L78)

Komponent karty użytkownika

## Parameters

### props

obiekt właściwości komponentu

#### onClick?

() => `void`

funkcja wywoływana po kliknięciu na kartę (opcjonalna)

#### user

`any`

obiekt reprezentujący użytkownika lub grupę

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/Button

# components/Button

## Functions

- [default](functions/default.md)



[**account_manager**](../../../README.md)

***

[account_manager](../../../modules.md) / [components/Button](../README.md) / default

# Function: default()

> **default**(`props`): `Element`

Defined in: [components/Button.tsx:12](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Button.tsx#L12)

Komponent Button wyświetlający przycisk z trzema wariantami stylów

## Parameters

### props

obiekt właściwości komponentu

#### label

`string`

tekst na przycisku

#### onClick

() => `void`

funkcja wywoływana po kliknięciu przycisku

#### type?

`"filled"` \| `"outlined"` \| `"outlined2"` = `"filled"`

typ przycisku: "filled" | "outlined" | "outlined2" (domyślnie "filled")

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/Divider

# components/Divider

## Functions

- [default](functions/default.md)



[**account_manager**](../../../README.md)

***

[account_manager](../../../modules.md) / [components/Divider](../README.md) / default

# Function: default()

> **default**(`props`): `Element`

Defined in: [components/Divider.tsx:12](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Divider.tsx#L12)

Komponent Divider wyświetlający poziomy lub pionowy pasek podziału

## Parameters

### props

obiekt właściwości komponentu

#### color

`string`

kolor tła paska

#### horizontal?

`boolean`

jeśli true, pasek jest poziomy

#### vertical?

`boolean`

jeśli true, pasek jest pionowy

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [components](../README.md) / Header

# Function: Header()

> **Header**(`props`): `Element`

Defined in: [components/Header.tsx:21](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Header.tsx#L21)

Komponent Header wyświetlający nagłówek strony

## Parameters

### props

obiekt właściwości komponentu

#### backArrow?

`boolean`

czy wyświetlać strzałkę wstecz (opcjonalne)

#### header

`any`

zawartość nagłówka

#### userProfileSrc?

`string`

adres URL zdjęcia profilowego użytkownika (opcjonalne)

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [components](../README.md) / Icon

# Function: Icon()

> **Icon**(`props`): `Element`

Defined in: [components/Icon.tsx:12](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Icon.tsx#L12)

Komponent Icon wyświetlający ikonę

## Parameters

### props

obiekt właściwości komponentu

#### onClick

() => `void`

funkcja wywoływana po kliknięciu na ikonę

#### size

`number`

rozmiar ikony

#### src?

`string`

źródło obrazka (jeśli pusty, wyświetlany jest obraz domyślny)

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [components](../README.md) / Message

# Function: Message()

> **Message**(`props`): `Element`

Defined in: [components/Message.tsx:15](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Message.tsx#L15)

Komponent Message wyświetlający pojedynczą wiadomość

## Parameters

### props

obiekt właściwości komponentu

#### children

`any`

zawartość wiadomości

#### isFirst?

`Boolean`

czy jest to pierwsza wiadomość w grupie wiadomości (opcjonalne)

#### isLast?

`Boolean`

czy jest to ostatnia wiadomość w grupie wiadomości (opcjonalne)

#### isUserAuthor?

`Boolean`

czy autorem wiadomości jest użytkownik (domyślnie false)

#### name?

`string`

imię autora wiadomości (opcjonalne)

#### src?

`string`

adres URL zdjęcia profilowego autora wiadomości

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [components](../README.md) / ProfileImage

# Function: ProfileImage()

> **ProfileImage**(`props`): `Element`

Defined in: [components/ProfileImage.tsx:10](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/ProfileImage.tsx#L10)

Komponent ProfileImage wyświetlający okrągłe zdjęcie profilowe z oznaczeniem aktywności

## Parameters

### props

obiekt właściwości komponentu

#### isActive?

`Boolean`

czy użytkownik jest aktywny (opcjonalne)

#### size

`number`

rozmiar obrazka (szerokość i wysokość w px)

#### src

`string`

adres URL zdjęcia profilowego

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [components](../README.md) / Section

# Function: Section()

> **Section**(`props`): `Element`

Defined in: [components/Section.tsx:10](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/Section.tsx#L10)

Komponent Section wyświetlający sekcję z nagłówkiem i zawartością

## Parameters

### props

obiekt właściwości komponentu

#### children

`any`

zawartość sekcji

#### header

`String`

nazwa sekcji

#### onClick?

() => `void`

funkcja wywoływana po kliknięciu na sekcję (opcjonalne)

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [components](../README.md) / TextInput

# Function: TextInput()

> **TextInput**(`props`): `Element`

Defined in: [components/TextInput.tsx:15](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/TextInput.tsx#L15)

Komponent Input wyświetlający pole do wprowadzania textu z etykietą

## Parameters

### props

obiekt właściwości komponentu

#### label

`string`

etykieta pola

#### long?

`boolean`

czy użyć pola textarea zamiast input (opcjonalne)

#### password?

`boolean`

czy pole jest typu hasło (opcjonalne)

#### placeholder?

`string`

tekst zastępczy w polu (opcjonalny)

#### setValue

`Function`

funkcja ustawiająca nową wartość pola

#### value

`string`

aktualna wartość pola

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [components](../README.md) / UserCard

# Function: UserCard()

> **UserCard**(`props`): `Element`

Defined in: [components/UserCard.tsx:18](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/components/UserCard.tsx#L18)

Komponent UserCard wyświetlający kartę użytkownika

## Parameters

### props

obiekt właściwości komponentu

#### buttons?

`any`

opcjonalne przyciski do wyświetlenia obok nazwy (opcjonalne)

#### children?

`any`

kontent karty (opcjonalne)

#### className?

`string`

klasy (opcjonalne)

#### isActive

`Boolean`

czy użytkownik jest aktywny

#### name

`String`

imię użytkownika

#### onClick?

() => `void`

funkcja wywoływana po kliknięciu na element z imieniem i nazwiskiem (opcjonalne)

#### onClickCard?

() => `void`

funkcja wywoływana po kliknięciu na całą kartę (opcjonalne)

#### style?

`any`

dodatkowe stylowanie (opcjonalne)

#### surname

`String`

nazwisko użytkownika

## Returns

`Element`

- komponent



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/Header

# components/Header

## References

### default

Renames and re-exports [Header](../functions/Header.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/Icon

# components/Icon

## References

### default

Renames and re-exports [Icon](../functions/Icon.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/Message

# components/Message

## References

### default

Renames and re-exports [Message](../functions/Message.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/ProfileImage

# components/ProfileImage

## References

### default

Renames and re-exports [ProfileImage](../functions/ProfileImage.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/Section

# components/Section

## References

### default

Renames and re-exports [Section](../functions/Section.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/TextInput

# components/TextInput

## References

### default

Renames and re-exports [TextInput](../functions/TextInput.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / components/UserCard

# components/UserCard

## References

### default

Renames and re-exports [UserCard](../functions/UserCard.md)



[**account_manager**](../README.md)

***

[account_manager](../modules.md) / config

# config

## Variables

- [default](variables/default.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [config](../README.md) / default

# Variable: default

> `const` **default**: `object`

Defined in: [config.tsx:4](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/config.tsx#L4)

Konfiguracja aplikacji zawierająca adres API

## Type declaration

### api

> **api**: `string` = `"http://localhost:5000"`



[**account_manager**](../README.md)

***

[account_manager](../modules.md) / layout

# layout

## Variables

- [metadata](variables/metadata.md)

## Functions

- [default](functions/default.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [layout](../README.md) / default

# Function: default()

> **default**(`props`): `Element`

Defined in: [layout.tsx:21](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/layout.tsx#L21)

Główny layout

## Parameters

### props

`Readonly`\<\{ `children`: `ReactNode`; \}\>

obiekt właściwości komponentu

## Returns

`Element`

Layout



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [layout](../README.md) / metadata

# Variable: metadata

> `const` **metadata**: `Metadata`

Defined in: [layout.tsx:12](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/layout.tsx#L12)



[**account_manager**](../../../../README.md)

***

[account_manager](../../../../modules.md) / (screens)/(auth)/login/page

# (screens)/(auth)/login/page

## Functions

- [default](functions/default.md)



[**account_manager**](../../../../../README.md)

***

[account_manager](../../../../../modules.md) / [(screens)/(auth)/login/page](../README.md) / default

# Function: default()

> **default**(): `Element`

Defined in: [(screens)/(auth)/login/page.tsx:19](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(auth)/login/page.tsx#L19)

Strona logowania.
Zarządza formularzem logowania użytkownika.

## Returns

`Element`

Strona logowania.



[**account_manager**](../../../../README.md)

***

[account_manager](../../../../modules.md) / (screens)/(auth)/register/page

# (screens)/(auth)/register/page

## Functions

- [default](functions/default.md)



[**account_manager**](../../../../../README.md)

***

[account_manager](../../../../../modules.md) / [(screens)/(auth)/register/page](../README.md) / default

# Function: default()

> **default**(): `Element`

Defined in: [(screens)/(auth)/register/page.tsx:19](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(auth)/register/page.tsx#L19)

Strona rejestracji użytkownika.
Zarządza formularzem rejestracji oraz przesyłaniem danych do API.

## Returns

`Element`

Strona rejestracji.



[**account_manager**](../../../../../../README.md)

***

[account_manager](../../../../../../modules.md) / (screens)/(base)/chat/\[chatType\]/\[id\]/page

# (screens)/(base)/chat/\[chatType\]/\[id\]/page

## Functions

- [default](functions/default.md)
- [LabeledContent](functions/LabeledContent.md)



[**account_manager**](../../../../../../../README.md)

***

[account_manager](../../../../../../../modules.md) / [(screens)/(base)/chat/\[chatType\]/\[id\]/page](../README.md) / default

# Function: default()

> **default**(`props`): `Element`

Defined in: [(screens)/(base)/chat/\[chatType\]/\[id\]/page.tsx:17](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/chat/[chatType]/[id]/page.tsx#L17)

Strona chatu
Umożliwia chatowanie prywatne oraz grupowe

## Parameters

### props

`any`

Właściwości komponentu (nieużywane)

## Returns

`Element`

Strona czatu



[**account_manager**](../../../../../../../README.md)

***

[account_manager](../../../../../../../modules.md) / [(screens)/(base)/chat/\[chatType\]/\[id\]/page](../README.md) / LabeledContent

# Function: LabeledContent()

> **LabeledContent**(`props`): `Element`

Defined in: [(screens)/(base)/chat/\[chatType\]/\[id\]/page.tsx:196](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/chat/[chatType]/[id]/page.tsx#L196)

## Parameters

### props

#### content

`string`

Zawartość tekstowa

#### label

`string`

Tekst etykiety

#### long?

`boolean`

Flaga do wyświetlania dłuższego tekstu

## Returns

`Element`

Komponent



[**account_manager**](../../../../../README.md)

***

[account_manager](../../../../../modules.md) / (screens)/(base)/group-settings/\[groupId\]/page

# (screens)/(base)/group-settings/\[groupId\]/page

## Functions

- [default](functions/default.md)
- [LabeledContent](functions/LabeledContent.md)
- [LineInput](functions/LineInput.md)
- [ParticipantCard](functions/ParticipantCard.md)



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



[**account_manager**](../../../../../../README.md)

***

[account_manager](../../../../../../modules.md) / [(screens)/(base)/group-settings/\[groupId\]/page](../README.md) / LabeledContent

# Function: LabeledContent()

> **LabeledContent**(`props`): `Element`

Defined in: [(screens)/(base)/group-settings/\[groupId\]/page.tsx:268](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/group-settings/[groupId]/page.tsx#L268)

## Parameters

### props

#### children?

`any`

Dzieci komponentu

#### content?

`string`

Opcjonalna zawartość tekstowa

#### label

`string`

Tekst etykiety

#### long?

`boolean`

Flaga do wyświetlania dłuższego tekstu (większa czcionka)

## Returns

`Element`

Komponent



[**account_manager**](../../../../../../README.md)

***

[account_manager](../../../../../../modules.md) / [(screens)/(base)/group-settings/\[groupId\]/page](../README.md) / LineInput

# Function: LineInput()

> **LineInput**(`props`): `Element`

Defined in: [(screens)/(base)/group-settings/\[groupId\]/page.tsx:283](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/group-settings/[groupId]/page.tsx#L283)

## Parameters

### props

#### placeholder

`string`

Tekst zastępczy

#### setValue

`Function`

Funkcja aktualizująca wartość inputa

#### value

`string`

Wartość inputa

## Returns

`Element`

Komponent



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



[**account_manager**](../../../README.md)

***

[account_manager](../../../modules.md) / (screens)/(base)/layout

# (screens)/(base)/layout

## Functions

- [default](functions/default.md)



[**account_manager**](../../../../README.md)

***

[account_manager](../../../../modules.md) / [(screens)/(base)/layout](../README.md) / default

# Function: default()

> **default**(`props`): `null` \| `Element`

Defined in: [(screens)/(base)/layout.tsx:18](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/layout.tsx#L18)

Layout strony

## Parameters

### props

Właściwości komponentu

#### children

`any`

Elementy potomne renderowane wewnątrz layoutu

## Returns

`null` \| `Element`

Layout



[**account_manager**](../../../README.md)

***

[account_manager](../../../modules.md) / (screens)/(base)/page

# (screens)/(base)/page

## Functions

- [default](functions/default.md)



[**account_manager**](../../../../README.md)

***

[account_manager](../../../../modules.md) / [(screens)/(base)/page](../README.md) / default

# Function: default()

> **default**(): `Element`

Defined in: [(screens)/(base)/page.tsx:16](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/page.tsx#L16)

Strona główna 
Wyświetla dashboard użytkownika z listą znajomych, grup i zaproszeń do znajomych.

## Returns

`Element`

Strona główna



[**account_manager**](../../../../../README.md)

***

[account_manager](../../../../../modules.md) / (screens)/(base)/profile/\[id\]/page

# (screens)/(base)/profile/\[id\]/page

## Functions

- [default](functions/default.md)
- [Input](functions/Input.md)
- [LineInput](functions/LineInput.md)



[**account_manager**](../../../../../../README.md)

***

[account_manager](../../../../../../modules.md) / [(screens)/(base)/profile/\[id\]/page](../README.md) / default

# Function: default()

> **default**(`props`): `Element`

Defined in: [(screens)/(base)/profile/\[id\]/page.tsx:18](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/profile/[id]/page.tsx#L18)

Strona profilu użytkownika.
Umożliwia przeglądanie profili urzytkowników

## Parameters

### props

Właściwości komponentu

#### params

\{ `id`: `string`; \}

Parametry trasy zawierające ID użytkownika

#### params.id

`string`

## Returns

`Element`

Strona profilu użytkownika



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



[**account_manager**](../../../../../../README.md)

***

[account_manager](../../../../../../modules.md) / [(screens)/(base)/profile/\[id\]/page](../README.md) / LineInput

# Function: LineInput()

> **LineInput**(`props`): `Element`

Defined in: [(screens)/(base)/profile/\[id\]/page.tsx:85](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/profile/[id]/page.tsx#L85)

Komponent wyświetlający jednoliniowy tekst (tylko do odczytu).

## Parameters

### props

Właściwości komponentu

#### placeholder

`string`

Tekst zastępczy wyświetlany, gdy wartość jest pusta

#### setValue

`Function`

Funkcja ustawiająca wartość (nieużywana, bo komponent jest tylko do odczytu)

#### value

`string`

Wyświetlana wartość tekstowa

## Returns

`Element`

JSX z tekstem wyświetlanym w divie



[**account_manager**](../../../../README.md)

***

[account_manager](../../../../modules.md) / (screens)/(base)/settings/page

# (screens)/(base)/settings/page

## Functions

- [default](functions/default.md)



[**account_manager**](../../../../../README.md)

***

[account_manager](../../../../../modules.md) / [(screens)/(base)/settings/page](../README.md) / default

# Function: default()

> **default**(): `Element`

Defined in: [(screens)/(base)/settings/page.tsx:16](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/(base)/settings/page.tsx#L16)

Strona ustawień profilu użytkownika
Umożliwia edycję danych osobowych i społecznościowych użytkownika

## Returns

`Element`

Strona ustawień



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / (screens)/layout

# (screens)/layout

## Functions

- [default](functions/default.md)



[**account_manager**](../../../README.md)

***

[account_manager](../../../modules.md) / [(screens)/layout](../README.md) / default

# Function: default()

> **default**(`props`): `Element`

Defined in: [(screens)/layout.tsx:11](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/(screens)/layout.tsx#L11)

Layout z providerem socket.io

## Parameters

### props

obiekt właściwości komponentu

#### children

`ReactNode`

elementy potomne renderowane wewnątrz providera

## Returns

`Element`

Layout



[**account_manager**](../README.md)

***

[account_manager](../modules.md) / socket

# socket

## Functions

- [SocketProvider](functions/SocketProvider.md)
- [useSocket](functions/useSocket.md)



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [socket](../README.md) / SocketProvider

# Function: SocketProvider()

> **SocketProvider**(`children`): `Element`

Defined in: [socket.tsx:21](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/socket.tsx#L21)

Provider zarządzający połączeniem socket.io i udostępniający je komponentom potomnym

## Parameters

### children

elementy potomne, które mogą korzystać z kontekstu socket

#### children

`ReactNode`

## Returns

`Element`



[**account_manager**](../../README.md)

***

[account_manager](../../modules.md) / [socket](../README.md) / useSocket

# Function: useSocket()

> **useSocket**(): `any`

Defined in: [socket.tsx:67](https://github.com/DawLip/programowanie-zespolowe/blob/7db6c4f7e8feac59e458adcc08c8cc70f3a35b0d/website/app/socket.tsx#L67)

Hook zwracający kontekst socket.io

## Returns

`any`

Obiekt z właściwościami socket oraz isConnected

## Throws

Błąd jeśli hook jest używany poza kontekstem <SocketProvider>



