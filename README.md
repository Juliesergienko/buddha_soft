You will find all the code in the api app.
There are two main entities in the project: Client and Manager.
Client is OneToOne relation with User. For each Client User is created.

Clients can:

1. register - by /api/version_number/register/ POST {"first_name": "string", "last_name": "string",
                                                     "email": "unique_string", "passport": "unique_string"}
Response: {"client_id": int_or_None, "pin_code": "string_or_None", "message": "string_OK_or_error"}
2. log in - by /api/version_number/log_in/ POST {"pin_code": "string"}
Response: {"status_code": 200 or 401}
3. get balance - if authorised - by /api/version_number/profile/ GET
Response: {"balance": decimal_balance}
4. close account - if authorised - by /api/version_number/close_account/ PUT
Response: {"status_code": 200}

Managers are created from Django Admin page.

To create Manager:

0. Create Group 'Manager' if not exists yet
1. Create new User
2. Add him to the 'Manager' group

Managers can:
1. see list of pending accounts - if authorised - by /api/version_number/pending_accounts/ GET
Response: {"client_list": [{"id": int_client)id, "status": "string_client_status"}, {},]}
2. confirm new account - if authorised - by /api/version_number/approve/client_id/activate/ PUT
Response: {"status_code": 200 or 401}
3. confirm new account - if authorised - by /api/version_number/approve/client_id/activate/ PUT
Response: {"status_code": 200 or 401}

Backend implementation:

Code was written using TDD, you will find tests in api/tests folder: clients.py has all the tests for Client entity,
managers.py has tests according Manager entity.

Logics according to Client and Manager behavior is in the api/client.py and api/manager.py respectively.
Views from views.py used only to call functions from api/client.py and api/manager.py.
However, there is a function is_manager in api/views.py. It checks whether user is in Manager group.
For better readebility it is left in api/views.py.
