# Copyright (c) 2002 Infrae. All rights reserved.
# See also LICENSE.txt
# $Revision: 1.2 $
from interfaces import IExternalSource
# Zope
import Acquisition
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo, ModuleSecurityInfo
# Silva
from Products.Silva.SilvaPermissions import ViewManagementScreens
# Interfaces
from Products.Silva.interfaces import IRoot
# Formulator
from Products.Formulator.Form import ZMIForm
from Products.Formulator.Errors import ValidationError, FormValidationError

icon="www/silvaexternalsource.png"

module_security = ModuleSecurityInfo(
    'Products.SilvaExternalSources.ExternalSource')

class _AvailableSources:
    """SINGLETON

    Helps getting a list of ExternalSources from context up.
    Stop at the "Silva Root".
    """

    def _list(self, context):
        """ Recurse through parents up. 
        
        Only list id's that can be reached from the context 
        through acquisition.
        """
        sources = {}
        while 1:
            objs = context.objectValues()
            for obj in objs:
                if IExternalSource.isImplementedBy(obj):
                    sources[obj.id] = 1
            if IRoot.isImplementedBy(context):
                # stop at Silva Root
                break
            context = context.aq_parent
        return sources.keys()

    def __call__(self, context): 
        return self._list(context)

module_security.declarePublic('availableSources')
availableSources = _AvailableSources()

class ExternalSource(Acquisition.Implicit):

    __implements__ = IExternalSource
    
    meta_type = "Silva External Source"

    security = ClassSecurityInfo()

    parameters = None # Cannot make it 'private'; the form won't work in the ZMI if it was.
    _data_encoding = 'ascii'
    _description = 'No description available'

    def __init__(self, id, title):
        self.id = id
        self.title = title

    # ACCESSORS

    def form(self):
        """ get to the parameters form
        """
        return self.parameters

    def to_html(self, REQUEST, **kw):
        """ Render the HTML for inclusion in the rendered Silva HTML.
        """
        return ''

    def to_xml(self, REQUEST, **kw):
        """ Render the XML for this source.
        """
        return '<source></source>'

    def is_cacheable(self, REQUEST, **kw):
        """ Specify the cacheability.
        """
        return 0

    def data_encoding(self):
        """ Specify the encoding of source's data.
        """
        return self._data_encoding

    def description(self):
        """ Specify the use of this source.
        """
        return self._description

    def index_html(self, REQUEST, RESPONSE):
        """ render HTML with default or other test values in ZMI for
        purposes of testing the ExternalSource.
        """
        form = self.form()

        try:
            kw = form.validate_all(REQUEST)
        except (FormValidationError, ValidationError), err:
            # If we cannot validate (e.g. due to required parameters), 
            # return a form.
            # FIXME: How to get some feedback in the rendered page? E.g.
            # in case of validation errors.
            return form.render(REQUEST=REQUEST)

        return self.to_html(REQUEST, **kw)

    # MODIFIERS

    security.declareProtected(ViewManagementScreens, 'set_form')
    def set_form(self, form):
        """ Set Formulator parameters form
        """
        self.parameters = form

    security.declareProtected(ViewManagementScreens, 'set_data_encoding')
    def set_data_encoding(self, encoding):
        """ set encoding of data
        """
        self._data_encoding = encoding

    security.declareProtected(ViewManagementScreens, 'set_description')
    def set_description(self, desc):
        """ set description of external source's use
        """
        self._description = desc

InitializeClass(ExternalSource)
