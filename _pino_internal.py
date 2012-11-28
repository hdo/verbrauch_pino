import sys, os, shutil, json, datetime, time;
from time import strftime, gmtime;

#################
### Functions ###
#################
# Get sorted files list without .DS_Store file
def pino_list_directory(p_path, p_reverse=True):
	listing = os.listdir(p_path)
	if ".DS_Store" in listing:
		listing.remove(".DS_Store")
	return sorted(listing, None, None, p_reverse)

# Copy all files in the source directory to the destination directory, except metadata files
def pino_copy_aux_files(p_path, p_to_path):
	listing = [x for x in pino_list_directory(p_path) if x != "_attr.json" and x != "_post.html"]
	for f in listing:
		shutil.copy(p_path + f, p_to_path + f)

# Get month name from 2 digits number as string
def pino_month_from_number(p_num):
	return {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}[p_num]

# Load the JSON attributes file at path
def pino_get_attr_at_path(p_path):
	return json.loads(open(p_path, 'r').read())

# Load the config file
def pino_load_config_file(p_path="_pino_config.json"):
	return json.loads(open(p_path, 'r').read())

def pino_save_content_to_file(p_path, p_content):
	handle = open(p_path, 'w')
	handle.write(p_content)
	handle.close()

# Open a given file and replace placeholder with config values, then save to build dir
def pino_format_file(p_file_in, p_cfg):
	content = open(p_file_in, 'r').read()
	new_content = content.replace("__PINO_SITE_NAME__", p_cfg["site_title"].encode('utf-8'))
	new_content = new_content.replace("__PINO_SITE_TAGLINE__", p_cfg["site_tagline"].encode('utf-8'))
	new_content = new_content.replace("__PINO_SITE_AUTHOR__", p_cfg["site_author"].encode('utf-8'))
	new_content = new_content.replace("__PINO_SITE_COPYRIGHT__", p_cfg["site_copyright"].encode('utf-8'))
	new_content = new_content.replace("__PINO_AUTHOR_TWITTER__", p_cfg["author_twitter_name"].encode('utf-8'))
	new_content = new_content.replace("__PINO_AUTHOR_TWITTER_URL__", p_cfg["author_twitter_url"].encode('utf-8'))
	return new_content;

########## RSS ##########
# Begin RSS
def pino_begin_rss(p_cfg):
	rss_header = '<?xml version="1.0" encoding="UTF-8"?>\r<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\r\t<channel>\r\t\t<title>' + p_cfg["site_title"] + '</title>\r\t\t<description>' + p_cfg["site_tagline"] + '</description>\r\t\t<link>'+ p_cfg["site_url"] + '</link>\r\t\t<lastBuildDate>' + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + '</lastBuildDate>'
	return rss_header

# Add RSS item
def pino_add_rss_item(p_cfg, p_title, p_desc, p_date, p_link, p_guid):
	rss_item = "\r\t\t<item>\r\t\t\t"
	rss_item += "<title>" + p_title + "</title>\r\t\t\t"
	rss_item += "<description>" + p_desc + "</description>\r\t\t\t"
	rss_item += "<pubDate>" + strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(p_date)) + "</pubDate>\r\t\t\t"
	rss_item += "<link>" + p_link + "</link>\r\t\t\t"
	rss_item += "<guid>" + p_guid + "</guid>\r\t\t"
	rss_item += "</item>"
	return rss_item

# End RSS
def pino_end_rss():
	return '\r\t</channel>\r</rss>'
