# REST API documentation

### [Go to README](README.md)

---
## Objects

- [Sessions](#sessions)
    + [Read](#readSession)
    + [Create](#createSession)
    + [Edit](#editSession)
    + [Delete](#deleteSession)
    

- [Users](#users)
    + [Read](#readUser)
    + [Create](#createUser)
    + [Edit](#editUser)
    + [Delete](#deleteUser)


---

## <span id="sessions">Sessions</span>

#### Prefix: `/api/sessions`
#### Example: `https://area-146.tk/api/sessions`


### Methods
> [Read session > GET](#readSession)\
> [Create session > POST](#createSession)\
> [Edit session > PUT](#editSession)\
> [Delete session > DELETE](#deleteSession)
---

### <span id="readSession" style="color: grey">GET:</span> Read session
######URL arguments:

Not required:\
`id` - session's id (8 lowercase letters)\
`sku` - session's SKU


###### returns
```json
{
    "message": "Success",
    "errors": [],
    "sessions": [
        {
            "id": "session1_id",
            "title": "session1_title",
            "admins_ids": "1;2;3",
            "players_ids": "1;2;3;4;5"
        },
        {
            "id": "session2_id",
            "title": "session2_title",
            "admins_ids": "1;2;3",
            "players_ids": "1;2;3;4;5"
        }
    ]
}
```
---

### <span id="createSession" style="color: grey">POST:</span> Create session

######URL arguments:

Required:\
`title` - new session's title

###### returns
```json
{
    "message": "Success",
    "errors": [],
    "data": {
        "id": "new_session_id"
    }
}
```
---

### <span id="editSession" style="color: grey">PUT:</span> Edit session
######URL arguments:
Not Required:\
`title` - new session's title\
`adminsIds` - ids of admins\
`playersIds` - ids of players

###### returns
```json
{
    "message": "Success",
    "errors": []
}
```
---

### <span id="deleteSession" style="color: grey">DELETE:</span> Delete session
######URL arguments: -

###### returns
```json
{
    "message": "Success",
    "errors": []
}
```
---

## <span id="users">Users</span>

#### Prefix: `/api/users`
#### Example: `https://area-146.tk/api/users`


### Methods
> [Read user > GET](#readUser)\
> [Create user > POST](#createUser)\
> [Edit user > PUT](#editUser)\
> [Delete user > DELETE](#deleteUser)
---

### <span id="readUser" style="color: grey">GET:</span> Read user
######URL arguments:

Required:\
`id` - user's id (8 lowercase letters)\
`email` - user's email


###### returns
```json
{
    "message": "Success",
    "errors": [],
    "users": [
        {
            "id": "user1_id"
        },
        {
            "id": "user2_id"
        }
    ]
}
```
---

### <span id="createUser" style="color: grey">POST:</span> Create user

######URL arguments:

Required:\
`email` - new user's email
`password` - new user's password

###### returns
```json
{
    "message": "Success",
    "errors": [],
    "data": {
        "id": "new_user_id"
    }
}
```
---

### <span id="editUser" style="color: grey">PUT:</span> Edit user
######URL arguments:

Required:\
`id` - user's id (8 lowercase letters)\
`email` - user's email

Not Required:\
`title` - new session's title\
`adminsIds` - ids of admins\
`playersIds` - ids of players

###### returns
```json
{
    "message": "Success",
    "errors": []
}
```
---

### <span id="deleteUser" style="color: grey">DELETE:</span> Delete user
######URL arguments:

Required:\
`id` - user's id (8 lowercase letters)\
`email` - user's email

###### returns
```json
{
    "message": "Success",
    "errors": []
}
```
---