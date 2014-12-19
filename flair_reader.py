import praw
from collections import defaultdict

r = praw.Reddit('flair reader')
r.login()

thread = raw_input("Enter thread url: ")
thread = r.get_submission(thread)

flairers = defaultdict(lambda : 0,{})

all_flairs = {}

file = open('flairs.txt','r')
for x in file:
    all_flairs[x[x.find("\"")+1:x.find("\"")+x[x.find("\"")+1:].find("\"")+1]]=x
file.close()

def get_flair(comment):
	for rep in comment.replies:
		if(rep.body.find('[')<rep.body.find(']')):
			if(flairers[rep.author.name]==0):
				flairers[rep.author.name]=1
			else:
				flairers[rep.author.name]+=1
			return [rep.body[rep.body.find('['):rep.body.find(']')+1],rep.author.name]
	return None

thread.replace_more_comments(limit=None, threshold=0)

def print_flair_css(thread):
	for c in thread.comments:
		if(type(c)==praw.objects.MoreComments):
			print_flair_css(c)
		elif(c.author!=None):
			author = c.author.name
			flair = get_flair(c)
			if(flair!=None):
				string= '.commentarea .author[href$="'+author+'"]:after{content:" '+flair[0]+'"}\n'
				all_flairs[author]=string

print_flair_css(thread)

for key in all_flairs.keys():
    print(all_flairs[key]),

print('________')

total = 0

for k in flairers.keys():
	print (k + " flaired " + str(flairers[k]) + " people.")
	total += flairers[k]

print "Total flaired: " + str(total)
