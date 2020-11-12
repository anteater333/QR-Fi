from flask import Flask, render_template, redirect, url_for, request
import qrcode

app = Flask(__name__)
temp_ssid=''
temp_qr=''

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        ssid = request.form['ssid']
        global temp_ssid
        temp_ssid = ssid
        password = request.form['password']
        protocol = request.form['protocol']
        
        qr = qrcode.QRCode(version=12, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=6, border=4)
        qr.add_data(F'WIFI:S:{ssid};T:{protocol};P:{password};;')
        #qr = qrcode.make(F'WIFI:S:{ssid};T:{protocol};P:{password};;')
        #qr.save("./static/qr.png")
        qr.make()
        qr1 = qr.make_image(fill_color="#000000", back_color="#ffffff")
        qr1.save("./static/qr.png")
        global temp_qr
        temp_qr=qr

        return redirect(url_for('result'))
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        fill = request.form['fill_color']
        back = request.form['back_color']
        img = temp_qr.make_image(fill_color = fill, back_color = back)
        img.save("./static/qr.png")

        #return render_template('result.html', image_file='static/qr.png')
        return render_template('result.html', fill_color=fill, back_color=back, image_file='static/qr.png', name=temp_ssid)
    return render_template('result.html', image_file='static/qr.png', name=temp_ssid)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == "__main__":
    app.run()