from flask import Flask, render_template, request

app = Flask(__name__)

def calculation(money, units_of_energy):
    price_per_unit = round(float(money) / float(units_of_energy), 2)
    price_per_solar = round((0.20 * float(units_of_energy)), 2)  # Assuming you want a float result
    return price_per_unit, price_per_solar

@app.route('/')
def index():
    return render_template('Web-Page.html')

@app.route('/result', methods=['POST'])
def result():
    bill = request.form.get('bill')
    energy = request.form.get('energy')
    price_per_unit, price_per_solar = calculation(bill, energy)
    return render_template('Web-Page.html', bill=bill, energy=energy, price_per_solar=price_per_solar, price_per_unit=price_per_unit)

if __name__ == '__main__':
    app.run(debug=True)
