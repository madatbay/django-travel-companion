# Django Travel Companion
Travelling Companion App - a system that will help you and your family to manage their travel itineraries. An A-Z solution that helps keep track of your budget, schedule, the cities that you will visit, flights between the cities and hotel bookings that you will make (can be multiple per city).

[![Django Test](https://github.com/madatbay/django-travel-companion/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/madatbay/django-travel-companion/actions/workflows/test.yml)

## Testing
Both models and view tested with built-in testing module. Test reports can be seen with coverage:
```
coverage run manage.py test
coverage html|report
```

## Local Deployment
Application was built on `Docker` images under the hood of `Docker-compose`. So, just run:

```
docker-compose up|stop|restart
```

Note static files are served with "--insecure" flag, yet it's not intended for absolute production use. Since our application is not deploye totally we have to serve them locally instead of NGINX server

Application has only 2 services:
- Web application
- Database - Postgresql


## Endpoints 
All endpoint added as a list in a corresponding app group

### User
`url="register/", name="register"` - Create a new user

`url="login/", name="login"),` - Create a login session

`url="logout/", name="logout"),` - Remove the logged in session

`url="profile/", name="profile"),` - Logged in user profile get view

`url="edit-profile/", name="edit_profile")` - Logged in user profile update view

### Travel

`url="", name="index"` - Home page or dashboard get view

`url="trips/all/", name="trip_all"` - All trips list view

`url="trips/create/", name="trip_create"` - Trip create view

`url="trips/<int:id>/", name="trip_detail"` - Single trip detail view

`url="trips/<int:id>/edit/", name="trip_update"` - Single trip update view

`url="trips/<int:id>/add-tripmates/", name="trip_mate_add"` - Add trip mates to a sing trip post view

`url="trips/<int:id>/add-destination/", name="trip_destination_add"` - Add or remov destinations to the trip

`url="trips/<int:id>/budget/", name="budget_detail"` - Budget detail view of the trip
`url="trips/<int:id>/flights/", name="flight_list"` - Flight list view of the trip

`url="flight/delete/<int:id>/", name="flight_delete"` - Single flight destroy view

`url="flight/add/<int:id>/", name="flight_add_or_update"` - Flight create or update view

`url="budget/delete/<int:id>/", name="budget_item_delete"` - Budget item destroy view

`url="budget/add/<int:id>/", name="budget_item_add_or_update"` - Budget item create or update view

`url="destinations/all/", name="destination_all"` - Destinations list view

`url="destinations/create/", name="destination_create"` - Destination create view
`url="destinations/<int:id>/update/", name="destination_update"` - Destination update view

`url="destinations/<int:des_id>/hotels/<int:hotel_id>/delete/", name="destination_hotel_delete",`- Hotel destroy view

`url="destinations/<int:id>/hotels/add/", name="destination_hotel_add_or_update"` - Hotel add or update view 