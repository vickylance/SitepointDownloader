import mechanize
from bs4 import BeautifulSoup
import urllib2 
import cookielib

cook = cookielib.CookieJar()
br = mechanize.Browser()
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.set_cookiejar(cook)


response = br.open("https://www.sitepoint.com/premium/l/join?ref_source=premium&ref_medium=sign-in")
with open("test.html", "a") as myfile:
    myfile.write(response.read() )
br.select_form(predicate=lambda frm: 'id' in frm.attrs and frm.attrs['id'] == 'new_user')
br.form['user[login]'] = 'vkkpp@hotmail.com'
br.form['user[password]'] = 'Rayquaza555!'
br.submit()

with open("loggedin.html", "a") as myfile:
    myfile.write(br.response().read())

response = br.open("https://www.sitepoint.com/premium/?q=&limit=400&offset=0&page=1&content_types[]=Course&slugs[]=all&states[]=available&order=")
with open("test2.html", "a") as myfile:
    myfile.write(response.read() )