# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import io

from math import ceil
from tempfile import NamedTemporaryFile

import pytz

from lxml import etree
from lxml.builder import E
from werkzeug.utils import cached_property

from nereid.helpers import send_file, url_for


class SitemapIndex(object):
    """
    A collection of Sitemap objects

    To add a sitemap index to one of your objects do the following:

    class Product(ModelSQL, ModelView):
        __name__ = "product.product"

        @classmethod
        def sitemap_index(cls):
            index = SitemapIndex(
                cls, cls.search_domain
                )
            return index.render()

        @classmethod
        def sitemap(cls, page):
            sitemap_section = SitemapSection(
                cls, cls.search_domain, page
                )
            return sitemap_section.render()

        def get_absolute_url(self, **kwargs):
            "Return the full_path of the current object"
            return url_for('product.product.render',
                uri=self.uri, **kwargs)
    """
    #: Batch Size: The number of URLs per sitemap page
    batch_size = 1000

    def __init__(self, model, domain, priorities=[0.5],
            max_age=60 * 60 * 24):
        """
        A collection of SitemapSection objects which are automatically
        generated based on the

        :param collection: An iterable of tuples with the name of the model
                           and the domain. Example

        ...>>> product_obj = pool.get('product.product')
        ...>>> sitemap = Sitemap(
        ...        product_obj, [('displayed_on_eshop', '=', True)])
        """
        self.model = model
        self.domain = domain
        self.priorities = priorities
        self.max_age = max_age

    def render(self):
        with io.BytesIO() as tmp_file:
            data = '<?xml version="1.0" encoding="UTF-8"?>\n'
            data += '<sitemapindex '
            data += 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            method = '%s.sitemap' % self.model.__name__
            for page in range(1, self.page_count + 1):
                for priority in self.priorities:
                    data += ('<sitemap><loc>%s</loc></sitemap>\n'
                        % url_for(method, page=page,
                            priority=str(priority), _external=True))
            data += '</sitemapindex>'

            tmp_file.write(data.encode())
            mimetype = 'application/xml'
            # Workaround to avoid closed file error
            # https://stackoverflow.com/questions/58197454/using-bytesio-and-flask-send-file
            # Remove with flask 2.0
            tmp_file.seek(0)
            return send_file(io.BytesIO(tmp_file.read()),
                max_age=self.max_age,
                mimetype=mimetype)

    @cached_property
    def count(self):
        """
        Returns the number of items of the object
        """
        max_id = self.model.search(
            self.domain, order=[('id', 'DESC')], limit=1
        )
        return max_id and max_id[0].id or 0

    @cached_property
    def page_count(self):
        """
        Returns the number of pages that will exist for the sitemap index
        >>> int(ceil(1.00/50000.00))
        1
        >>> int(ceil(50000.00/50000.00))
        1
        >>> int(ceil(50001.00/50000.00))
        2
        >>> int(ceil(100000.00/50000.00))
        2
        >>> int(ceil(100001.00/50000.00))
        3
        """
        return int(ceil(float(self.count) / float(self.batch_size)))


