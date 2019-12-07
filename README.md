# bluetooth-localization
An indoor positioning system based on Bluetooth Low Energy, that can locate multiple devices.

## How to Use - run following commands
1. docker-compose up -d //runs the container in detach mode
2. docker-compose exec web python manage.py makemigrations
3. docker-compose exec web python manage.py createsuperuser
  3.1. username: admin
  3.2. email: 'leave it blank and press enter'
  3.3. password: admin
  3.4. type 'y' and press enter if django asks something about password.
4. docker-compose exec web python manage.py migrate
5. docker-compose down //kills the container
