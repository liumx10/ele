import requests 
import json

def get_shop():
	r = requests.get('http://115.159.159.158:9200/hackathon/restaurant/_search')
	res = json.loads(r.text)
	size = res['hits']['total']

	r = requests.get('http://115.159.159.158:9200/hackathon/restaurant/_search?from=0&size='+str(size))
	return json.loads(r.text)

def get_menu(restaurant_id):
	r = requests.get('http://115.159.159.158:9200/hackathon/menu/_search?size=100000&q=_id:'+str(restaurant_id))
	res = json.loads(r.text)
	size = res['hits']['total']

	r = requests.get('http://115.159.159.158:9200/hackathon/menu/_search?from=0&size='+str(size))
	return json.loads(r.text)

def get_order(restaurant_id):
	baseurl  = "http://115.159.159.158:9200/hackathon/order/_search?q=restaurant_id:"+str(restaurant_id)
	r = requests.get(baseurl)
	res = json.loads(r.text)
	size = res['hits']['total']

	r = requests.get(baseurl+"&from=0&size="+str(size))
	return json.loads(r.text)

def main():
	shop = []
	menu = []
	order = []

	#shop = get_shop()
	#menu = get_menu()
	order = get_order(456941)

	print "========= shop number =========="
	print len(shop['hits']['hits'])
	print "========= menu number =========="
	print len(menu['hits']['hits'])
	print "========= order number ========="
	print len(order['hits']['hits'])


if __name__ == "__main__":
	main()