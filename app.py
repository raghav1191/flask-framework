from flask import Flask, render_template, request, redirect
import requests
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/getstockinfo')
def getstockinfo():
  return render_template('getstockinfo.html')


@app.route('/result',methods = ['POST'])
def result():
      result = request.form.to_dict(flat=False)
      ticker = (result['ticker'][0])
      metric = (result['metric'][0])
      apikey = '3142324324324'
      url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=%s&apikey=%s' % (ticker, apikey)
      r = requests.get(url)
      data = r.json()
      timeseries = data['Weekly Time Series']
      df = pd.DataFrame.from_dict(timeseries, orient='index')
      a = ''
      if metric == '1':
        a = df['1. open']
      elif metric == '2':
        a = df['2. high']
      elif metric == '3':
        a = df['3. low']
      else:
        a = df['4. close']
      
      plt.plot(a)
      plt.savefig('static/images/plot.png')

      return render_template('result.html', url ='static/images/plot.png')

if __name__ == '__main__':
  app.run(port=33507, debug=True)
