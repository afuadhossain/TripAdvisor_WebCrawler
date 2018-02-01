import nltk, requests, re, pprint, urllib
from bs4 import BeautifulSoup
import sys

class Thread:
    def __init__(self, urlprefix, firstpage):
        self.usernames = []
        self.posts = "<s>"
        self.urlprefix = urlprefix
        self.firstpage = firstpage

    def parsePages(self):
        #original post carries from page to page
        #we only want to print the opening comment once
        firstpage = True
        r = urllib.urlopen(self.firstpage)
        soup = BeautifulSoup(r, 'html.parser')
        while(1):
            letters = soup.find_all('div', class_='postBody')
            for element in letters:
                if firstpage == False: #firstpage will be first on all subsequent pages
                    firstpage = True
                    continue;
                newPost = Post()
                #adds the latest post in XML format to our current string
                self.posts+=newPost.parsePost(element, self.usernames).toXML()

            firstpage = False
            #guiArw sprite-pageNext is the arrow to which contains a link to the next page
            pagenext = soup.find('a',class_='guiArw sprite-pageNext')
            #If there are no more pages in the thread we are finished
            if pagenext != None:
                link = pagenext.attrs['href'] #retrieves link to next pagenext
                r = urllib.urlopen(self.urlprefix+ link) #half to include the prefix because link only includes everythign after
                soup = BeautifulSoup(r, 'html.parser')
            else:
                break #terminate when we don't have any other pages to investigate
        self.posts += '</s>' #Add end tag to the post
        if len(self.usernames) == 1:
            return ''
        else:
            return self.posts + '\n'

class Post:
    def __init__(self):
        self.usernumber = 0
        self.comment = ""

    #method returns the XML format of a post
    def toXML(self):
        return '<utt uid="' + str(self.usernumber) + '">' + self.comment + '</utt>'

    def parsePost(self, postBody, users):
        #pars is a list of paragraph tags for a particular post
        pars = postBody.find_all('p')
        text = ""
        for p in pars:
            tmp = p.get_text().rstrip('\n')
            if tmp != '':
                tmp += ' '
            self.comment += tmp

        self.comment = self.comment[0:len(self.comment)-1]

        lines = str(postBody).split('\n')
        user = ""
        for line in lines:
            if line[9:16] == 'usr_adm': #usr_adm is the tag used for the current users post
                user = line[17:].partition('"')[0] #retrieves the username from the ine
                break;

        #get the userID number
        for pos,current in enumerate(users):
            if current == user:
                self.usernumber = pos
                return self

        #if we have not encountered the user before, add him to the list of users
        #userID is the next available number
        self.usernumber = len(users)
        users.append(user)
        return self

#using list comparisons to get the URLs on each page
def get_urls(soup):
    return [a.attrs.get('href') for a in soup.select('div b a[href^=/ShowTopic]')]

def main(outfilename):
    #to return URLs of discussion topics in a list, from a page
    f = open(outfilename, 'w')
    f.write('<dialog>')
    root_url = 'https://www.tripadvisor.fr/'
    index_url = root_url + 'ShowForum-g187070-i12-France.html'

    r = urllib.urlopen(index_url)
    soup = BeautifulSoup(r, 'html.parser')
    for _ in range(0,1000):
        elements = get_urls(soup)
        for element in elements:
            thread = Thread('https://www.tripadvisor.fr', root_url + element)
            f.write(thread.parsePages().encode('utf-8'))

        firstpage = False
        #guiArw sprite-pageNext is the arrow to which contains a link to the next page
        pagenext = soup.find('a',class_='guiArw sprite-pageNext')
        #If there are no more pages in the thread we are finished
        if pagenext != None:
            pagelink = pagenext.attrs['href'] #retrieves link to next pagenext
            r = urllib.urlopen('https://www.tripadvisor.fr' + pagelink) #half to include the prefix because link only includes everythign after
            soup = BeautifulSoup(r, 'html.parser')
        else:
            break #terminate when we don't have any other pages to investigate

    f.write("</dialog>")
    f.close()


if __name__ == '__main__':
    #command line should be the output file name
    main(sys.argv[1])
