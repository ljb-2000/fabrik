#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Fabrik - a custom django/javascript frontend to cobbler
#
# Copyright 2009-2012 Stuart Sears
#
# This file is part of fabrik
#
# fabrik is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# fabrik is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with fabrik. If not, see http://www.gnu.org/licenses/.
# top-level docstrings

__doc__ = """
top-level module for django views.
the django views were getting complicated
so I've separated the AJAX calls from the std pages as an experiment

"""

__all__ = [ 'std', 'ajax', 'auth' ]
