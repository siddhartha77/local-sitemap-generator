# local-sitemap-generator
Generates sitemap.xml files for locally stored files.

# Setup
There should only be three variables you need to change:

**BASE_DIR**: This is the root of the local directory you want to index. This will be replaced with URL_BASE below.

**SUB_DIR**: The subdirectory of BASE_DIR you want to index. Set to "/" to index everything.

**URL_BASE**: The URL where your files are located. This is also assumed to be the directory where the sitemap.xml files will be stored if multiple XML files are generated because they are greater than 50MB or contain more than 50,000 files.
