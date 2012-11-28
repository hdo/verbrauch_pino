import sys, os, shutil, json, datetime;
from time import strftime, gmtime;
from _pino_internal import *;

## Change CWD, this script MUST BE in the basedir of the site ##
os.chdir(os.path.dirname(os.path.realpath(__file__)))

############
### Vars ###
############
my_pino_cfg = pino_load_config_file();
my_build_dir = my_pino_cfg["pino_build_path"]
my_pages_dir = "pages/"
my_posts_dir = "posts/"
my_styles_dir = "styles/"
my_tpl_dir = "templates/"
my_tpl_post = pino_format_file(my_tpl_dir + "post.html", my_pino_cfg)
my_max_rss_items = my_pino_cfg["pino_max_rss_items"]

## Create build directory ##
if os.path.exists(my_build_dir) == True:
   shutil.rmtree(my_build_dir)
os.mkdir(my_build_dir)

## Copy styles (css / js / images...) ##
shutil.copytree(my_styles_dir, my_build_dir + my_styles_dir)

## Copy htaccess
if os.path.exists("htaccess") == True:
   shutil.copy("htaccess", my_build_dir + ".htaccess")

## Copy 404 ##
errpage = pino_format_file(my_tpl_dir + "404.html", my_pino_cfg)
pino_save_content_to_file(my_build_dir + "404.html", errpage)

## Create static pages ##
listing = pino_list_directory(my_pages_dir)
for filename in listing:
   tmp = os.path.basename(my_pages_dir + filename)
   dir_name = os.path.splitext(tmp)[0]
   os.mkdir(my_build_dir + dir_name)
   static_page = pino_format_file(my_pages_dir + filename, my_pino_cfg)
   pino_save_content_to_file(my_build_dir + dir_name + "/index.html", static_page)

## Create posts pages & Archives list ##
html_archives = ""
## RSS ##
rss_done = 0
rss = pino_begin_rss(my_pino_cfg)
# Loop through all years

current_data_file = my_posts_dir + '_post.html'
if os.path.exists(current_data_file) and os.path.isfile(current_data_file):
   html_archives += '\n<p class="posts-year">' + "Aktuelle Verbrauchswerte" + '</p>'
   f_content = open(current_data_file, 'r').read()
   html_archives += '\n' + f_content + '\n'
 


list_year = pino_list_directory(my_posts_dir)
for dirname_year in list_year:
   if os.path.isfile(my_posts_dir + dirname_year):
      continue

   os.mkdir(my_build_dir + dirname_year)
   html_archives += '\n<p class="posts-year">' + dirname_year + '</p>'
   path_year = my_posts_dir + dirname_year + '/'
   # Loop through all months
   list_month = pino_list_directory(path_year)
   for dirname_month in list_month:
      html_archives += '\n<p class="posts-month">' + pino_month_from_number(dirname_month) + '</p>' + '<div class="posts-list">'
      path_month = path_year + dirname_month + '/'
      # Loop through all posts
      list_day = pino_list_directory(path_month)
      for dirname_day in list_day:
         path_day = path_month + dirname_day         
         if os.path.isfile(path_day):       
            if dirname_day =='_post.html':
               month_content = open(path_day, 'r').read()
               html_archives += '\n' + month_content + '\n'
            continue
         splitted = dirname_day.split('.')
         os.makedirs(my_build_dir + dirname_year + '/' + dirname_month + '/' + splitted[1])
         attrs = pino_get_attr_at_path(path_month + dirname_day + "/_attr.json")
         title = attrs['title'].encode('utf-8')
         #html_archives += '\n<p class="posts-list-title"><span class="posts-list-day">' + splitted[0] + '</span> <a href="./' + dirname_year + '/' + dirname_month + '/' + splitted[1] + '/" title="' + title + '">' + title + '</a></p>'
         # Build page
         f_post = my_tpl_post.replace("__POST_TITLE__", title)
         f_post = f_post.replace("__POST_DATE__", pino_month_from_number(dirname_month)[0:3] + " " + splitted[0] + ", " + dirname_year)
         f_post = f_post.replace("__POST_CONTENT__", open(path_month + dirname_day + "/_post.html", 'r').read())
         f_post = f_post.replace("__POST_SEODESC__", attrs['seodesc'].encode('utf-8'))
         f_post = f_post.replace("__POST_KEYWORDS__", ','.join(attrs['keywords']).encode('utf-8'))
         handlep = open(my_build_dir + dirname_year + '/' + dirname_month + '/' + splitted[1] + '/index.html', 'w')
         handlep.write(f_post)
         handlep.close()
         # RSS
         if rss_done < my_max_rss_items:
            rss_link = my_pino_cfg["site_url"] + dirname_year + '/' + dirname_month + '/' + splitted[1] + '/'
            rss += pino_add_rss_item(my_pino_cfg, title, attrs['seodesc'].encode('utf-8'), attrs['timestamp'], rss_link, rss_link)
            rss_done = rss_done + 1

         pino_copy_aux_files(path_month + dirname_day + '/', my_build_dir + dirname_year + '/' + dirname_month + '/' + splitted[1] + '/')
      html_archives += '\n</div>\n'

## End RSS ##
os.mkdir(my_build_dir + "feed")
rss += pino_end_rss()
pino_save_content_to_file(my_build_dir + "feed/feed.rss", rss)

## Create index.html ##
content_index = pino_format_file("templates/index.html", my_pino_cfg)
content_index = content_index.replace("__ARCHIVES__", html_archives)
pino_save_content_to_file(my_build_dir + "index.html", content_index)
