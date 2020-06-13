# bluetooth-localization
An indoor positioning system based on Bluetooth Low Energy, that can locate multiple devices.

## How to Use - run following commands
1. docker-compose up -d  --  runs the container in detach mode
2. docker-compose exec web python manage.py makemigrations
3. docker-compose exec web python manage.py migrate
4. docker-compose exec web python manage.py createsuperuser
   - username: admin
   - email: 'leave it blank and press enter'
   - password: admin
   - type 'y' and press enter if django asks something about password.
5. docker-compose down  --  kills the container
