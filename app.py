from flask import Flask, render_template, request

app = Flask(__name__)

tradition_energy_price = 12.5
solar_energy_price = 5
solar_panel_price = 50000

def calculation(money):
    units_of_energy = round(float(money) / tradition_energy_price, 2)
    price_using_solar = round(units_of_energy * solar_energy_price, 2)
    saving = float(money) - price_using_solar
    return price_using_solar, saving

def solar_panel(savings):
    months = round(solar_panel_price / savings)
    days = round(months * 30)

    if months == 0 and days == 0:
        return 1, 30

    return months, days

def investment(savings, planning_years, months_to_pay_for_panel):
    totalMonths = planning_years * 12
    monthsEarning = totalMonths - months_to_pay_for_panel
    totalMonths_Earning = monthsEarning * savings
    earning_without_maintainance = monthsEarning * savings
    earning_with_maintainance = earning_without_maintainance - 1000

    total_saving = savings * totalMonths

    return totalMonths, monthsEarning, totalMonths_Earning, earning_without_maintainance, earning_with_maintainance, total_saving

@app.route('/')
def index():
    return render_template('Web-Page.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        bill = request.form.get('bill')
        
        if bill:
            bill = round(float(bill), 2)
        else:
            return render_template('Web-Page.html')

        price_using_solar, savings = calculation(bill)
        savings = round(savings, 2)
        months, days = solar_panel(savings)

        return render_template('Web-Page.html', bill=bill, price_using_solar=price_using_solar, savings=savings, months=months, days=days)
        
    except ValueError:
        return render_template('Web-Page.html')

@app.route('/result_investment', methods=['POST'])
def result_investment():
    try:
        bill = request.form.get('bill')
        planning_years = request.form.get('planning_years')

        if bill:
            bill = round(float(bill), 2)
        else:
            return render_template('Web-Page.html')

        if planning_years:
            planning_years = int(planning_years)

        price_using_solar, savings = calculation(bill)
        months, days = solar_panel(savings)

        totalMonths, monthsEarning, totalMonths_Earning, earning_without_maintainance, earning_with_maintainance, total_saving = investment(savings, planning_years, months)
        totalMonths, monthsEarning, totalMonths_Earning, earning_without_maintainance, earning_with_maintainance, total_saving = round(totalMonths), round(monthsEarning), round(totalMonths_Earning), round(earning_without_maintainance), round(earning_without_maintainance), round(total_saving)


        return render_template('Web-Page.html', bill=bill, price_using_solar=price_using_solar, savings=savings, months=months, days=days, planning_years=planning_years, totalMonths=totalMonths, monthsEarning=monthsEarning, totalMonths_Earning=totalMonths_Earning, earning_without_maintainance=earning_without_maintainance, earning_with_maintainance=earning_with_maintainance, total_saving = total_saving)
        
    except ValueError or TypeError:
        return render_template('Web-Page.html') 

if __name__ == '__main__':
    app.run(debug=True)
