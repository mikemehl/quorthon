import click
import gen_site
import http.server
import os
import log

@click.group()
def quorthon():
  pass

@quorthon.command(help="Build your site to the output directory.")
def build():
  gen_site.gen_site()

@quorthon.command(help="Serve your site from the output directory.")
def serve():
  log.info("NOT YET SUPPORTED")

if __name__ == "__main__":
  quorthon()
