daftar = open('Machine LearningUnsupervised Learning Part 2 of 3.txt','r')
daftar_link = open('../ml_unsupervised_link.txt','wb')
for d in daftar:
	daftar_link.write("http://"+d.split("\t")[1]+"\n")