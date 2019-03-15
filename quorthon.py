#!/usr/bin/python3

import click
import http.server
import os
import frontmatter
import sys
import yaml
import jinja2
import markdown
import sass
import shutil
import glob

DEFAULT_CONFIG = "---\n\
site:\n\
  title: \"Test Site\"\n\
  base_url: \"http://127.0.0.1:8000\"\n\
pretty_urls: True "

def debug(msg):
  out = "[ DEBUG ]: %s" % msg
  print(out)

def error(msg):
  out = "[ ERROR ]: %s" % msg
  sys.exit(out)

def info(msg):
  out = "[ INFO  ]: %s" % msg
  print(out)

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
    outstr  = "===============\n"
    outstr += "filename: %s\n" % self.fname
    ouinfo += "name: %s\n" % self.name
    ouinfo += "file ext: %s\n" % self.file_ext
    ouinfo += "url: %s\n" % self.url
    ouinfo += "metadata: %s\n" % self.metadata
    ouinfo += "content:\n%s" %self.content
    return outstr 

def check_dirs():
  # Check for all required directories and files
  curr_dir = os.listdir() 
  if not "config.yml" in curr_dir:
    print("No config file in directory!")
    return False
  if not "layouts" in curr_dir:
    print("No layouts folder in directory!")
    return False
  if not "pages" in curr_dir:
    print("No pages folder in directory!")
    return False
  return True

def read_config():
  # Open the configuration YAML and read in necessary options.
  with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)
    site = config["site"] #site variable used across site
    if "pretty_urls" in config:
      PageData.pretty = config["pretty_urls"]
    return config, site

def parse_data():
   if not os.path.isdir("data"):
     return None 
   yaml_files = glob.glob("data/*.yml")
   data = dict()
   for data_file in yaml_files:
     name = os.path.basename(data_file)
     name = os.path.splitext(name)[0]
     with open(data_file, "r") as f:
       data[name] = yaml.load(f)
   return data
       
def setup_templates():
  env = jinja2.Environment(loader=jinja2.FileSystemLoader("layouts"))
  return env

def parse_pages():
  page_dir = "pages"
  pages_info = []
  for _dir, subdir, files, in os.walk(page_dir):
    for file_name in files:
      fname = os.path.join(_dir, file_name)
      page = PageData(fname)
      pages_info.append(page)
  return pages_info

def gen_page(page, site, config, env):
  if page.file_ext == ".md":
    info("Writing %s..." % page.fname)
    content = markdown.markdown(page.content)
    cont_templ = jinja2.Template(content)
    content = cont_templ.render(site=site, page=page.metadata)
    if page.metadata["layout"]:
      template_name = page.metadata["layout"] + ".html"
    else:
      template_name = "default.html"
    templ = env.get_template(template_name)
    if not templ:
      error("Template %s not found!" % page.metadata["layout"])
    out = templ.render(site=site, content=content, page=page.metadata)
    if PageData.pretty:
      outdir = os.path.join(os.getcwd(), "output")
      outdir = os.path.join(outdir, page.url[1:])
      if not os.path.isdir(outdir):
        os.makedirs(outdir)
      with open("output/%s/index.html" % page.url, "w") as f:
        f.write(out)
    else:     
      warning("UGLY URLS NOT YET SUPPORTED")
  if page.file_ext == ".html":
    warning("HTML NOT YET SUPPORTED")
  return

def compile_sass():
  IN_DIR = "output/assets/scss"
  OUT_DIR = "output/assets/css"
  if not os.path.isdir(IN_DIR):
    return
  if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)
  sass.compile(dirname=("assets/scss", "assets/css"))
  shutil.rmtree(IN_DIR)
  return

def init_dirs():
  curr_dir = os.listdir() 
  if not "config.yml" in curr_dir:
    print("Creating config.yml...")
    with open("config.yml", "w") as config_yml:
      config_yml.write(DEFAULT_CONFIG)
  if not "layouts" in curr_dir:
    print("Creating layouts directory...")
    os.mkdir("layouts")
  if not "pages" in curr_dir:
    print("Creating pages directory...")
    os.mkdir("pages")
  if not "assets" in curr_dir:
    print("Creating assets directory...")
    os.mkdir("assets")


def gen_site():

  if not check_dirs():
    return

  # Read config options and site variable
  config, site = read_config()

  # Open templates and have them ready to go
  template_list = os.listdir("layouts")
  env = setup_templates()
  if not "default.html" in env.list_templates():
    print("No default template found!")
    return 

  # Load all data into our site variable
  data = parse_data()
  site["data"] = data

  # Now, create our output directory.
  if "output" in os.listdir():
    shutil.rmtree("output")
  os.mkdir("output")

  # Copy over files in the assets directory
  shutil.copytree("assets", "output/assets")

  # Compile any SASS found.
  compile_sass()

  # Generate the pages.
  pages = parse_pages()
  for page in pages:
    gen_page(page, site, config, env)
  print("Site generated...")


@click.group()
def quorthon():
  pass

@quorthon.command(help="Build your site to the output directory.")
def build():
  gen_site()

@quorthon.command(help="Serve your site from the output directory.")
def serve():
  info("INIT: NOT YET SUPPORTED")

@quorthon.command(help="Initialize directory/file structure for Quorthon.")
def init():
  init_dirs()

if __name__ == "__main__":
  quorthon()
