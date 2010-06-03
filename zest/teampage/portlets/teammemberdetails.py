# -*- coding: utf-8 -*-
#from zope import schema
#

from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zest.teampage import ZestTeamPageMessageFactory as _


class ITeamMemberDetailsPortlet(IPortletDataProvider):
    pass


class Assignment(base.Assignment):
    implements(ITeamMemberDetailsPortlet)

    @property
    def title(self):
        return _(u"Team Member Details")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('teammemberdetails.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()
        self.portal_url = portal_state.portal_url()

    @property
    def available(self):
        """ Only show te teammember details portlet if we view a team member
        """
        return (self.context.portal_type == "TeamMember")

    @memoize
    def _data(self):
        return []

    def getHobbies(self):
        """Return the hobbies of the team member."""
        hobbies = self.context.getHobbies()
        if hobbies:
            return ', '.join(self.context.getHobbies())
        else:
            return None

    def get_zest_blog_items(self, author):
        """This return an aggregated list of blog items from both external
        blogs and the Zest blog.
        """
        blogbrains = self.context.portal_catalog.searchResults(
           Creator=author, portal_type='Blog Entry',
           sort_on='modified', sort_order='reverse')
        if not blogbrains:
            return []

        zestblog = blogbrains[0].getObject()
        zestitem = dict(title=zestblog.Title(),
                        url=zestblog.absolute_url())
        zestitem = [zestitem]

        return zestitem


class AddForm(base.NullAddForm):
    form_fields = form.Fields(ITeamMemberDetailsPortlet)
    label = _(u"Add Review Portlet")
    description = _(u"This portlet displays Teammember Details")

    def create(self):
        return Assignment()
