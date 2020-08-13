def med_add(name,cur_med,db_med):
    from search_using_practo import med_practo
    import pymysql
    from fuzzywuzzy import fuzz
    # db_med = pymysql.connect(host="localhost",user="root",password="12345",db="user_info")
    # cur_med= db_med.cursor()
    cur_med.execute("SELECT medName,med_id,MATCH (medName,description) AGAINST (%s) as score from med_info WHERE MATCH (medName,description) AGAINST (%s) ORDER BY score DESC",(name,name))
    p=cur_med.fetchone()
    try:
        
        if p is None:
            (medName,description,sideEffects,uses,dosage,substitutes)=med_practo(name)
            query="INSERT INTO med_info (medName,description,sideEffects,uses,dosage,substitutes) VALUES ('%s','%s','%s','%s','%s','%s')"%(medName,description,sideEffects,uses,dosage,substitutes)
            cur_med.execute(query)
            #cur.execute(query,q)
            db_med.commit()
            print("medicine added From None found block to database",name)
            cur_med.execute("SELECT med_id from med_info where medName=%s",medName)
            ID=cur_med.fetchone()
            return ID[0]
        elif p is not None:
            temp=p[0]
            matp=fuzz.partial_ratio(name.lower(),temp.lower())
            matt=fuzz.ratio(name.lower(),temp.lower())
            matr=fuzz.token_sort_ratio(name.lower(),temp.lower())
            if (matp>70 and matt>55 and matr>50):
                print("med present",temp)
                return p[1]
            else:
                print("in else block of add medicine if not found")
                (medName,description,sideEffects,uses,dosage,substitutes)=med_practo(name)
                query="INSERT INTO med_info (medName,description,sideEffects,uses,dosage,substitutes) VALUES ('%s','%s','%s','%s','%s','%s')"%(medName,description,sideEffects,uses,dosage,substitutes)
                cur_med.execute(query)
                #cur.execute(query,q)
                db_med.commit()
                print("medicine added from found block to database "+ name +" -> "+medName)
                cur_med.execute("SELECT med_id from med_info where medName=%s",medName)
                ID=cur_med.fetchone()
                return ID[0]
        else:
            
            print("execcuted successfully whole block")
            return None
    except:
        print("fetched data from database",p)
        print("Error in Running")
        return None
    
