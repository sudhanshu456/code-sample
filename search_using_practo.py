def med_practo(name):
    import requests
    import re
    import json
    import urllib.request, urllib.parse
    from lxml import html
    
    r=str(name)
    url="https://www.practo.com/practopedia/api/v1/search?query={}"
    entered_query_encode=urllib.parse.quote(r)
    final_url=url.format(entered_query_encode)
    connection=urllib.request.urlopen(final_url)
    connection.headers.get_content_charset()
    connection.getheaders()
    data=connection.read()
    js=json.loads(data)
    #print(json.dumps(js,indent=4))
    tp=js[0]['drug']['sub_type']
    print(tp)

    
    if tp=="drug":
        #for Drug type
        final_url='https://www.practo.com/medicine-info/'+ js[0]["drug"]["slug"]
        print(final_url)
        print("Medicine Info")
        r=requests.get(final_url)
        byte_data=r.content
        source_code=html.fromstring(byte_data)
        tree=source_code.xpath('/html/head/script[5]')


        gh=tree[0].text

        #def remove_control_chart(s):
        #   return re.sub(r'\\x..', '', s)
        #fg=remove_control_chart(gh)
        #fg.replace(u'\xa0', ' ').encode('utf-8')
        fgg=gh[25:]
        y=json.loads(fgg)
        medname=y["product_reducer"]["brand"]["name"]
        description=y["product_reducer"]["brand"]["description"]
        sideEffects=""
        subsitutes=""
        indications=""
        contraIndications=""
        dosage=""
        for i in range(len(y["product_reducer"]["brand"]["sideEffects"]["listText"])):
            #print("side effects: ",y["product_reducer"]["brand"]["sideEffects"]["listText"][i]["text"])
            sideEffects+=y["product_reducer"]["brand"]["sideEffects"]["listText"][i]["text"]+'\n'



        for i in range(len(y["product_reducer"]["brand"]["substitutes"])):
            #print("Subsitutes: ",y["product_reducer"]["brand"]["substitutes"][i]["sku_name"])
            subsitutes+=y["product_reducer"]["brand"]["substitutes"][i]["sku_name"]+'\n'



        for i in range(len(y["product_reducer"]["brand"]["indications"])):
            #print("Uses:",y["product_reducer"]["brand"]["indications"][i]["name"])
            #print("descriptions: ",y["product_reducer"]["brand"]["indications"][i]["description"])
            indications+= y["product_reducer"]["brand"]["indications"][i]["name"]+'\n'
            indications+=y["product_reducer"]["brand"]["indications"][i]["description"]+"\n"



        for i in range(len(y["product_reducer"]["brand"]["contraIndications"]["listText"])):
            #print("ContraIndications : ",y["product_reducer"]["brand"]["contraIndications"]["listText"][i]["text"])
            #print("description of ContraIndication : ",y["product_reducer"]["brand"]["contraIndications"]["listText"][i]["description"])
            contraIndications+=y["product_reducer"]["brand"]["contraIndications"]["listText"][i]["text"]+'\n'
            contraIndications+=y["product_reducer"]["brand"]["contraIndications"]["listText"][i]["description"]+'\n'


        for i in range(len(y["product_reducer"]["brand"]["dosage"])):
            #print("Dosages : ",y["product_reducer"]["brand"]["dosage"][i]["type"])
            #print("description about doasges :",y["product_reducer"]["brand"]["dosage"][i]["text"])
            dosage+=y["product_reducer"]["brand"]["dosage"][i]["type"]+"\n"
            dosage+=y["product_reducer"]["brand"]["dosage"][i]["text"]+"\n"




        if subsitutes=="":
            subsitutes+="Not Defined"+"\n"
        else:
            pass
        if dosage=="":
            dosage+="Not Defined"+"\n"


        print("proper executed drug product part")
        medname=medname.translate(str.maketrans({"'":"","-":" "}))
        description=description.translate(str.maketrans({"'":"","-":" "}))
        sideEffects=sideEffects.translate(str.maketrans({"'":"","-":" "}))
        indications=indications.translate(str.maketrans({"'":"","-":" "}))
        dosage=dosage.translate(str.maketrans({"'":"","-":" "}))
        subsitutes=subsitutes.translate(str.maketrans({"'":"","-":" "}))
        return (medname,description,sideEffects,indications,dosage,subsitutes)


    
    elif tp=="general_product":
        final_url='https://www.practo.com/health-products/{}/p'.format(js[0]["drug"]["slug"])
        print(final_url)
        print("health Product")
        r=requests.get(final_url)
        byte_data=r.content
        source_code=html.fromstring(byte_data)
        tree=source_code.xpath('/html/head/script[4]')
        gh=tree[0].text
        fgg=gh[25:]
        y=json.loads(fgg)
        medname=y["health_product_state"]["health_product"]["product_name"]
        description=""
        sideEffects="Not Defined"
        subsitutes=""
        uses=""
        dosage=""

    #product section
        
        for i in range(len(y["health_product_state"]["health_product"]["health_product_sections"])):

            if y["health_product_state"]["health_product"]["health_product_sections"][i]["title"]=="Description":
                description+=y["health_product_state"]["health_product"]["health_product_sections"][i]["section_description"]+"\n"
            elif y["health_product_state"]["health_product"]["health_product_sections"][i]["title"]=="Dosage" or y["health_product_state"]["health_product"]["health_product_sections"][i]["title"]=="How to use":
                dosage+=y["health_product_state"]["health_product"]["health_product_sections"][i]["section_description"] + "\n"
            elif y["health_product_state"]["health_product"]["health_product_sections"][i]["title"]=="Ingredients":
                try:
                    for j in range(len(y["health_product_state"]["health_product"]["health_product_sections"][i]["text_list"])):
                        subsitutes+=y["health_product_state"]["health_product"]["health_product_sections"][i]["text_list"][j]["text"]+"\n"    #ingredient
                except:
                    subsitutes+=y["health_product_state"]["health_product"]["health_product_sections"][i]["section_description"]+"\n"      #if nots lis
            elif y["health_product_state"]["health_product"]["health_product_sections"][i]["title"]==("Directions for use" or "How to use"):
                uses+=y["health_product_state"]["health_product"]["health_product_sections"][i]['section_description']+"\n"
                
            
        
        for i in range(len(y["health_product_state"]["health_product"]["health_product_highlights"])):
            uses+=y["health_product_state"]["health_product"]["health_product_highlights"][i]['highlight'] +"\n"  #highlight

##        try:
##            
##            for i in range(len(y["health_product_state"]["health_product"]["health_product_sections"][1]["text_list"])):
##                subsitutes+=y["health_product_state"]["health_product"]["health_product_sections"][1]["text_list"][i]["text"]+"\n"    #ingredient
##        except:
##            subsitutes+=y["health_product_state"]["health_product"]["health_product_sections"][1]["section_description"]+"\n"      #if nots list
##
        if subsitutes=="":
            subsitutes+="Not Defined"+"\n"
        else:
            pass
        
        if dosage=="":
            dosage+="Not Defined"+"\n"

        print("executed health product part")
        medname=medname.translate(str.maketrans({"'":"","-":" "}))
        description=description.translate(str.maketrans({"'":"","-":" "}))
        sideEffects=sideEffects.translate(str.maketrans({"'":"","-":" "}))
        uses=uses.translate(str.maketrans({"'":"","-":" "}))
        dosage=dosage.translate(str.maketrans({"'":"","-":" "}))
        subsitutes=subsitutes.translate(str.maketrans({"'":"","-":" "}))
        return (medname,description,sideEffects,uses,dosage,subsitutes)
    else:
        print("else part")
        return




















        
