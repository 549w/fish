import jieba.posseg as pseg
def seperate(words):
	results = []
	sep = pseg.cut(words)
	for i in sep:
		results.append(i.word)
	return results		
def pick_word(words, word_type):
	results = []
	divide = pseg.cut(words)
	for d in divide:
		if d.flag == word_type:
			results.append(d.word)
	return results