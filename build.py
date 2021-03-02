import os,glob
import markdown
import shutil

def toMarkdown(line):
  if "@ Title: " in line:
    return "<title>Tristan Goodell &mdash; " + line[9:] + "</title>"
  elif "@ Description: " in line:
    return "<meta name='description' content=" + line[15:] + "'>"
  elif "@ Author: " in line:
    return "<meta name='author' content='" + line[10:] + "'>"
  elif "@ Keywords: " in line:
    return "<meta name='keywords' content='" + line[12:] + "'>"
  elif "@ Date: " in line:
    return line[8:]
  else:
    return markdown.markdown(line)

pages=[]
pageContent=[]

folder_path = 'md-pages/'
for filename in glob.glob(os.path.join(folder_path, '*.md')):
  with open(filename, 'r') as f:
    text=f.read()
    newPage=filename[9:14]
    pages.append(newPage)

    newPageContent=""

    for line in text.split("\n"):
      newPageContent+=toMarkdown(line)

    pageContent.append(newPageContent)

print(pages)
print(pageContent)

shutil.rmtree("p/")
os.mkdir("p")

n=0
for pageTitle in pages:
  pageTitle=pageTitle.replace(" ","-").lower
  os.mkdir("p/" + str(pageTitle))

  htmlFile=open("p/" + pageTitle + "/index.html",w)
  htmlFile.write(pageContent[n])

  n+=1