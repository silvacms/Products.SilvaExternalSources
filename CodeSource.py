# Copyright (c) 2002-2007 Infrae. All rights reserved.
# See also LICENSE.txt
# $Revision: 1.19 $
from interfaces import IExternalSource
from ExternalSource import ExternalSource
from zope.interface import implements
# Zope
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
from Products.Formulator.Form import ZMIForm
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
# Silva
from Products.Silva.SilvaPermissions import ViewManagementScreens, AccessContentsInformation
from Products.Silva.helpers import add_and_edit
from Products.Silva.i18n import translate as _

class CodeSource(ExternalSource, Folder):

    implements(IExternalSource)
    
    meta_type = "Silva Code Source"

    security = ClassSecurityInfo()

    # UTF as UI is in UTF-8
    _data_encoding = 'UTF-8'
        
    # ZMI Tabs
    manage_options = (
        {'label':'Edit', 'action':'editCodeSource'},
        ) + Folder.manage_options

    security.declareProtected(ViewManagementScreens, 'editCodeSource')
    editCodeSource = PageTemplateFile(
        'www/codeSourceEdit', globals(),  __name__='editCodeSource')

    def __init__(self, id, script_id=None):
        self.id = id
        self._script_id = script_id

    # ACCESSORS

    security.declareProtected(AccessContentsInformation, 'script_id')
    def script_id(self):
        return self._script_id

    security.declareProtected(AccessContentsInformation, 'to_html')
    def to_html(self, REQUEST, **kw):
        """ render HTML for code source
        """
        try:
            script = self[self._script_id]
        except KeyError:
            return None
        self._deserialize(kw)
        result = script(**kw)
        if type(result) is unicode:
            return result
        return unicode(result, self.data_encoding(), 'replace')
    
    def _deserialize(self, kw):
        fields = self.form().get_fields()
        for field in fields:
            kw[field.id] = self._cast_value(kw.get(field.id, None), field.meta_type)
        return kw

    def _cast_value(self, value, field_type):
        if field_type == 'CheckBoxField':
            if value == '1':
                return True
            return False
        if field_type == 'IntegerField':
            return int(value)
        #XXX More field types? Dates? Selects?
        return value

    # MANAGERS

    security.declareProtected(ViewManagementScreens, 'manage_editCodeSource')
    def manage_editCodeSource(
        self, title, script_id, data_encoding, description=None, cacheable=None):
        """ Edit CodeSource object
        """
        msg = u''

        if data_encoding and data_encoding != self._data_encoding:
            try:
                unicode('abcd', data_encoding, 'replace')
            except LookupError:
                # unknown encoding, return error message
                m = _(
                    "Unknown encoding ${enc}, not changed! ",
                    mapping={"enc":charset})
                msg += sm #"Unknown encoding %s, not changed!. " % data_encoding
                return self.editCodeSource(manage_tabs_message=m)
            self.set_data_encoding(data_encoding)
            msg += 'Data encoding changed. '

        title = unicode(title, self.management_page_charset)

        if title and title != self.title:
            self.title = title
            m = _("Title changed. ")
            msg += m #'Title changed. '

        if script_id and script_id != self._script_id:
            self._script_id = script_id
            m = _("Script id changed. ")
            msg += m #'Script id changed. '

        # Assume description is in the encoding as specified 
        # by "management_page_charset". Store it in unicode.
        description = unicode(
            description, self.management_page_charset)

        if description != self._description:
            self.set_description(description)
            m = _("Description changed. ")
            msg += m #'Description changed. '

        if not (not not cacheable) is (not not self._is_cacheable):
            self.set_is_cacheable(cacheable)
            m = _("Cacheability setting changed. ")
            msg += m #'Cacheability setting changed. '

        try:
            script = self[script_id]
        except KeyError:            
            m = _("<b>Warning</b>: ")
            msg += m #'<b>Warning</b>: '
            if not script_id:
                m = _('no script id specified! ')
            else:
                m = _(
                    'This code source does not contain an callable object with\
                    id "${id}"! ',
                    mapping={'id': script_id})
            msg += m
        return self.editCodeSource(manage_tabs_message=msg)

InitializeClass(CodeSource)

addCodeSource = PageTemplateFile(
    "www/codeSourceAdd", globals(), __name__='addCodeSource')

def manage_addCodeSource(context, id, title, script_id=None, REQUEST=None):
    """Add a CodeSource object
    """
    cs = CodeSource(id, script_id)
    title = unicode(title, cs.management_page_charset)
    cs.title = title
    context._setObject(id, cs)
    cs = context._getOb(id)
    cs.set_form(ZMIForm('form', 'Parameters form', unicode_mode=1))
    
    add_and_edit(context, id, REQUEST, screen='editCodeSource')
    return ''
