## Basic country report

To start the program please run main.py. 

The result is .csv file containing basic info about European countries (region can
be changed in the config file).


* **Country name in English and native language**

* **Area and population**
* **Capital, official language(s), domain and time zone(s)**
  
  For countries that have more than one language and/or time zone, values are separated
  with "|".
* **Information if country is a member of the European Union**
  
  The regional block can be changed in the config file.
* **Distance from Poland in kilometers**
  
  Country can be changed in the config file.
* **Currency symbol, name and exchange rate to PLN**
  
  Currency we want the exchange rate for can be changed in the config file.
* **Timestamp**

API documentation:

[REST Countries](https://restcountries.eu/#api-endpoints-code)

[Coinbase Digital Currency](https://developers.coinbase.com/api/v2?shell#get-currencies)