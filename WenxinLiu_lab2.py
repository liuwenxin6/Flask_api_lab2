import csv
from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
csv_filename = "AAPL.csv"

lst = [*csv.DictReader(open(csv_filename))]
#print(lst)

app = Flask(__name__)

#GET METHODS:
@app.route('/getData/', methods = ['GET']) 
def getd():
    return lst

@app.route('/getData/<date>/', methods = ['GET']) #expects date format: YYYY-MM-DD
def getdatad(date):
    for k in lst:
        if k['Date'] == date:
            return k
    return None

@app.route('/calculate10DayAverage/', methods = ['GET']) #CONFIRM ABOUT THIS
def calculate10DayAverage():
    sum = 0
    total_len = len(lst)
    for k in range (9):
        cur = lst[total_len-k-1]
        sum += float(cur['Close'])
    return str(sum/10)

#POST METHODS:
@app.route('/getData/', methods = ['POST'])
def getData(): #expects date format: YYYY-MM-DD
    start_d = request.json['Start Date']
    start_dt = datetime.strptime(start_d, '%Y-%m-%d')
    end_d = request.json['End Date']
    end_dt = datetime.strptime(end_d, '%Y-%m-%d')
    ans_lis = []
    for k in lst:
        cur_dt = datetime.strptime(k['Date'], '%Y-%m-%d')
        if cur_dt>= start_dt and cur_dt <= end_dt:
            ans_lis.append(k)
    return ans_lis
# {    "Start Date" : "2016-12-25",    "End Date" : "2017-01-05" }

@app.route('/addData/', methods = ['POST'])
def addData():
    date_val = request.json['Date']
    open_val = request.json['Open']
    high_val = request.json['High']
    low_val = request.json['Low']
    close_val = request.json['Close']
    adj_close_val = request.json['Adj Close']
    vol_val = request.json['Volume']

    new_item = {'Date': date_val, 'Open': open_val, 'High': high_val, \
                'Low': low_val, 'Close': close_val, 'Adj Close': adj_close_val, \
                'Volume': vol_val}
    lst.append(new_item)
    return "successfully added: " + date_val


#PUT METHOD
@app.route('/updateData/', methods = ['PUT'])
def updateData(): #expects date format: YYYY-MM-DD
    date_val = request.json['Date']
    open_val = request.json['Open']
    high_val = request.json['High']
    low_val = request.json['Low']
    close_val = request.json['Close']
    adj_close_val = request.json['Adj Close']
    vol_val = request.json['Volume']
    for k in lst:
        if k['Date'] == date_val:
            k['Open'] = open_val
            k['High'] = high_val
            k['Low'] = low_val
            k['Close'] = close_val
            k['Adj Close'] = adj_close_val
            k['Volume'] = vol_val
            return "Updated successfully for:" + date_val
    return date_val+ " not found. Unable to update!"

#DELETE METHOD
@app.route('/deleteData/', methods = ['DELETE'])
def deleteData(): #expects date format: YYYY-MM-DD
    ddate = request.json['Delete Date']
    for k in lst:
        if k['Date'] == ddate:
            lst.remove(k)
            return "Deleted successfully for: " + ddate
    return ddate+ " not found. Unable to delete!"
# {    "Delete Date" : "2016-11-23"}

#{
#    "Date" : "2022-11-26",
#    "Open": "500", 
#    "High": "800",
#    "Low": "200", 
#    "Close": "405", 
#    "Adj Close": "900",
#    "Volume": "4444444444"
#}

if __name__ == '__main__':
    app.run(debug=True)
