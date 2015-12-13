import apriori
import getdata
import multiprocessing

def main():
    shop_set = set()
    data = getdata.get_shop()
    for shop in data["hits"]["hits"]:
        shop_set.add(shop["_id"])
    for shop_id in shop_set:
        print shop_id
        p = multiprocessing.Process(target=apriori.mineAssosiationRule,args=(shop_id,))
        p.start()
        p.join(10)
        if p.is_alive():
            print shop_id+"is killed."
            p.terminate()
            p.join()

if __name__ == '__main__':
    main()