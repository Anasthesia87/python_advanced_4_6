from voluptuous import Schema, All, Length, PREVENT_EXTRA

user = Schema(
    {
        "id": int,
        "email": str,
        "first_name": str,
        "last_name": str,
        "avatar": str
    },
    extra=PREVENT_EXTRA,
    required=True,
)

response_list_users = Schema(
    {
        "page": int,
        "per_page": int,
        "total": int,
        "total_pages": int,
        "data": All([user], Length(min=7)),
        "support": {
            "url": str,
            "text": str
        }
    })


response_create_user = Schema(
    {
        "name": str,
        "job": str,
        "id": str,
        "createdAt": str
    })


response_update_user = Schema(
    {
        "name": str,
        "job": str,
        "updatedAt": str
    })

response_get_user = Schema(
    {
        "data": user,
        "support": {
            "url": str,
            "text": str
        }
    })