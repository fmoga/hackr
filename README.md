# Hackr Events

Hackr is a web application for managing hackathons written using [Django][1].

### Features

* Authentication using Google Account
* Manage events (hackathons)
* Projects can be proposed by users for a particular hackathon
* Users can show their interest in a project by joining them
* Each project has a comments section where a discussion can be developed
* Once the hackathon is over, the event creator can start the voting phase
* Users can make proposals for best hackathon contribution or vote existing ones
* Event creator can end the voting phase, making the results public

### Installation

#### Requirements

* `sudo apt-get install python-mysqldb python-pip`
* MySQL database named `hackr`
* Google application created via [Google APIs Console][2]. OAuth callback endpoint is `complete/google-profile/`. Add app tokens to settings.py.

#### Dependencies

    $ sudo pip install django 
    $ sudo pip install django-social-auth
    $ sudo pip install flup # if using FastCGI for deployment

### Notes

#### Modifying the model

In order to alter the database but keep current data, execute the following:

    $ python manage.py dumpdata events --format json > dump.json 
    $ python manage.py reset events 
    $ python manage.py loaddata dump.json
    
[1]: https://www.djangoproject.com/
[2]: https://code.google.com/apis/console/
