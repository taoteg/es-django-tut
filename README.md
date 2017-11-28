# ElasticSearch Integration with Django (1.9.3) Tutorial

## Setup

Using this tutorial and sbsequent references as baseline:

- https://qbox.io/blog/how-to-elasticsearch-python-django-part1
- https://github.com/CommandrAvander/elasticsearch-django-tutorial
- https://docs.djangoproject.com/en/1.11/
- https://www.elastic.co/guide/index.html
- https://github.com/elastic/elasticsearch
- https://www.codingforentrepreneurs.com/blog/django-virtualenv-python-gitignore-file/
- https://pixabay.com/en/blog/posts/django-search-with-elasticsearch-47/

Uses a custom project template that is no loger available, so recreating manually to match tutorial structure.

*Target Structure*

```
.
|_____wsgi.pyc
|_____static
|_____|_____bootstrap.min.css
|_____|_____jquery-ui.min.js
|_____|_____jquery-ui.min.css
|_____|_____dashboard.css
|_____|_____jquery-ui.css
|_____|_____jquery.min.js
|_____|_____bootstrap.min.js
|_____|_____bootstrap-theme.min.css
|_____urls.pyc
|_____templates
|_____|_____index.html
|_____|_____base.html
|_____|_____student-details.html
|_____manage.py
|_____urls.py
|_____conf
|_____|_______init__.py
|_____|_______pycache__
|_____|_____|_____base.cpython-36.pyc
|_____|_____|_______init__.cpython-36.pyc
|_____|_____base.pyc
|_____|_______init__.pyc
|_____|_____base.py
|_____apps
|_____|_____core
|_____|_____|_____migrations
|_____|_____|_____|_______init__.pyc
|_____|_____|_____|_____0001_initial.py
|_____|_____|_____|_____0001_initial.pyc
|_____|_____|_____models.pyc
|_____|_____|_____models.py
|_____|_____|_____management
|_____|_____|_____|_______init__.pyc
|_____|_____|_____|_____commands
|_____|_____|_____|_____|_____push-to-index.py
|_____|_____|_____|_____|_____dummy-data.pyc
|_____|_____|_____|_____|_____dummy-data.py
|_____|_____|_____|_____|_______init__.pyc
|_____|_____|_____|_____|_____push-to-index.pyc
|_____|_____|_____views.pyc
|_____|_____|_____apps.py
|_____|_____|_____admin.py
|_____|_____|_____urls.pyc
|_____|_____|_______init__.pyc
|_____|_____|_____urls.py
|_____|_____|_____admin.pyc
|_____|_____|_____views.py
|_____|_______init__.pyc
|_____wsgi.py
```

*Starting Structure*

```
.
|_____project
|_____|_______init__.py
|_____|_____settings.py
|_____|_____urls.py
|_____|_____wsgi.py
|_____manage.py
```
