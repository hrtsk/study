import eel
import desktop
import search
import os
import sys

app_name="html"
end_point="index.html"
size=(700,600)

@eel.expose
def kimetsu_search(word, path, file_name):
    search.kimetsu_search(word, path, file_name)
    
@eel.expose
def path_search(file_name):
    file_dir = os.path.dirname(sys.argv[0])
    dir = os.path.dirname(file_dir)
    eel.abs_path(os.path.join(dir, file_name)) #type: ignore

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)