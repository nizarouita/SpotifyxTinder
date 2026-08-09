from KNN import Knn
from songs import Song
from data import Data

s1= Song('6DCZcSspjsKoFjzjrWoCdn',	'Drake',	'Scorpion', "God's Plan")
s2= Song('7MXVkk9YMctZqd1Srtv4MB',	'The Weeknd;Daft Punk',	'Starboy',	'Starboy'	)
s3= Song('1DIXPcTDzTj8ZMHt3PDt8p',	'Coolio;L.V.',	"Gangsta's Paradise",	"Gangsta's Paradise"	)
s4= Song('2hETkH7cOfqmz3LqZDHZf5',	'Cesária Evora',	'Miss Perfumado',	'Barbincor')
taste = [s1, s3]
K=Knn(taste)
K.pick_songs()
L1=[]
L2=[]
for s in K.primary:
    L1.append(s.name)
for s in K.secondary:
    L2.append(s.name)

print(L1,L2)


