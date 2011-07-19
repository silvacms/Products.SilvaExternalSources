# Copyright (c) 2002-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

# Zope
from App.class_init import InitializeClass
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from OFS.Folder import Folder
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.Formulator.Form import ZMIForm
from Products.SilvaExternalSources.interfaces import ICodeSource
from Products.SilvaExternalSources.interfaces import ICodeSourceService
from Products.SilvaExternalSources.ExternalSource import EditableExternalSource
from Products.Silva.SilvaPermissions import ViewManagementScreens, \
    AccessContentsInformation
from Products.Silva.helpers import add_and_edit

from five import grok
from silva.core.interfaces.content import IVersion
from silva.core.services.base import ZMIObject
from silva.core import conf as silvaconf
from zope.component import getUtility


class CodeSource(EditableExternalSource, Folder, ZMIObject):
    grok.implements(ICodeSource)

    meta_type = "Silva Code Source"
    security = ClassSecurityInfo()

    # ZMI Tabs
    manage_options = (
        {'label':'Edit', 'action':'editCodeSource'},
        ) + Folder.manage_options

    security.declareProtected(ViewManagementScreens, 'editCodeSource')
    editCodeSource = PageTemplateFile(
        'www/codeSourceEdit', globals(),  __name__='editCodeSource')

    # register icon and factories
    silvaconf.icon('www/codesource.png')
    silvaconf.factory('manage_addCodeSourceForm')
    silvaconf.factory('manage_addCodeSource')

    _data_encoding = 'UTF-8'
    _fs_location = None

    def __init__(self, id, script_id=None, fs_location=None):
        super(CodeSource, self).__init__(id)
        self._script_id = script_id
        self._fs_location = fs_location

    def test_source(self):
        # return a list of problems or None
        errors = []
        # in real life the parent of the form is the document. We try
        # to do the same here.
        root = self.get_root()
        if root.get_default():
            root = root.get_default()
        if self.parameters is not None:
            try:
                aq_base(self.parameters).__of__(root).test_form()
            except ValueError as error:
                errors.extend(error.args)
        if not self._script_id:
            errors.append(u'Missing required renderer id.')
        elif self._script_id not in self.objectIds():
            errors.append(u'Missing renderer %s. Please a script or template with this id.' % self._script_id)
        if errors:
            return errors
        return None

    # ACCESSORS
    security.declareProtected(AccessContentsInformation, 'script_id')
    def script_id(self):
        return self._script_id

    security.declareProtected(AccessContentsInformation, 'get_fs_location')
    def get_fs_location(self):
        return self._fs_location

    security.declareProtected(AccessContentsInformation, 'to_html')
    def to_html(self, content, request, **parameters):
        """Render HTML for code source
        """
        try:
            script = self[self._script_id]
        except KeyError:
            return None
        parameters['version'] = None
        parameters['model'] = content.get_content()
        if IVersion.providedBy(content):
            parameters['version'] = content
        result = script(**parameters)
        if isinstance(result,  unicode):
            return result
        return unicode(result, self.get_data_encoding(), 'replace')

    # MANAGERS

    security.declareProtected(ViewManagementScreens, 'manage_editCodeSource')
    def manage_editCodeSource(
        self, title, script_id, data_encoding, description=None,
        cacheable=None, previewable=None, update_source=None):
        """ Edit CodeSource object
        """
        if update_source and self.get_fs_location():
            service = getUtility(ICodeSourceService)
            installable = service.get_installable_source(
                location=self.get_fs_location())
            if installable is not None:
                installable.update(self)
                return self.editCodeSource(
                    manage_tabs_message='Source updated from the filesystem')
            return self.editCodeSource(
                manage_tabs_message='Could find the associated definition on the filesystem')

        msg = u''

        if data_encoding and data_encoding != self._data_encoding:
            try:
                unicode('abcd', data_encoding, 'replace')
            except LookupError:
                # unknown encoding, return error message
                msg += "Unknown encoding %s, not changed! " % data_encoding
                return self.editCodeSource(manage_tabs_message=msg)
            self.set_data_encoding(data_encoding)
            msg += u'Data encoding changed. '

        title = unicode(title, self.management_page_charset)

        if title and title != self.title:
            self.title = title
            msg += "Title changed. "

        if script_id and script_id != self._script_id:
            self._script_id = script_id
            msg += "Script id changed. "

        # Assume description is in the encoding as specified
        # by "management_page_charset". Store it in unicode.
        description = unicode(description, self.management_page_charset)

        if description != self._description:
            self.set_description(description)
            msg += "Description changed. "

        if not (not not cacheable) is (not not self._is_cacheable):
            self.set_cacheable(cacheable)
            msg += "Cacheability setting changed. "

        if not (not not previewable) is (not not self.is_previewable()):
            self.set_previewable(previewable)
            msg += "Previewable setting changed. "

        return self.editCodeSource(manage_tabs_message=msg)

InitializeClass(CodeSource)


manage_addCodeSourceForm = PageTemplateFile(
    "www/codeSourceAdd", globals(),
    __name__='manage_addCodeSourceForm')


def manage_addCodeSource(
    context, id, title, script_id=None, fs_location=None,REQUEST=None):
    """Add a CodeSource object
    """
    cs = CodeSource(id, script_id, fs_location)
    title = unicode(title, cs.management_page_charset)
    cs.title = title
    context._setObject(id, cs)
    cs = context._getOb(id)
    cs.set_form(ZMIForm('form', 'Parameters form', unicode_mode=1))

    add_and_edit(context, id, REQUEST, screen='editCodeSource')
    return ''
