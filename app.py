from flask import Flask, render_template, request
from datetime import datetime, timedelta
from calculation import calculate

app = Flask(__name__)

# Pre-existing route for index.html and table.html
@app.route("/", methods=["GET", "POST"])
def index():
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November",
        12: "December"
    }


    if request.method == "POST":
        sol_id = request.form["sol"].zfill(4)
        branch = request.form["branch"]
        region = request.form['region']
        month = int(request.form["month"])
        year = int(request.form["year"])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        first_day_of_month = datetime(year, month, 1).strftime("%d/%b/%Y")
        last_day_of_month = (datetime(year, month+1, 1) - timedelta(days=1)).strftime("%d/%b/%Y")
        place = request.form["place"]
        month_text = month_names[month]


        if int(month) >= 4:
            prev_year = year
            prev_to_prev_year = year - 1
        else:
            prev_year = year - 1
            prev_to_prev_year = year - 2

        # Define BACID data
        bacid_data = {
            '1640': 'XXXX0054511004',
            '1610': 'XXXX0054301001',
            '1460': 'XXXX0052601001',
            '1650': '',
            '1660': 'XXXX0054561004',
            '1630': 'XXXX0054501003',
            '1430': 'XXXX0052501008',
            '1550': 'XXXX0054201001',
            '1580': 'XXXX0054201007',
        }

        # Modify BACID values
        modified_bacid_data = {
            code: (sol_id + bacid[4:]) if bacid else ''
            for code, bacid in bacid_data.items()
            }

        return render_template("table.html", date=date, sol_id=sol_id, branch=branch,
                               region=region, place=place, month=month_text, year=year,
                               prev_year=prev_year, prev_to_prev_year=prev_to_prev_year,
                               bacid_data=modified_bacid_data, first_day_of_month=first_day_of_month,
                               last_day_of_month=last_day_of_month)

    return render_template("index.html")

@app.route("/statement", methods=["GET", "POST"])
def table():

    month = request.form.get('month')
  
    data = request.form.to_dict()
    
    results = calculate(data, month)

    justification = " ✦ ".join(value for key, value in data.items() if key.endswith("_justification"))

    return render_template("result.html", data=data, calculated_data=results,
                           justification=justification)


if __name__ == "__main__":
    app.run(debug=True)
