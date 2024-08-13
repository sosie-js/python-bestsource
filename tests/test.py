
look = {"a":"boo","Box":"yop","Flower":"yup"}

my_dict= {"Arc":"desc asc", "Box": "desc box","Flower":"desc flower"}
    
for l in look.keys():
    try :
        print(my_dict[l])
        break
    except KeyError as e:
    #
        #print(e)
        pass
