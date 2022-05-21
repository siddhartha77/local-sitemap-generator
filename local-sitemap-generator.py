# Python 3.6+

import pathlib
from html import escape

# Local directory to index
BASE_DIR = "C:/www/testsite"
# Path under BASE_DIR to index
SUB_DIR = "/public/"
# Replace BASE_DIR with this
URL_BASE = "https://testsite.com/"

# Index only this extension pattern (*.html, *.htm)
FILE_FILTER = "*.htm[l?]"
# Filenames will look like sitemap-path-001.xml
XML_URLSET_FILENAME_PREFIX = "sitemap" + SUB_DIR.replace("/","-")
# If multiple files are generated, sitemapindex.xml will index them
XML_SITEMAPINDEX_FILENAME = "sitemapindex.xml"
# Headers and footers are 111 bytes
DEFAULT_XML_FILESIZE = 111
# Max sitemap.xml for Google is 50MB
MAX_XML_FILESIZE = 49000000
# Max files in a single sitemap.xml is 50000
XML_MAX_FILES = 50000

def prep_xml_file(f, type):
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<" + type + " xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")

def end_xml_file(f, type):
    f.write("</" + type + ">")

def main():
    xml_filecount = 1
    xml_full_filename = XML_URLSET_FILENAME_PREFIX + f"{xml_filecount:03d}" + ".xml"
    xml_filesize = DEFAULT_XML_FILESIZE
    filecount = 0
    
    f = open(xml_full_filename, "w")
    prep_xml_file(f, "urlset")
    
    for file in pathlib.Path(BASE_DIR + SUB_DIR).glob("**/" + FILE_FILTER):
        path = escape(file.as_posix().replace(BASE_DIR, URL_BASE))
        write_str = "<url><loc>" + path + "</loc></url>\n"
        f.write(write_str)
        xml_filesize += len(write_str)
        filecount += 1

        if filecount % 10000 == 0:
            print(filecount)
        
        if xml_filesize > MAX_XML_FILESIZE or filecount > XML_MAX_FILES:
            end_xml_file(f, "urlset")
            f.close()
            xml_filecount += 1
            xml_filesize = DEFAULT_XML_FILESIZE
            filecount = 0
            f = open(xml_full_filename, "w")
            prep_xml_file(f, "urlset")     

    end_xml_file(f, "urlset")
    f.close()

    if xml_filecount > 1:
        f = open(XML_SITEMAPINDEX_FILENAME, "w")
        prep_xml_file(f, "sitemapindex")

        for i in range(1, xml_filecount + 1):
            write_str = URL_BASE + XML_URLSET_FILENAME_PREFIX + f"{i:03d}" + ".xml"
            f.write("<sitemap><loc>" + write_str + "</loc></sitemap>\n")

        end_xml_file(f, "sitemapindex")
        f.close()

    print("Done!")

if __name__ == "__main__":
    main()
