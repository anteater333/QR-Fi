from flask import Flask, render_template, redirect, url_for, request
import qrcode

app = Flask(__name__)
temp=''

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        ssid = request.form['ssid']
        global temp
        temp = ssid
        password = request.form['password']
        protocol = request.form['protocol']
        
        qr = qrcode.make(F'WIFI:S:{ssid};T:{protocol};P:{password};;')
        qr.save("./static/qr.png")

        return redirect(url_for('result'))
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html', image_file='static/qr.png', name=temp)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run()