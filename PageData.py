import os
import re
import frontmatter
import log

class PageData():

  pretty = True

  def __init__(self, file_name):
    self.fname = os.path.abspath(file_name)
    self._setup_name()
    self._setup_url()
    self._parse_page()

  def _setup_name(self):
    name = os.path.basename(self.fname)
    self.name = os.path.splitext(name)[0]

  def _setup_url(self):
    rel_name = os.path.relpath(self.fname, "pages")  
    url = os.path.splitext(rel_name)[0]
    if not PageData.pretty:
      url += ".html" 
    if url[0] == ".":
      url = url[1:]
    else:
      url = '/' + url
    if url.endswith("index"):
      url = url[:-5]
    self.url = url

  def _parse_page(self):
    with open(self.fname, "r") as f:
      metadata, content = frontmatter.parse(f.read())
      self.metadata = metadata
      self.content = content
      self.file_ext = os.path.splitext(self.fname)[1]

  def __repr__(self):
    info = "===============\n"
    info += "filename: %s\n" % self.fname
    info += "name: %s\n" % self.name
    info += "file ext: %s\n" % self.file_ext
    info += "url: %s\n" % self.url
    info += "metadata: %s\n" % self.metadata
    info += "content:\n%s" %self.content
    return info
