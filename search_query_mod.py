def search_query(keyword):
    from bs4 import BeautifulSoup
    import requests
    search_qurey=str(keyword)
    url_template="https://www.1mg.com/search/all?name="+search_qurey
    print(url_template)
    temp=requests.get(url_template)
    temp.status_code
    soup=BeautifulSoup(temp.content,"html.parser")
    h=soup.find_all('div',class_="style__horizontal-card___1Zwmt")
    try:
        l=[]
        for i in h:
            links = i.findAll('a')
            for a in links:
                l.append(a['href'])        
        l[0]
        basedir='https://www.1mg.com'
        final_url=basedir+l[0]
        print(final_url)
        detail_page=requests.get(final_url)
        detail=BeautifulSoup(detail_page.content,'html.parser')
        g=[]
        for row in detail.find_all('div',class_='bodyRegular'):
                print(row.text)
                g.append(row.text)
        g[0]
        return g
      
    except IndexError:
        h=soup.find_all('div',class_="style__product-box___3oEU6")
        l=[]
        for i in h:
            links = i.findAll('a')
            for a in links:
                l.append(a['href'])        
        l[0]
        basedir='https://www.1mg.com'
        final_url=basedir+l[0]
        print(final_url)
        detail_page=requests.get(final_url)
        detail=BeautifulSoup(detail_page.content,'html.parser')
        g=[]
        for row in detail.find_all('div',class_='pNormal marginTop-8'):
                print(row.text)
                g.append(row.text)
        g[0]
        return g

