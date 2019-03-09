#!/usr/bin/python3

import yaml
import jinja2
import markdown
import frontmatter
import os

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
    return config, site

def setup_templates():
  env = jinja2.Environment(loader=jinja2.FileSystemLoader("layouts"), autoescape=jinja2.select_autoescape(["html", "xml"]))
  return env

def gen_site():

  if not check_dirs():
    return

  # Read config options and site variable.
  config, site = read_config()

  # Open templates and have them ready to go
  template_list = os.listdir("layouts")
  env = setup_templates()
  if not "default.html" in env.list_templates():
    print("No default template found!")
    return 

  # Now, create our output directory if it doesn't exist.
  curr_dir = os.listdir()
  if not "output" in curr_dir:
    os.mkdir("output")

  # Go through the contents of the pages directory and generate an html file for each one.
  pages = os.listdir("pages")
  for page in pages:
    fname, fext = os.path.splitext("pages/%s" % page)
    if not fext == ".md":
      continue
    print("Writing %s..." % page)
    with open("pages/%s" % page, "r") as page_file:
      metadata, content = frontmatter.parse(page_file.read())
      content = markdown.markdown(content)
      cont_templ = jinja2.Template(content)
      content = cont_templ.render(site=site, page=metadata)
      if metadata["layout"]:
        templ = env.get_template(metadata["layout"] + ".html")
      else:
        templ = env.get_template("default.html")
      out = templ.render(site=site, content=content, page=metadata) 
      name = page.split(".")[0]
      if config["pretty_urls"] and not name == "index":
        os.mkdir("output/%s" % name)
        with open("output/%s/index.html" % (name), "w") as out_file:
          out_file.write(out)
      else:
        with open("output/%s%s" % (name, ".html"), "w") as out_file:
          out_file.write(out)

  print("Site generated...")

if __name__ == "__main__":
  gen_site()
