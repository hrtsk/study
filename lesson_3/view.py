import eel
import desktop
import search
import re
import os

app_name="html"
end_point="index.html"
size=(700,600)

@eel.expose
def kimetsu_search(word, input_path, path):
    search.kimetsu_search(word, input_path, path)
    
@eel.expose
def path_search(path):
    name = re.search(r"C:\\fakepath\\(.*)" , path)
    file_name = name.group(1) #type: ignore
    file_path = os.path.abspath(file_name)
    eel.abs_path(file_path) #type: ignore

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)