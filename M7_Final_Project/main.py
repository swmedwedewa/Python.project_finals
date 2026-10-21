from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Переменные (кг CO₂)
COEFFICIENTS = {
    "electricity_kwh": 0.45,
    "gas_m3": 1.9,
    "petrol_l": 2.31,
    "flight_km": 0.18,
    "meat_beef_kg": 13.5,
    "meat_chicken_kg": 3.7,
    "veg_kg": 0.5,
}

TREE_CO2_PER_YEAR_KG = 22  # одно дерево


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/energy')
def category_energy():
    return render_template('category_energy.html')

@app.route('/category/transport')
def category_transport():
    return render_template('category_transport.html')

@app.route('/category/forest')
def category_forest():
    return render_template('category_forest.html')

@app.route('/carbon-calculator')
def carbon_calculator_page():
    return render_template('carbon_calculator.html')

@app.route('/api/carbon-calculator', methods=['POST'])
def carbon_calculator_api():
    data = request.form if request.form else {}

    def get_float(key, default=0.0):
        v = data.get(key, default)
        try:
            val = float(v)
            return max(0.0, val)
        except (TypeError, ValueError):
            return 0.0

    electricity = get_float("electricity_kwh")
    gas = get_float("gas_m3")
    petrol = get_float("petrol_l")
    flight_km = get_float("flight_km")
    meat_beef = get_float("meat_beef_kg")
    meat_chicken = get_float("meat_chicken_kg")
    veg = get_float("veg_kg")

    total_co2_kg = (
        electricity * COEFFICIENTS["electricity_kwh"] +
        gas * COEFFICIENTS["gas_m3"] +
        petrol * COEFFICIENTS["petrol_l"] +
        flight_km * COEFFICIENTS["flight_km"] +
        meat_beef * COEFFICIENTS["meat_beef_kg"] +
        meat_chicken * COEFFICIENTS["meat_chicken_kg"] +
        veg * COEFFICIENTS["veg_kg"]
    )

    total_co2_tons = total_co2_kg / 1000
    trees_needed = total_co2_kg / TREE_CO2_PER_YEAR_KG

    # Уровень воздействия
    if total_co2_tons < 2:
        level = "низкий"
        message = "Хороший результат: ваш след ниже среднего."
    elif total_co2_tons < 6:
        level = "средний"
        message = "Типичный городской след. Есть пространство для улучшений."
    else:
        level = "высокий"
        message = "Высокий след. Несколько простых действий могут заметно его снизить."

    return jsonify({
        "co2_kg": round(total_co2_kg, 2),
        "co2_tons": round(total_co2_tons, 2),
        "trees_equivalent": round(trees_needed, 1),
        "level": level,
        "message": message,
    })


if __name__ == '__main__':
    app.run(debug=True)