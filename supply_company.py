import pymongo
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from bson.datetime_ms import datetime
from datetime import datetime as dtm
from collections import Counter
import matplotlib.pyplot as plt

class Supplement_Company():
    def __init__(self):
        
        myclient=pymongo.MongoClient("mongodb+srv://")
        mydb=myclient["sample_supplies"]
        mycollection=mydb["sales"]
        self.mycollection=mycollection

        while True:
            print("\nPlease Select Transaction:\n1-Store Locations List\n2-Total Revenue of Stores\n3-Satisfaction of Stores\n4-Bestsellers in The Company\n5-Top Earning Products\n6-Seasons")
            transaction=input("\nTransaction:")
            if transaction=="1":
                locations=self.Locations_list()
                print(locations)
            elif transaction=="2":
                self.total_revenue()
            elif transaction=="3":
                self.Satisfaction()
            elif transaction=="4":
                self.BestSeller()
            elif transaction=="5":
                self.Best_product()
            elif transaction=="6":
                self.seasons()
            elif transaction=="q":
                break
            else:
                print("Error, please try again.")

    def Locations_list(self):
        locations_list=[]
        unique_locations_list=[]
        for loc in self.mycollection.find():
            locations=loc["storeLocation"]
            locations_list.append(locations)
        unique_locations_list=list(set(locations_list))
        return unique_locations_list

    def total_revenue(self):
        liste=self.Locations_list()
        cities_list=[]
        for i in liste:
            seattle=self.mycollection.find({"storeLocation":i})
            toplam_seattle=0
            for dongu in seattle:
                items=dongu["items"]
                for dongu2 in items:
                    quantity=dongu2["quantity"]
                    price=float(str(dongu2["price"]))    
                    toplam_seattle+=quantity*price
            cities_list.append({i:toplam_seattle})
        sorted_list=sorted(cities_list, key= lambda x: list(x.values()),reverse=True)
        dollar_added_list = [{key:str(value)+" $" for key,value in d.items()} for d in sorted_list]
        for i in dollar_added_list:
            print(i)
        sorted_list.reverse()

        #CG
        city_revenues = {}
        for item in sorted_list:
            city_name = list(item.keys())[0]
            revenue_str = item[city_name]
            revenue = float(revenue_str)
            city_revenues[city_name] = revenue
        labels = list(city_revenues.keys())
        values = list(city_revenues.values())
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel('Şehirler')
        plt.ylabel('Milyon Gelir ($)')
        plt.title('Şehir Gelirleri')
        plt.xticks(rotation=45, ha='right')
        plt.ylim(60000,3000000)
        plt.tight_layout()
        plt.show()


    def Satisfaction(self):
        liste=self.Locations_list()
        cities_list=[]
        satisfaction_sum=0
        for i in liste:
            location=self.mycollection.find({"storeLocation":i})
            overall_average=0
            satisfaction_sum=0
            count=0
            for sorgu1 in location:
                satisfaction_all=sorgu1["customer"]["satisfaction"]
                satisfaction_sum+=int(satisfaction_all)
                count+=1
            overall_average=satisfaction_sum*2/count
            cities_list.append({i+f" ({count} customer)":overall_average})
        sorted_list=sorted(cities_list, key= lambda x: list(x.values()),reverse=True)
        percent_added_list = [{key:str(value)+" /10" for key,value in d.items()} for d in sorted_list]
        for i in percent_added_list:
            print(i)
        city_ratings = {}  # Şehirleri ve memnuniyet puanlarını saklayacağımız boş bir sözlük

        for item in percent_added_list:
            city_name = list(item.keys())[0]  # Sözlüğün anahtarını (şehir adını) alıyoruz
            rating_str = item[city_name].split()[0]  # Memnuniyet puanını alıyoruz
            rating = float(rating_str)  # String puanını float'a dönüştürüyoruz
            city_ratings[city_name] = rating  # Şehir adı ve puanını sözlüğe ekliyoruz

        labels = list(city_ratings.keys())
        values = list(city_ratings.values())

        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='green')
        plt.xlabel('Şehirler')
        plt.ylabel('Memnuniyet Oranı')
        plt.title('Şehirlerin Memnuniyet Oranları')
        plt.xticks(rotation=45, ha='right')
        plt.ylim(7,8)
        plt.tight_layout()
        plt.show()

    def BestSeller(self):
        product_list=[]
        list_bestseller=[]
        counter_products=Counter()
        all_data=self.mycollection.find({})
        for dongu in all_data:
            items=dongu["items"]
            for dongu2 in items:
                product_name=dongu2['name']
                quantity=dongu2['quantity']
            product_list.append((product_name,quantity))
        for names,quants in product_list:
            counter_products[names]+=quants
        list_bestseller=list(counter_products.items())
        sorted_list=sorted(list_bestseller, key = lambda x :x[1],reverse=True)
        for i in sorted_list:
            print(i)
        labels, values = zip(*list_bestseller)

        #CG
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, shadow=True)
        plt.axis('equal')

        plt.title('En Çok Satan Ürünler Pasta Grafiği')
        plt.show()
        # unique_product_list=list((set(product_list)))            
        # list_bestseller.append({eleman:product_list.count(eleman)*quantity})
        # count_product_list=list(set(x[0] for x in product_list if product_list.count(x)>0))   

    def Best_product(self):
        product_list=[]
        revenue_product_list=Counter()
        all_data=self.mycollection.find({})
        for dongu in all_data:
            items=dongu["items"]
            for dongu2 in items:
                sum_money=0
                product_name=dongu2["name"]
                quantity=dongu2["quantity"]
                price=float(str(dongu2["price"]))    
                sum_money+=quantity*price
            product_list.append({product_name:sum_money})
        for dict in product_list:
            for key,value in dict.items():
                revenue_product_list[key]+=value
        revenue_product_list=list(revenue_product_list.items())
        sorted_list=sorted(revenue_product_list, key = lambda x :x[1],reverse=True)
        # dollar_added_list = [(key,str(value)+" $") for key,value in sorted_list]
        # for i in dollar_added_list:
        #     print(i)
        
        revenue_product_list.reverse()
        labels, values = zip(*revenue_product_list)
        #CG

        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel('Ürünler')
        plt.ylabel('Satış Miktarı ($)')
        plt.title('Ürünlerin Satış Miktarına Göre Dağılımı (Bar Grafiği)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def date_and_time(self):
        product_list=[]
        list_date_product=[]
        list_date=[]
        clock_time=[]
        list_time_product=[]
        all_data=self.mycollection.find({})
        for dongu in all_data:
            date=dongu["saleDate"]
            items=dongu["items"]
            date_time=datetime.datetime.strftime(date, '%d %B %Y')
            clock_time=datetime.datetime.strftime(date, '%H %M %S')
            for dongu2 in items:
                product_name=dongu2['name']
                quantity=dongu2["quantity"]
                product_list.append(product_name)
                list_date_product.append((date_time , product_name,quantity))
                list_time_product.append((clock_time , product_name,quantity))
        return list_date_product , list_time_product
    
    def seasons(self):
        dates,times=self.date_and_time()
        i=0
        counter_date_time=Counter()
        list_date_product=[]
        list_seasons=[]
        # months_list=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        # all_year_list=[]
        # unique_year_list=[]
        for index in dates:
            list_date_product.append((index[0][3:6],int(index[0][-4:]),index[1],index[2]))
        for month,year,name,quantity in list_date_product:
            # all_year_list.append(year)
            # unique_year_list=sorted(set(all_year_list), key=lambda x: x)
            i+=1
            counter_date_time[month+" "+f"{year}"]+=(int(len(name)/len(name)))*quantity

            list_seasons=list(counter_date_time.items())
        # sorted_counter_date_time=sorted(list_seasons[0:2], key=lambda x : months_list.index(x[0])) # sorted_counter_date_time=sorted(counter_date_time.items(),key=lambda x: x[1])
        sorted_data = sorted(list_seasons, key=lambda x: dtm.strptime(x[0], "%b %Y"))

        #CG
        months = [item[0] for item in sorted_data]
        years = [item[1] for item in sorted_data]
        # Grafik çizdirme
        plt.figure(figsize=(15, 7))
        plt.plot(months, years, marker='o', color='red', label='Satışlar',linewidth=3.5)
        plt.xlabel('Yıl-Ay')
        plt.ylabel('Satışlar')
        plt.title('Satışların Ay ve Yıllara Göre Grafiği')
        plt.xticks(rotation=60)
        plt.tight_layout()
        plt.legend()
        plt.show()



        # print(sorted_counter_date_time)
Supplement_Company()

