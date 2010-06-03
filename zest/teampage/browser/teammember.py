from DateTime import DateTime
import random

from plone.app.layout.viewlets.common import ViewletBase
from zope.interface import implements

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFPlone.utils import getToolByName

from zest.teampage.interfaces import ITeamMemberView

import feedparser


class BaseView(BrowserView):
    """Base Browser View class which provides frequently used methods."""

    def get_image_tag(self, field, **kwargs):
        """Generate image for tag for ``field`` using api of the ImageField.
        """
        return self.context.getField(field).tag(self.context, **kwargs)


class TeamMemberView(BaseView):
    """View for a TeamMember.
    """
    implements(ITeamMemberView)

    def getFullName(self):
        """Return the full name of the team member."""
        return ' '.join([self.context.Title(),
                         self.context.getSurname()])

    def getAge(self):
        """Return the age of the team member."""
        birthdate = self.context.getBirthdate()
        if birthdate is None:
            return None
        today = DateTime()
        age = today.year() - birthdate.year()
        # Apply correction when before birthday.
        if (today.month() < birthdate.month() or
            (today.month() == birthdate.month() and
            today.day() < birthdate.day())):
            age = age - 1
        return age

    def has_portrait_hover(self):
        """ return True if this member has a hover portrait, False otherwise"""

        return hasattr(self.context, 'portrait_hover') and \
        self.context.portrait_hover.getSize() > 0

    def getHobbies(self):
        """Return the hobbies of the team member."""
        hobbies = self.context.getHobbies()
        if hobbies:
            return ', '.join(self.context.getHobbies())
        else:
            return None

    def get_random_teammember(self):
        """Return the url of the introduction page of a random team member."""
        catalog = getToolByName(self, 'portal_catalog')
        brains = catalog.searchResults(
            portal_type='TeamMember',
            review_state='published')
        if brains:
            random.seed()
            brain = random.choice(brains)
            return '/'.join([brain.getURL(), 'teammember_introduction'])
        else:
            return ''

    def language(self):
        return self.context.restrictedTraverse(
            '@@plone_portal_state').language()

    def get_zest_blog_items(self, author):
        """This return an aggregated list of blog items from both external
        blogs and the Zest blog
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

    def get_blog_items(self, author):
        """ This return an aggregated list of blog items from both external
            blogs and the Zest blog
        """
        blogbrains = self.context.portal_catalog.searchResults(
            Creator=author, portal_type='Blog Entry',
            sort_on='created', sort_order='reverse', sort_limit=2)
        results = []
        if blogbrains:
            for brain in blogbrains:
                zestblog = brain.getObject()
                zestitem = dict(title=zestblog.Title(),
                                url=zestblog.absolute_url(),
                                date=zestblog.created())
                results.append(zestitem)

        teammember = self.context.portal_catalog.searchResults(
            id=author, portal_type='TeamMember')
        url = teammember[0].getObject().getExternal_blog()
        d = feedparser.parse(url)
        for item in d['items']:
            try:
                link = item.links[0]['href']
                itemdict = {
                    'title': item.title,
                    'url': link,
                }
                if hasattr(item, "updated"):
                    itemdict['date'] = DateTime(item.updated)
                else:
                    itemdict['date'] = ""
            except AttributeError:
                continue
            results.append(itemdict)
        return sorted(results, key=lambda k: k['date'], reverse=True)


class TeamMemberViewlet(ViewletBase):
    render = ViewPageTemplateFile('teammember_viewlet.pt')


class TeamMemberListing(BaseView):
    """View for the TeamMember folder listing.
    """

    def get_teammembers(self):
        """Return a list of dictionaries with the team members.
        """
        result = []
        folderfilter = {'portal_type': ['TeamMember', ]}

        for obj in self.context.listFolderContents(contentFilter=folderfilter):
            teammemberview = obj.restrictedTraverse('@@teammember_view')
            fullname = teammemberview.getFullName()
            hover_tag = teammemberview.get_image_tag('portrait_hover',
                                                      scale='portrait_hover')
            has_portrait_hover = teammemberview.has_portrait_hover()
            portrait_url = obj.absolute_url() + '/portrait_portrait_small'

            result.append({
                'url': obj.absolute_url(),
                'firstname': obj.Title(),
                'name': fullname,
                'function': obj.getFunction(),
                'freelance': obj.getFreelance(),
                'hover_tag': hover_tag,
                'has_portrait_hover': has_portrait_hover,
                'portrait_url': portrait_url,
                })

        return result

    def get_batched_teammembers(self, columns=4):
        if columns < 1:
            return []
        batched_results = []
        results = self.get_teammembers()
        while len(results) > columns:
            batched_results.append(results[:columns])
            results = results[columns:]
        batched_results.append(results)

        return batched_results
