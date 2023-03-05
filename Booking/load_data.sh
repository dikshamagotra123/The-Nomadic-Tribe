#!/bin/bash
python manage.py loaddata fixtures/amentities.json 
python manage.py loaddata fixtures/adventures.json
python manage.py loaddata fixtures/hotels.json
