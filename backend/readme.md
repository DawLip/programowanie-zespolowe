/dashboard
- nie zgadza się z modelem i bazą danych
    File "/home/david/workspace/studies/account_manager/backend/app/routes/aside.py", line 17, in get_aside
        ((Room.user1_id == user_id) & (Room.user2_id == friend.id)) |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AttributeError: type object 'Room' has no attribute 'user1_id'

/aside
- zwracając użytkowników dodać id user
- zwracając grupy dodać id grupy
- nie zgadza się z modelem i bazą danych
    File "/home/david/workspace/studies/account_manager/backend/app/routes/dashboard.py", line 51, in get_dashboard
    'messageAuthor': msg.user.name,
    AttributeError: 'Messages' object has no attribute 'user'

(POST) /user/:id
- edytuje tylko name, surname i email

! Grupa musi mieć pole "destription"

(POST) /group/new
- nowy endpoint do tworzenia grupy
zwraca
{ groupId, status }