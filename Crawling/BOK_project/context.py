

from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

init = ScrapyClientContextFactory.__init__ 
def init2(self, *args, **kwargs):
  init(self, *args, **kwargs)
  self.method = SSL.SSLv23_METHOD
ScrapyClientContextFactory.__init__ = init2
