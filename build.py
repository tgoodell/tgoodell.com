import os,glob
import markdown
import shutil

def toMarkdown(line):
  if "@ Title: " in line:
    return "Title: " + line[9:]
  elif "@ Description: " in line:
    return "Description: " + line[15:]
  elif "@ Author: " in line:
    return "Author: " + line[10:]
  elif "@ Keywords: " in line:
    return "Keywords: " + line[12:]
  elif "@ Date: " in line:
    return "Date: " + line[8:]
  else:
    return markdown.markdown(line)

pages=[]
titleList=[]
descriptionList=[]
authorList=[]
keywordList=[]
dateList=[]
pageContent=[]

folder_path = 'md-pages/'
for filename in glob.glob(os.path.join(folder_path, '*.md')):
  with open(filename, 'r') as f:
    text=f.read()
    newPage=filename[9:14]
    pages.append(newPage)

    newPageContent=""

    for line in text.split("\n"):
      mline=toMarkdown(line)
      if mline[:7]=="Title: ":
        titleList.append(mline[7:])
      elif mline[:13]=="Description: ":
        descriptionList.append(mline[13:])
      elif mline[:8]=="Author: ":
        authorList.append(mline[8:])
      elif mline[:10]=="Keywords: ":
        keywordList.append(mline[10:])
      elif mline[:6]=="Date: ":
        dateList.append(mline[6:])
      else:
        newPageContent+=toMarkdown(line)+"\n"

    pageContent.append(newPageContent)

print(pages)
print(pageContent)

shutil.rmtree("public/p")
os.remove("public/index.html")
os.mkdir("public/p")

n=0
for pageTitle in pages:
  pageTitle=str(pageTitle).replace(" ","-").lower()

  htmlFile=open("public/p/" + str(pageTitle) + ".html","w")
  with open("partials/standard.html", 'r') as f:
    fileContents = f.read()
  with open("partials/nav.html", 'r') as f:
    fileContents=fileContents.replace("{{{nav}}}",f.read())
  with open("partials/footer.html", 'r') as f:
    fileContents=fileContents.replace("{{{footer}}}",f.read())

  fileContents=fileContents.replace("{{{content}}}",pageContent[n])
  fileContents=fileContents.replace("{{{title}}}",titleList[n])
  fileContents=fileContents.replace("{{{author}}}",authorList[n])
  fileContents=fileContents.replace("{{{keywords}}}",keywordList[n])
  fileContents=fileContents.replace("{{{description}}}",descriptionList[n])

  htmlFile.write(fileContents)

  n+=1

n=0
pageTable=""
for page in pages:
  pageTable+="<tr>\n<td>" + str(n) +"</td>\n<td><a href='p/" + str(pages[n]).replace(" ","-").lower() + ".html'>" + str(titleList[n]) + "</a></td>\n<td>" + str(keywordList[n]) + "</td>\n</tr>\n"
  n+=1
  
with open("partials/home.html", 'r') as f:
    home=f.read()
    home=home.replace("{{{pages}}}",pageTable)
    htmlFile=open("public/index.html","w")
    htmlFile.write(home)
