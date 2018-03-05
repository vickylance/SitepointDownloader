import glob
import ntpath
import os
import requests
import re
from os.path import basename

path = "video_courses/"
savepath = "video_download/"

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def get_valid_foldername(s):
    return " ".join(str(s).replace('/', ' or ').replace('?', '').split('_'))

def makeDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def downloadfile(name,url):
    r = requests.get(url, stream = True)
    print "****Connected****"
    f=open(name,'wb');
    print "Downloading.....  " + name 
    # download started
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024*1024):
            if chunk:
                f.write(chunk)
        
    print "%s downloaded!\n"%name
    f.close()

for files in glob.glob(path + "*.txt"):
    infile = list(open(files))
    root, ext = os.path.splitext(basename(files))
    # makeDir(savepath + get_valid_foldername(root))
    # outfile = open(savepath,'w')
    for line in infile:
        downloadfile(savepath + get_valid_foldername(root) + '/' + get_valid_foldername(line.split('||')[0])+".mp4", line.split('||')[1])
    # for k in range (0,len(a)):
    #     print(a[0], file=outfile, end='')
    # infile.close()
    # outfile.close()
print "done" 