from backend.main_algo import Knn
from songs import Song
from data import Data

s1= Song('6DCZcSspjsKoFjzjrWoCdn',	'Drake',	'Scorpion', "God's Plan")
s2= Song('3F5CgOj3wFlRv51JsHbxhe',	'Drake;21 Savage',	'Honestly, Nevermind',	'Jimmy Cooks (feat. 21 Savage)')
s3= Song('68Dni7IE4VyPkTOH9mRWHr',	'J. Cole',	'2014 Forest Hills Drive',	'No Role Modelz')
s4= Song('40iJIUlhi6renaREYGeIDS',	'Drake;Travis Scott',	'Certified Lover Boy',	'Fair Trade (with Travis Scott)'	)
taste = [s1, s3, s2, s4]
K=Knn(taste)
K.pick_songs()
#L1=[]
# L2=[]
# L3=[]
# for s in K.primary:
#     L1.append(s.name)
# for s in K.secondary:
#     L2.append(s.name)
# for s in K.secondary:
#     L3.append(s.name)

# print(L1,L2, L3)
print(K.primary)

