# Dumblestore

A prototype API for the infrastructure modernization of Albus Dumbledore's video store that uses outdated practices like magic. This API allows manipulating the movie catalog and users for the admin, and presenting the movie catalog to users

### [Click here for the demo](http://dumblestore.herokuapp.com/api)

## Endpoints:

- **REST api root** `/api/`: You can access browsable api that acts as a documentation with html content over browsers. Also serves as the root for JSON API access. No anonymous access.

- **Users** `/api/users/`: Shows User related data. Admin has all the CRUD functionality, users can only see their own info.
- **Movies** `/api/movies/`: Admin has all the CRUD functionality, users can only see the movie info. Can be sorted by id, title or genre

- **Token Authentication**: `/api-token-auth/` distributes API tokens. Supply email and password by a POST request to this endpoint to receive your token. Then use this token in your `Authorization` header prefixed by "Token " keyword. e.g (for Powershell)

```powershell
$params = @{
 "username"="albus@hogwarts.com";
 "password"="kendra1881";
}
$token = (irm -method POST -uri "http://dumblestore.herokuapp.com/api-token-auth/" -B $params).token
irm -method GET http://dumblestore.herokuapp.com/api/movies/ -H  @{Authorization="Token $token"}
```

- **Session Authentication**: `/api-auth/` Primarily for compatibility with browsers as they don't provide a nice way to use token based authentication. Use the "login" form on the top of the API pages while browsing. CSRF protection enabled, therefore use token authentication for cross origin API requests.
- **Django Admin**: `/admin` direct access to database tables accessible by superuser.

Superuser name: `albus@hogwarts.com`
Superuser password: `kendra1881`

Customer passwords are in format: `f"{first_name}42"`
email: `bbutt2@bloomberg.com` password: `Bryan42`
