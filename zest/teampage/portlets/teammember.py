from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from zest.teampage import ZestTeamPageMessageFactory as _


class ITeamMemberPortlet(IPortletDataProvider):

    pass


class Assignment(base.Assignment):
    implements(ITeamMemberPortlet)

    @property
    def title(self):
        return _(u"Team Member Introduction")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('teammember.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()
        self.portal_url = portal_state.portal_url()

    @memoize
    def _data(self):
        return []


class AddForm(base.NullAddForm):
    form_fields = form.Fields(ITeamMemberPortlet)
    label = _(u"Add Review Portlet")
    description = _(
        u"This portlet displays a Teammember introduction from the site")

    def create(self):
        return Assignment()
