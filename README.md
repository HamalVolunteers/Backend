# Backend
Python backend for the application

# current tests sidclaimer
The current tests (i.e CI) reset the DB completly (to not overcrowd it).
They should be changed to reset a safer envieroment later.
But it will be dependend on the chosen DB/xRM.

# Backend flow
1) Recieve an HTTP request from flutter frontend.
2) Breakdown the request by the given structure.
3) parse the request to the right function.
4) Get the information from the DB.
5) Return the JSON to flutter as an HTTP answer.

# requests & answers
First, any Error will result in:
`
{
  "status": "error"
  "data": <doesnt matter>
}
`
## get user information by id
### message structure
`
{
  "action":"getUserById"
  "payload":{"id":<user_id>}
}
`
expects <user_id> to be an integer
### return structure
`
{
  "status":"ok"
  "data": {
            "id":<user_id>
            "name":"user_name"
            "filter":<list_of_filters>
          }
}
`
list_of filters is a lists of strings
If the user doesn't exsists, it returns {}
## get user filters by id
### message structure
`
{
  "action":"getFiltersByUserId"
  "payload":{"id":<user_id>}
}
`
expects <user_id> to be an integer
### return structure
`
{
  "status":"ok"
  "data": {
            "filters":<list_of_filters>
          }
}
`
list_of filters is a lists of strings
If the user doesn't exsists, it returns an empty list
## add user filter by id
### message structure
`
{
  "action":"addFilterById"
  "payload":{"id":<user_id>,"filter":<filter>}
}
`
filter is a string
### return structure
`
{
  "status":"ok"
  "data": <res>
}
`
res can be:
1) True- if succeded
2) False- if user (user_id) already has the filter

If the user doesn't exists, it returns an error (as stated above)

## remove user filter by id
### message structure
`
{
  "action":"removeFilterById"
  "payload":{"id":<user_id>,"filter":<filter>}
}
`
filter is a string
### return structure
`
{
  "status":"ok"
  "data": <res>
}
`
res can be:
1) True- if succeded
2) False- if user didn't exist/user doesn't have the filter

## add user
### message structure
`
{
  "action":"addUser"
  "payload":
  {"id":<user_id>
    "name": <user_name>
    "filters":<list_of_filters>}
}
`
list_of filters is a lists of strings
### return structure
`
{
  "status":"ok"
  "data": <res>
}
`
res can be:
1) True- if succeded
2) False- if user (user_id) already exsits
## get events by filter
### message structure
`
{
  "action":"getEventByFilters"
  "payload":{"filters":<list_of_filters>}
}
`
list_of filters is a lists of strings
### return structure
`
{
  "status":"ok"
  "data": <list_of_events>
}
`
#### events are sorted
- The higher an event, the more filters he has in common.
- returns only events with at least one matching filter.
## sign user to an event
### message structure
`
{
  "action":"signUserToEvent"
  "payload":{"id":<user_id>, "eventId": <event_id>}
}
`
expects <user_id> and <event_id> to be integers
### return structure
`
{
  "status":"ok"
  "data": <res>
}
`
res can be:
1) True- if suceeded
2) False- user already signed to this event/ no more space

If the user doesn't exists, it returns an error (as stated above)

## remove user from an event
### message structure
`
{
  "action":"removeUserFromEvent"
  "payload":{"id":<user_id>, "eventId": <event_id>}
}
`
expects <user_id> and <event_id> to be integers
### return structure
`
{
  "status":"ok"
  "data": <res>
}
`
res can be:
1) True- if suceeded
2) False- user not signed to this event/ event doesnt exists

## add event
### message structure
`
{
  "action":"addEvent"
  "payload":{
            "eventId": <event_id>
            "name": <name>
            "capacity":<capacity>
            "info":<info>
            "filters":<list_of_filters>
            }
}
`
expects <event_id> and <capacity> to be integers
expects <name> and <info> to be strings
list_of filters is a lists of strings
### return structure
`
{
  "status":"ok"
  "data": <res>
}
`
res can be:
1) True- if suceeded
2) False- event already exists
## get event by id
### message structure
`
{
  "action":"getEventById"
  "payload":{"eventId":<event_id>}
}
`
expects <event_id> to be an integer
### return structure
`
{
  "status":"ok"
  "data": <res>
}
`
res can be:
1) True- if suceeded
2) False- event doesnt exists
