#!/usr/bin/python3

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
  log.info("INIT: NOT YET SUPPORTED")

@quorthon.command(help="Initialize directory/file structure for Quorthon.")
def init():
  gen_site.init_dirs()

if __name__ == "__main__":
  quorthon()
