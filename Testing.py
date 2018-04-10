import indianexpress
from itertools import combinations

# qlist = ['shudra', 'dalit', 'untouchable', 'sc',
# 	'st','obc', 'lower+caste', 'minorities', 'backward class', 'tribal', 
# 	'adivasi', 'upper caste', 'brahmin', 'kshatriya', 'vaishya','government', 
# 	'democracy', 'election', 'college', 'education', 'scholar', 'merit', 'meritorious', 
# 	'employer', 'national', 'international', 'rich']

qlist = ["irfan","khan","blackmail", "movie", "review"]

for i in range(len(qlist)):
	qlist[i] = ("+".join(qlist[i].split(" "))).lower()

for query in combinations(qlist,3):
	indianexpress.main(query, "/home/ubuntu/BTC/Scrap/IE.csv")

"""
Other newspaper queries will be added soon
"""