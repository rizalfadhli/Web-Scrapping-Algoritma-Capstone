from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url = 'https://www.exchange-rates.org/history/IDR/USD/T' 
url_get = requests.get(url, headers = { 'User-Agent': 'Popular browser\'s user-agent', })
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs = {'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')

row_length = len(tr)

temp = [] #initiating a tuple

for i in range(1, len(tr)):
    row = table.find_all('tr')[i]
    
    #get date
    date = row.find_all('td')[0].text
    date = date.strip() #for removing the excess whitespace
    
    #get price
    price = row.find_all('td')[2].text
    price = price.strip() #for removing the excess whitespace
    
    temp.append((date,price)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date', 'price'))

#insert data wrangling here
df['date'] = df['date'].astype('datetime64')
df['price'] = df['price'].str.replace(',','')
df['price'] = df['price'].str.replace(' IDR','')
df['price'] = df['price'].astype('float')
df = df.set_index('date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["price"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = ____.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)