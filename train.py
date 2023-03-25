import requests
from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)


db = mysql.connector.connect(host='localhost', user='root', password='',database='train')
cursor = db.cursor()

@app.route('/create_table',methods=['GET','POST'])
def createTable():
    createQuery = 'create table trains(train_id VARCHAR(20) PRIMARY KEY NOT NULL, train_name VARCHAR(50) NOT NULL, from_station VARCHAR(50) NOT NULL, to_station VARCHAR(50) NOT NULL, date_running VARCHAR(50) NOT NULL, arrival_time FLOAT(10) NOT NULL, departure_time FLOAT(10) NOT NULL, seats_remaining int, reaching_time FLOAT, day_running VARCHAR(60))'
    cursor.execute(createQuery)
    db.commit()
    foreignQuery = 'create table status(train_id VARCHAR(50) NOT NULL, train_name VARCHAR(50) NOT NULL, date_running VARCHAR(50) NOT NULL, running_via VARCHAR(90), FOREIGN KEY (train_id) REFERENCES trains(train_id))'
    cursor.execute(foreignQuery)
    db.commit()
    return("<div style='color:green;text-align:center;font-size: 46px;padding: 40vh 0 0 0'><b>Table created successfully</b></div>")



@app.route('/insert_data',methods=['GET','POST'])
def insertTable():
    insertQuery = 'insert into trains values ("A1234","Netravathi Express","KLM","ALP","22-01-2022",10.55,11.05,20,03.30,"monday"),' \
                  '("A5678","Amaravathi Express","KLM","KTM","23-01-2022",11.55,12.05,60,01.30,"tuesday"),' \
                  '("A9810","Kurla Express","KLM","IDUKKI","22-01-2022",12.55,01.05,80,04.30,"monday")'
    cursor.execute(insertQuery)
    db.commit()
    statusQuery = 'insert into status values ("A1234","Netravathi Express","22-01-2022","KLM PTA ALP"),' \
                  '("A5678","Amaravathi Express","23-01-2022","KLM PTA KTM ALP"),' \
                  '("A9810","Kurla Express","22-01-2022","KLM PTA KTM ALP IDK")'
    cursor.execute(statusQuery)
    db.commit()
    return("<div style='color:green;text-align:center;font-size: 46px;padding: 40vh 0 0 0'><b>Values inserted successfully</b></div>")


@app.route('/getstatus',methods=['GET','POST'])
def status():
    source = request.args.get('source').upper()
    desn = request.args.get('destination').upper()
    dat = request.args.get('date')
    lsDate = []
    trainName = []
    lsDate.append(dat)
    runningQuery = 'select train_id, running_via from status where date_running = %s'
    cursor.execute(runningQuery,lsDate)
    statusRecord = cursor.fetchall()
    for i in range(len(statusRecord)):
        if (source in statusRecord[i][1]) and (desn in statusRecord[i][1]):
            trainName.append(statusRecord[i][0])
    attach = ', '.join(['%s'] * len(trainName))
    fetchQuery = f'select train_id, train_name, from_station, to_station, arrival_time, departure_time, seats_remaining from trains where train_id IN ({attach})'
    cursor.execute(fetchQuery,trainName)
    record = cursor.fetchall()
    display_ls = [{'Train ID': records[0], 'Train Name' : records[1], 'Source' : records[2] , 'Destination' : records[3],
                   'Arrive at': records[4],'Leave at': records[5],'No. of seats' : str(records[6])} for records in record]
    return jsonify(display_ls)


if __name__ =='__main__':
    app.run(debug=True)