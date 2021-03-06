# BMT Blog
DBMS Final Project

## Project Description
Please refer to [wiki][description] for project description.

## Project Design
Please refer to [wiki][design] for project design.

## Quickstart
### Virtual Environment
Please make sure that you are using Python 3 and `venv` package is installed. 
If you are using Ubuntu Linux system, you can install it as follows:
```
$ sudo apt-get install python3-venv
```
### Local Test
```
$ git clone https://github.com/mxyaiiao/cs5200_fall2018_bmt.git
$ cd cs5200_fall2018_bmt
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirement.txt
$ python manage.py runserver --host 0.0.0.0
```
### Visit
Navigate to http://localhost:5000/ . 
The initialization has already been dumped into SQLite. 
Please refer to [wiki][test] for detailed testing steps.

## Pre-loaded User Privilege and Credentials
* Admin: Administrator. admin/admin
* Moderator: alice/alice
* Monitor: bob/bob
* Noticer: charlie/charlie
* Basic User: dan/dan, ed/ed, frank/frank, greg/greg, han/han, ivan/ivan

## Useful Links
### Technology Stack
* https://github.com/pandao/editor.md
* http://flask.pocoo.org/
* https://en.gravatar.com/
* https://www.heroku.com/
* https://www.sqlite.org/
### YouTube Link
* https://youtu.be/NNaGNW9-EH0

[description]: https://github.com/mxyaiiao/cs5200_fall2018_bmt/wiki/Project
[design]: https://github.com/mxyaiiao/cs5200_fall2018_bmt/wiki/Design
[test]: https://github.com/mxyaiiao/cs5200_fall2018_bmt/wiki/Testing
