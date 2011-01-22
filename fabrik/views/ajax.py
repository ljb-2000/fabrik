#!/usr/bin/env python
# standard module documentation:
"""
views/ajax.py
This file contains the methods that respond to AJAX calls from our pages.
i.e. all those under $host/apps/fabrik/ajax/
All those that involve writing require JSON 'hash' structures.
"""

## ----- imports from the local python distribution --- ##
# generic python imports
import os

# used for dumping errors if things go horribly wrong.
# also used for serialiaztion of objects
import simplejson
from fnmatch import fnmatch
from operator import itemgetter

## -------- imported Django modules and methods ---------- ##
from django.http import HttpResponse
from django.shortcuts import render_to_response


# bring in our custom forms
from fabrik.forms import *

# local 'utility; functions
from fabrik.utils import *

# configuration fils for common vars:
from fabrik.config import *

# separate webapi class in ${APPDIR}/cobblerweb.py
from fabrik.cobblerweb import CobblerWebApi

# cobbler utils for passthru auth etc
import cobbler.utils as cobblerutils

# okay, this might not be the best option... as if cobblerd is restarted without httpd also restarting
# the handle becomes stale.
# currently this uses a generic user/password. ideally we want it to prompt and cache.
global apihandle
apihandle = CobblerWebApi()
# these two methods come directly from cobbler_web
# will need munging a little
## - Ajaxy callback functions - ##

def resolve_name (request, hostname):
    """
    calls resolve_host from the utils module
    """
    results = resolve_host(hostname)
    return HttpResponse(results)

def get_layout (request, layoutname):
    """
    calls getlayout from utils to get layout file content
    """
    results = getlayout(layoutname)
    return HttpResponse(results)

# delete, rename and convert to profile....

def del_system(request):
    """
    used to delete system record via javascript callback
    """
    systemname = simplejson.loads(request.raw_post_data)['systemname']
    if apihandle.deleteSystem(systemname):
        return HttpResponse("Success", mimetype="text/javascript")
    else:
        return HttpResponse("Failure", mimetype="text/javascript")

def rename_system(request):
    """
    AJAXy callback for renaming systems
    """
    # check_auth(request)
    data = simplejson.loads(request.raw_post_data)
    
    result = apihandle.renameSystem(data['systemname'], data['newname'])

    if result == True:
        return HttpResponse('system renamed')
    else:
        return HttpResponse('Failed to rename system')

def sys_to_profile(request):
    """
    converts a system record to a profile (deletes interfaces etc)
    Currently this essentially copies ksmeta, distro etc
    The new profile becomes a child of the original system's profile.
    Anything else becomes a complex procedure.
    This expects JSON data: { 'systemname' : name, 'profilename': name }
    """
    data = simplejson.loads(request.raw_post_data)

    res =  apihandle.systemToProfile(data['profilename'], data['systemname'])
    if res == True:
        return HttpResponse('profile %s created from system %s' %(data['profilename'], data['systemname']) )
    else:
        return HttpResponse(res)

def get_profile_layout(request, profilename):
    """
    Parse ksmeta for disk info as above
    """
    p = apihandle.getProfile(profilename)
    if p != '~':
        disksnippet = p['ks_meta'].get('disksnippet', None)
        customlayout = p['ks_meta'].get('customlayout', None)
        if disksnippet is not None:
            return HttpResponse(simplejson.dumps({ 'Type' : 'disksnippet', 'Data' : disksnippet}), mimetype='application/javascript')
        elif DiskLayout is not None:
            layout = DiskLayout.replace('|', '\n')
            return HttpResponse(simplejson.dumps({'Type' : 'customlayout', 'Data' : layout}), mimetype='application/javascript')
        else:
            return HttpResponse(simplejson.dumps({'Type' : 'None', 'Data' : 'None'}), mimetype='application/javascript')
    
def list_systems(request):
    """
    fetches list of systems as JSON
    """
    res = []
    syslist = apihandle.getSystemNames()

    for x in syslist:
        res.append({ 'val' : x, 'name' : x })
    data = simplejson.dumps(res)
    return HttpResponse(data, mimetype='application/javascript')

def get_sysip(sysrecord):
    res = []
    for iface, data in sysrecord['interfaces'].iteritems():
        res.append('%s (%s)' %( data['ip_address'], iface ))
    return ','.join(res)
    

def list_profiles(request):
    """
    fetches list of profiles as JSON
    """
    res = []
    proflist = apihandle.getProfileNames()

    for x in proflist:
        res.append({ 'val' : x, 'name' : x })
    data = simplejson.dumps(res)
    return HttpResponse(data, mimetype='application/javascript')

def list_layouts(request, topdir = '/var/lib/cobbler/snippets/disklayouts'):
    """
    returns list of existing disk layouts (custom & core) as JSON
    """
    res = []
    for base, dirs, files in os.walk(topdir):
        lpath = re.sub(r'%s/?' % topdir, '', base)
        for f in files:
               res.append({'name' : f, 'val' : os.path.join(lpath, f) })
    data = simplejson.dumps(sorted(res, key=itemgetter('name')))
    return HttpResponse(data, mimetype = 'application/javascript')

def dump_systems(request):
    results = allsystems()
    return HttpResponse(simplejson.dumps(results), mimetype="text/javascript")

def get_system(request,systemname):
    results = apihandle.systemDetails(systemname)
    return HttpResponse(simplejson.dumps(results), mimetype="text/javascript")

## ---------- Save a disk layout ------------------ ##
def save_layout(request):
    """
    takes the JSON data posted from jQuery and tries to save it :)
    """
    data = simplejson.loads(request.raw_post_data)
    result = savelayout(data)
    if result == True:
        return HttpResponse('Layout saved')
    else:
        return HttpResponse(result)


# deprecated but worth keeping for a while anyway

def autocomplete_systems(request):
    def iter_results(results):
        if results:
            for r in results:
                yield '%s\n' % r

    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')

    term = request.GET.get('term')
    syslist = [ x for x in apihandle.getSystemNames() if fnmatch(x, '*%s*' % term) ]

    return HttpResponse(simplejson.dumps(syslist), mimetype='text/javascript')


def autocomplete_profiles(request):
    def iter_results(results):
        if results:
            for r in results:
                yield '%s\n' % r

    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')

    term = request.GET.get('term')
    syslist = [ x for x in apihandle.getProfileNames() if fnmatch(x, '*%s*' % term) ]

    return HttpResponse(simplejson.dumps(syslist), mimetype='text/javascript')
