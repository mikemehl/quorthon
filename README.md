# Quorthon

## A trve kvlt static site generator.

---

Quorthon is a small python application for creating static websites. Quorthon is geared towards simplicity and minimalism, providing only a few features:
 * layouts with Jinja2 templates
 * data stored in YAML form
 * content written in Markdown
 * support for rendering scss/sass

I made this tool after spending too long fussing with Jekyll and Pelican, and finding that they don't really fit my needs. This tool is for someone who needs to quickly knock up a bare bones website.

Quorthon is meant to be run as a command line tool. There are three commands:

 * **quorthon.py init** sets up the basic directory structure needed for Quorthon in the current directory.
 * **quorthon.py build** creates a directory called "output" and builds the site there.
 * **quorthon.py serve** starts a server to serve the output directory on port 12345.

A small sample site is included as an example.

Quorthon is named after the legendary musician of Bathory fame, because I was listening to too much black metal while working on this.
