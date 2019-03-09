#!/usr/bin/python3

import yaml
import jinja2
import markdown
import frontmatter
import os

def gen_site():

  # Check for all required directories and files
  curr_dir = os.listdir() 
  if not "config.yml" in curr_dir:
    print("No config file in directory!")
    return
  if not "layouts" in curr_dir:
    print("No layouts folder in directory!")
  if not "pages" in curr_dir:
    print("No pages folder in directory!")

  # Open the configuration YAML and read in necessary options.
  with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)
    site = config["site"] #site variable used across site

  # Open templates and have them ready to go
  template_list = os.listdir("layouts")
  templates = dict() 
  for template in template_list:
    with open("layouts/%s" % template, "r") as templ_file:
      fname, fext = os.path.splitext(template) 
      templates[fname] = jinja2.Template(templ_file.read())
  if templates["default"] is None:
    print("No default template found!")
    return 

  # Now, create our output directory if it doesn't exist.
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
      out = templates["default"].render(site=site, content=content, page=metadata) 
      name = page.split(".")[0]
      with open("output/%s%s" % (name, ".html"), "w") as out_file:
        out_file.write(out)

  print("Site generated...")

if __name__ == "__main__":
  gen_site()
