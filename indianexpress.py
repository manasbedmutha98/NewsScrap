from bs4 import BeautifulSoup
import requests
import csv

def retrieve(field, soup):

	if(field.lower() ==("time")):
		ans = soup.find("meta",  property="article:published_time")
		if(ans!=None):
			return ans["content"].strip().replace("\n","\t")
		else:
			return "NA"

	if(field.lower() ==("language")):
		ans = soup.find('meta', itemprop="inLanguage")
		if(ans!=None):
			return ans["content"].strip().replace("\n","\t")
		else:
			return "NA"
		
	if(field.lower() ==("newskeywords")):
		ans = soup.find("meta", attrs={'name':'news_keywords'})
		if(ans!=None):
			return ans["content"].strip().replace("\n","\t")
		else:
			return "NA"

	if(field.lower() ==("keywords")):
		ans = soup.find("meta", attrs={'name':'keywords'})
		if(ans!=None):
			return ans["content"].strip().replace("\n","\t")
		else:
			return "NA"

	if(field.lower() ==("author")):
		ans = soup.find('meta', itemprop="author")
		if(ans!=None):
			return ans["content"].strip().replace("\n","\t")
		else:
			return "NA"

	if(field.lower() ==("headline")):
		ans = soup.find("meta",  property="og:title")
		if(ans!=None):
			return ans["content"].strip().replace("\n","\t")
		else:
			return "NA"

	if(field.lower() ==("synopsis")):
		ans = soup.find("meta",  property="og:description")
		if(ans!=None):
			return ans["content"].strip().replace("\n","\t")
		else:
			return "NA"

	if(field.lower() ==("coverpic")):
		ans = soup.find("meta",  property="og:image")
		if(ans!=None):
			return ans["content"].strip().replace("\n","\t")
		else:
			return "NA"

	if(field.lower() ==("body")):
		ans = soup.find('div', attrs={'class': 'full-details'})
		return ans
			

def getdata(url):
	Data = []
	r  = requests.get(url)
	data = r.text

	soup = BeautifulSoup(data,"lxml")
	
	Time = retrieve("time",soup)
	Language = retrieve("Language",soup)
	NewsKeywords = retrieve("NewsKeywords",soup)
	Keywords = retrieve("Keywords",soup)
	Author = retrieve("author",soup)
	Headline = retrieve("headline",soup)
	Synopsis = retrieve("synopsis",soup)
	CoverPic = retrieve("coverpic",soup)
	#print(Time," * ",Language," * ", Author," * ", Headline," * ", Synopsis," * ",CoverPic,"*",Keywords,"*",NewsKeywords, " 8 ",url )
	Comments = "NA1"
	try:
		for each_div in soup.findAll('div',{'class':'comment-body'}):
			Commenter = each_div.find('div', attrs={'class': 'commenter-name'}).text
			CommentTime = each_div.find('div', attrs={'class': 'datetime'}).text
			CommentText = each_div.find('div', attrs={'class': 'comment-content'}).text
			CommentFull = "["+Commenter+", "+CommentTime+", "+CommentText+"]"
			Comments = Comments+";"+CommentFull
	except:
		 Comments = "NA"
	
	
	Body = retrieve("body",soup)
	if(Body):
		body = ""
		for each_div in Body.findAll('p'):
			body = body + " "+ (each_div.getText()).replace("\n"," ")

		body = body.replace("\n"," ")
		#print(len(body))
		#print(type(NewsKeywords))
	else:
		body = "NA"


	Article = [sitename, Headline, url, Author, Synopsis, 
	CoverPic, NewsKeywords, Keywords, body, Comments]
	#print (Article)
	Data = "~".join(Article)
	print("\nNext")
	
	return Data

def main (queryIn, loc):
	global sitename
	sitename = "Indian Express"
	print(sitename)
	#query =["IIT","Gandhinagar"]
	query = "+".join(queryIn).lower()
	url = "indianexpress.com/?s="+query
	print (url)
	r  = requests.get("http://" +url)
	data = r.text
	MainSoup = BeautifulSoup(data,"lxml")

	SearchRetr = MainSoup.find('div', attrs={'class': 'search-result'})

	TotalArticles = (SearchRetr.find('h6').getText()).split()[-3]
	print("Found a total of "+TotalArticles+" articles.\n")

	#loc = "/home/ubuntu/BTC/IE.csv"


	for each_div in SearchRetr.findAll('div',{'class':'details'}):
		headline = each_div.find('p')
		ArticleLink = each_div.find('a', recursive = True)['href']
		print([query.replace("+",",")])
		Article = getdata(ArticleLink)+"~"+query.replace("+",",")+"\n"
		#print (Article)
		file = open(loc, "a")
		#out = csv.writer(file)
		file.write(Article)
		file.close()
		#file.write(Article)

	for i in range(2,int(TotalArticles)//16):
		url = ("indianexpress.com/page/"+str(i)+"/?s="+query).lower()
		print (url)

		r  = requests.get("http://" +url)
		data = r.text
		MainSoup = BeautifulSoup(data,"lxml")

		SearchRetr = MainSoup.find('div', attrs={'class': 'search-result'})

		for each_div in SearchRetr.findAll('div',{'class':'details'}):
			headline = each_div.find('p')
			ArticleLink = each_div.find('a', recursive = True)['href']
			Article = getdata(ArticleLink)+"~"+query.replace("+",",")+"\n"
			file = open(loc, "a")
			#out = csv.writer(file)
			file.write(Article)
			file.close()

		#print (i)
		
		#print(headline)
		#print (each_div.find('div', attrs={'class': 'synopsis'}).text)
	    #print (each_div.get('div',{'class':'synopsis'}).text)


