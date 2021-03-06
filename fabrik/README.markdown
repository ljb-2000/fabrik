README
======

This directory contains the key python code for the fabrik web interface.

Key Python files
----------------

* urls.py
  - maps URL patterns to functions in views.py

* views/*.py
  - generates forms and other pages, rendering them using the given templates 

* forms.py
  - form definitions: fields, content, syntax-checking


* utils.py
  - custom utility code for reuse in views

* cobblerweb.py
  - an abstraction of some elements of the Cobbler XMLRPC API
	This includes methods to produce output in a form consumable by django
	form elements.

* config.py
  - configuration file, mainly key = value pairs
    used by most parts of the fabrik interface.

Templating
----------

* templatetags/
  - files defining new tags for use in django templates.
  see templatetags/README

* templates/
  - template files used by views.py to render content.
    see templates/README


