import indianexpress
from itertools import combinations

for query in combinations(['shudra', 'dalit', 'untouchable', 'sc',
	'st','obc', 'lower+caste', 'minorities', 'backward class', 'tribal', 'adivasi'],3):
	indianexpress.main(query, "/home/ubuntu/BTC/Scrap/IE.csv")