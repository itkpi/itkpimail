# itkpimail

[![Build Status](https://travis-ci.org/itkpi/itkpimail.svg)](https://travis-ci.org/itkpi/itkpimail)

## Setup development environment via Vagga (Recommended)
#### Requirements
 - Linux


 1. Setup vagga http://vagga.readthedocs.org/
 2. Clone this repo
 3. vagga setup
 4. vagga run

## Setup development environment via VirtualEnv
#### Requirements

 - Python 3

 1. Clone this repo
 2. virtualenv venv && . venv/bin/activate
 3. pip install -r requirements.txt
 4. python manage.py migrate
 5. python manage.py runserver
