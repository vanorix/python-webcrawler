import xmlrpc.client
import sys, getopt

def main(argv):
	url = ''
	deepness = 0
	term = ''

	try:
		opts, args = getopt.getopt(argv,"hu:d:t:",["url=","deepness=","term="])
	except getopt.GetoptError:
   		print('client.py -u <url> -d <deepness> -t <term>')
   		sys.exit(2)

	for opt, arg in opts:
	  	if opt == '-h':
	  		print('client.py -u <url> -d <deepness> -t <term>')
	  		sys.exit()
	  	elif opt in ("-u", "--url"):
	  		url = arg
	  	elif opt in ("-d", "--deepness"):
	  		deepness = arg
	  	elif opt in ("-t", "--term"):
	  		term = arg

	with xmlrpc.client.ServerProxy("http://localhost:3000/SOII") as proxy:
		print(proxy.putWork(url, deepness, term))

if __name__ == "__main__":
	main(sys.argv[1:])