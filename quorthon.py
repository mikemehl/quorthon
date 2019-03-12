import click
import gen_site

@click.group()
def quorthon():
  pass

@quorthon.command(help="Build your site to the output directory.")
def build():
  gen_site.gen_site()

if __name__ == "__main__":
  quorthon()
