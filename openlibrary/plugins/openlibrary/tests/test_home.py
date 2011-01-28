import datetime
import web
from infogami.utils.view import render_template
from infogami.utils import template
from openlibrary.i18n import gettext

from BeautifulSoup import BeautifulSoup

class TemplateTest:
    def load_templates(self, path):
        template.load_templates(path)
        
    def setup_method(self, method):
        self.load_templates("openlibrary/plugins/openlibrary")
        self.load_templates("openlibrary/plugins/upstream")

        web.template.Template.globals["_"] = gettext
        
        web.ctx.env = web.storage()
        web.ctx.headers = []
        web.ctx.lang = "en"
        
    def teardown_method(self, method):
        template.disktemplates.clear()
        web.ctx.clear()

class TestHome:
    pass

class TestHomeTemplates(TemplateTest):
    def test_about_template(self):
        html = unicode(render_template("home/about"))
        assert "About the Project" in html
    
        blog = BeautifulSoup(html).find("ul", {"id": "olBlog"})
        assert blog is not None
        assert len(blog.findAll("li")) == 0
        
        posts = [web.storage({
            "title": "Blog-post-0",
            "link": "http://blog.openlibrary.org/2011/01/01/blog-post-0",
            "pubdate": datetime.datetime(2011, 01, 01)
        })]
        html = unicode(render_template("home/about", blog_posts=posts))
        assert "About the Project" in html
        assert "Blog-post-0" in html
        assert "http://blog.openlibrary.org/2011/01/01/blog-post-0" in html

        blog = BeautifulSoup(html).find("ul", {"id": "olBlog"})
        assert blog is not None
        assert len(blog.findAll("li")) == 1
        
    def test_stats_template(self):
        html = unicode(render_template("home/stats"))
        assert "Around the Library" in html
        
    def test_read_template(self):
        html = unicode(render_template("home/read"))
        assert "Books to Read" in html
        
    def test_borrow_template(self):
        html = unicode(render_template("home/borrow"))
        assert "Return Cart" in html

    def test_home_template(self):
        html = unicode(render_template("home/index"))
        
        assert '<div class="homeSplash"' in html
        assert "Books to Read" in html
        assert "Return Cart" in html
        assert "Around the Library" in html
        assert "About the Project" in html