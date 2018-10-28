import os
import re
import urllib.request as ur
import html
import csv

def f(root,r1,r2,r3):
    a = "{0}/{1}/{2}/{3}".format(root,r1,r2,r3)
    b = "{0}/{1}/{2}".format(root,r1,r2)
    c = "{0}/{1}".format(root,r1)
    d = "{0}".format(r3)
    if os.path.exists(a) == True:
        if os.path.exists(b) == True:
            if os.path.exists(c) == True:
                if os.path.exists(d) == True:
                   os.mkdir(r3)
            else:
                os.makedirs(c)
        else:
            os.makedirs(b)
    else:
        os.makedirs(a)

def crHeaddir():
    if not os.path.exists(os.getcwd()+"/газета"):
        os.makedirs(os.getcwd()+"/газета")
    fi = open(os.getcwd()+"/газета/Table.csv", "w")
    fi.close()


def linksOnPage(way):
    k = 1
    resarr = []
    linkNP = 'http://sp-18.ru/'
    for k in range(1, 10):
        try:
            url = linkNP + way + '/page/' + str(k) + '/'
            page = ur.urlopen(url)
            text = page.read().decode('utf-8')
            regex = r'<a href="http://sp-18.ru/20../../.*?/#more-.+?" class="more-link"><span class="continue">Читать дальше</span>'
            res = re.findall(regex, text)
            if res:
                resarr.append(res)
            k += 1
        except:
            continue
    return resarr

def linksWriting(resarr):
    links = []
    for elem in resarr:
        for el in elem:
            e = str(el)
            regex1 = '"(http://sp-18.ru/20../../.*?/#more-.+?)" class="more-link"><span class="continue">Читать дальше'
            res1 = re.search(regex1, el)
            if res1:
                links.append(res1.group(1))
            else:
                continue
    return links

def downloadArticles(links,year,month):
    for i,elem in enumerate(links):
        url = str(elem)
        page = ur.urlopen(url)
        text = page.read().decode('utf-8')

        textAt = (html.unescape(text))
        au = '@au Noname'
        regexTi = '<h1>(.*?)</h1>'
        tiN = re.findall(regexTi, textAt)
        tiNa = (tiN[0])
        ti = '@ti ' + tiNa
        regexDa = 'Написано: (..)'
        daNu = re.findall(regexDa, textAt)
        daNum = (daNu[0])
        da = '@da ' + daNum + '.' + str(month) + '.' + str(year)
        regexTo = 'category tag">(.*?)<'
        top = re.findall(regexTo, textAt)
        if len(top)>0:
            topic = '@topic ' + (top[0])
        else:
            topic = '@topic ' + 'None'
        urlad = '@url ' + elem
        #(au, ti, da, topic, urlad)
        regex = '<div class="entry">(.*?)</div>'
        res = re.findall(regex, text, flags=re.DOTALL)
        res = str(res)
        regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
        regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
        regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
        clean_t = regScript.sub("", res)
        clean_t = regComment.sub("", clean_t)
        clean_t = regTag.sub("", clean_t)
        clFile = (html.unescape(clean_t))
        res = str(clFile)
        for ind,e in enumerate(res):
            if(e in ["\\","n","r","t","]","[","'"]):
                res = res.replace(e," ")
        res = res.split(" ")
        res1 = ""
        for ind1,e in enumerate(res):
            res[ind1] = res[ind1].strip(" ")
            if e:
                res1 += e+" "
        res = res1
        path1 = "{0}/article{1}.txt".format(os.getcwd()+"/газета/plain/"+str(year)+"/"+str(month),str(i+1))
        path2 = "{0}/article{1}.txt".format(os.getcwd() + "/газета/mystem-plain/" + str(year) + "/" + str(month), str(i+1))
        path3 = "{0}/article{1}.xml".format(os.getcwd()+"/газета/mystem-xml/"+str(year)+"/"+str(month),str(i+1))
        fle = open(path1, 'w')

        fle.write(au+"\n"+ti+"\n"+da+"\n"+topic+"\n"+urlad+"\n"+str(res))
        fle.close()
        fle = open(path2, 'w')
        fle.write("")
        fle.close()
        fle = open(path3, 'w')
        fle.write("")
        fle.close()
        os.system('./mystem -ncid ' + path1 + ' ' + path2)
        os.system('./mystem -ncid ' + path1 + ' ' + path3)
        with open(os.getcwd()+"/газета/Table.csv","a", encoding= "UTF-8") as csvfile:
            line = [path1,"Noname","None","None",tiNa,daNum + '.' + str(month) + '.' + str(year),"публицистика"
                ,"None","None",top[0],"None","нейтральный","н-возраст","н-возраст","районная"
                ,elem,"Сельская правда","None",daNum + '.' + str(month) + '.' + str(year),"Газета","Россия","Удмуртская Республика","ru"]
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='\t', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(line)

def main():
    crHeaddir()
    i = 2010
    j = 7
    way = ''
    for i in range (2010, 2013):
        for j in range (1, 13):
            if len(str(j)) < 2:
                j = '0' + str(j)
            way = str(i) + '/' + str(j)
            val1 = linksOnPage(way)
            val2 = linksWriting(val1)
            f(os.getcwd() + "/газета","plain",i,j)
            f(os.getcwd() + "/газета", "mystem-xml", i, j)
            f(os.getcwd() + "/газета", "mystem-plain", i, j)
            val3 = downloadArticles(val2,i,j)
            j = int(j) + 1
        else:
            j = int(j)-12
    i = int(i) + 1

main()
