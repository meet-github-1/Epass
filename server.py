from flask import Flask, render_template, request
from twilio.rest import Client
import requests
account_sid = 'AC50454e30f2fbbffa7107d7cc23afab66'
auth_token = '54377b935128aebc5ab6fbb4dfb49bd4'
client = Client(account_sid,auth_token)
app = Flask(__name__, static_url_path='/static')
@app.route('/')
def registration_form():
    return render_template('homepage.html')

@app.route('/login_page',methods=['POST', 'GET'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest-state']
    destination_dt = request.form['destination']
    phoneNumer = request.form['phoneNumber']
    id_proof = request.form['idcard']
    date = request.form['trip']
    full_name = first_name + "." + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt/pop) * 100)
    if travel_pass < 30 and request.method == 'POST':
        status ='CONFIRMED'
        client.messages.create(to="(91)"+phoneNumer,
                               from_='(678) 841-7149',
                               body="Hello "+" "+full_name+" "+"Your Travel From" +" "+source_dt+" "+"To"+" "+destination_dt+" "
                               +"Has "+status+" On "+date+", Apply later")
        return render_template('status.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumer, var8=date, var9=status)
    else:
        status = 'NOT CONFIRMED'
        client.messages.create(to="(91)"+phoneNumer,
                               from_='(678) 841-7149',
                             body="Hello " + " " + full_name + " " + "Your Travel From" + " " + source_dt + " " + "To" + " " + destination_dt + " "
                         + "Has " + status + " On " + date + ", Apply later")
        return render_template('status.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumer, var8=date, var9=status)

if __name__ == "__main__":
    print("hello manmeet")
    app.run(port=5000,debug=True)