class SitemapSection(object):
    """
    A SitemapSection class is a simple Python class that represents a
    "section" of  entries in your sitemap. For example, one Sitemap class could
    represent all the entries of your weblog, while another could represent all
    of the events in your events calendar.

    In the simplest case, all these sections get lumped together into one
    `sitemap.xml`, but it's also possible to use the framework to generate a
    sitemap index that references individual sitemap files, one per section.

    The implementation though inspired by the Django project, is heavily
    influenced around the design of the Tryton project.


    How to use::

        Step 1: Create a method name sitemap for each model that needs to use
                a sitemap. Example:

                class Product(ModelSQL, ModelView):
                    __name__ = "product.product"

                    @classmethod
                    def sitemap(cls, page):
                        sitemap_section = SitemapSection(
                            cls, cls.search_domain, page
                            )
                        return sitemap_section.render()

                    def get_absolute_url(self, **kwargs):
                        "Return the full_path of the current object"
                        return url_for('product.product.render',
                            uri=self.uri, **kwargs)


    :param model: The Tryton model/object from which the pagination needs to
                  be generated. Passing `self` from the calling object's method
                  would be the usual way you will have to pass this argument
    :param domain: The domain expression which should be searched against in
                   the model
    :param page: The page of the sitemap.
    """

    #: The timeout in seconds for the headers, which would be respceted by
    #: intermediate cache servers.
    max_age = 60 * 60 * 24

    #: Indicates how frequently the page is likely to change. This value
    #: provides general information to search engines and may not correlate
    #: exactly to how often they crawl the page. Valid values are:
    #:
    #:     always
    #:     hourly
    #:     daily
    #:     weekly
    #:     monthly
    #:     yearly
    #:     never
    #:
    #: The value "always" should be used to describe documents that change
    #: each time they are accessed. The value "never" should be used to
    #: describe archived URLs. Please note that the value of this tag is
    #: considered a hint and not a command.
    #:
    #: Even though search engine crawlers may consider this information when
    #: making decisions, they may crawl pages marked "hourly" less frequently
    #: than that, and they may crawl pages marked "yearly" more frequently
    #: than that. Crawlers may periodically crawl pages marked "never" so that
    #: they can handle unexpected changes to those pages.
    #:
    #: Defaults to 'never'
    changefreq = 'never'

    #: The priority of this URL relative to other URLs on your site. Valid
    #: values range from 0.0 to 1.0. This value does not affect how your pages
    #: are compared to pages on other sitesâ€”it only lets the search engines
    #:  know which pages you deem most important for the crawlers.
    #:
    #: A default priority of 0.5 is assumed by the protocol.
    #:
    #: Please note that the priority you assign to a page is not likely to
    #: influence the position of your URLs in a search engine's result pages.
    #: Search engines may use this information when selecting between URLs on
    #: the same site, so you can use this tag to increase the likelihood that
    #: your most important pages are present in a search index.
    #:
    #: Also, please note that assigning a high priority to all of the URLs on
    #: your site is not likely to help you. Since the priority is relative, it
    #: is only used to select between URLs on your site.
    priority = 0.5

    #: It is really memory intensive to call complete records and generate site
    #: maps from them if the collection is large. Hence the queries may be
    #: divided into batches of this size
    batch_size = 1000

    min_id = property(lambda self: (self.page - 1) * self.batch_size)
    max_id = property(lambda self: self.min_id + self.batch_size)

    def __init__(self, model, domain, page):
        self.model = model
        self.domain = domain
        self.page = page

    def __iter__(self):
        """
        The default implementation searches for the domain and finds the
        ids and generates xml for it
        """
        domain = [('id', '>', self.min_id), ('id', '<=', self.max_id)]
        domain = domain + self.domain

        ids = self.model.search(domain)
        for id in ids:
            record = self.model(id)
            yield(self.get_url_xml(record))
            del record

    def render(self):
        """
        This method writes the sitemap directly into the response as a
        stream using the ResponseStream
        """
        with io.BytesIO() as tmp_file:
            data = '<?xml version="1.0" encoding="UTF-8"?>\n'
            data += '<urlset '
            data += 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            for line in self:
                data += etree.tostring(line).decode('utf-8') + '\n'
            data += '</urlset>'

            tmp_file.write(data.encode())
            mimetype = 'application/xml'
            # Workaround to avoid closed file error
            # https://stackoverflow.com/questions/58197454/using-bytesio-and-flask-send-file
            # Remove with flask 2.0
            tmp_file.seek(0)
            return send_file(io.BytesIO(tmp_file.read()),
                max_age=self.max_age,
                mimetype=mimetype)

    def get_url_xml(self, item):
        """
        Returns the etree node for the specific item
        """
        return E(
            'url',
            E('loc', self.loc(item)),
            E('lastmod', self.lastmod(item)),
            E('changefreq', self.changefreq),
            E('priority', str(self.priority)),
        )

    def loc(self, item):
        """
        URL of the page. This URL must begin with the protocol
        (such as http) and end with a trailing slash, if the application
        requires it. This value must be less than 2,048 characters.

        The URL can probably be generated using url_for and with external
        as True to generate absolute URLs

        Default: returns the absolute url of the object

        :param item: Instance of the item.
        """
        return item.get_absolute_url(_external=True)

    def lastmod(self, item):
        """
        The date of last modification of the file. This date should be in
        W3C Datetime format. This format allows you to omit the time portion,
        if desired, and use YYYY-MM-DD. Note that this tag is separate from
        the If-Modified-Since (304) header the server can return, and
        search engines may use the information from both sources differently.

        The default implementation fetches the write_date of the record and
        returns it in the W3C Datetime format

        Note: This attribute is optional and ignored if value is None
        """
        timestamp = item.write_date or item.create_date
        timestamp_in_utc = pytz.utc.localize(timestamp)
        return timestamp_in_utc.isoformat()
