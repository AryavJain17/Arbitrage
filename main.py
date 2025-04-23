from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Arbitrage Betting Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; background: #f0f0f0; }
        .container { background: white; padding: 30px; max-width: 600px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; }
        input, button { width: 100%; padding: 10px; margin: 10px 0; }
        .result { background: #d4edda; color: #155724; padding: 15px; margin-top: 20px; border-left: 5px solid #28a745; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; margin-top: 20px; border-left: 5px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Arbitrage Betting Calculator</h2>
        <form method="post">
            <label>Total Money:</label>
            <input type="number" step="0.01" name="total_money" required>
            <label>Odds for Side 1:</label>
            <input type="number" step="0.01" name="odds1" required>
            <label>Odds for Side 2:</label>
            <input type="number" step="0.01" name="odds2" required>
            <button type="submit">Calculate</button>
        </form>
        {% if result %}
            <div class="result">
                <p><strong>Bet on Side 1:</strong> {{ result['Bet on Odds1'] }}</p>
                <p><strong>Bet on Side 2:</strong> {{ result['Bet on Odds2'] }}</p>
                <p><strong>Guaranteed Profit:</strong> ₹{{ result['Guaranteed Profit'] }}</p>
            </div>
        {% elif error %}
            <div class="error">
                <p>{{ error }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def arbitrage_bet(total_amount, odds1, odds2):
    inv1 = 1 / odds1
    inv2 = 1 / odds2
    total_inv = inv1 + inv2

    if total_inv >= 1:
        return None

    bet1 = total_amount * inv1 / total_inv
    bet2 = total_amount * inv2 / total_inv
    payout1 = bet1 * odds1
    payout2 = bet2 * odds2
    profit = min(payout1, payout2) - total_amount

    return {
        "Bet on Odds1": round(bet1, 2),
        "Bet on Odds2": round(bet2, 2),
        "Guaranteed Profit": round(profit, 2)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            total_money = float(request.form['total_money'])
            odds1 = float(request.form['odds1'])
            odds2 = float(request.form['odds2'])
            result = arbitrage_bet(total_money, odds1, odds2)
            if not result:
                error = "DON'T PLACE THE BET — WRONG CHOICE"
        except:
            error = "Invalid input. Please enter valid numbers."

    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
