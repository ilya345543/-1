from flask import Flask, render_template, request
import math

app = Flask(__name__)

FUNCTIONS = {
    'x2': lambda x: x ** 2,
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'exp': lambda x: math.exp(x),
    'sqrt': lambda x: math.sqrt(x) if x >= 0 else None,
    'x': lambda x: x,
    'const': lambda x: 1,
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        func_name = request.form.get("function")
        a = float(request.form.get("a"))
        b = float(request.form.get("b"))
        n = int(request.form.get("n"))

        if a >= b:
            return render_template("calculator.html", error="Предел a должен быть меньше b")

        if n <= 0:
            return render_template("calculator.html", error="Количество разбиений n должно быть больше 0")

        result = compute_integral(FUNCTIONS[func_name], a, b, n)

        return render_template("result.html",
                               func_name=func_name,
                               a=a,
                               b=b,
                               n=n,
                               result=result)

    return render_template("calculator.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/about/<func_name>")
def about_function(func_name):
    functions_info = {
        'x2': 'Функция x² — парабола ветвями вверх, вершина в (0;0).',
        'sin': 'Функция sin(x) — синусоида: волнообразная кривая, нечетная функция.',
        'cos': 'Функция cos(x) — косинусоида: волнообразная кривая, четная функция.',
        'exp': 'Функция eˣ — экспонента: показательная функция.',
        'sqrt': 'Функция √x — квадратный корень: график корня.',
        'x': 'Функция x — линейная: возрастающая прямая, с углом наклона 45 градусов.',
        'const': 'Функция 1 — константа: прямая параллельная оси абсцисс.',
    }
    info = functions_info.get(func_name, "Информация не найдена")
    return render_template("about_function.html", func_name=func_name, info=info)

def compute_integral(func, a, b, n):
    h = (b - a) / n
    integral = 0
    for i in range(n):
        x = a + i * h
        y = func(x)
        if y is None:
            return None
        integral += y * h
    return integral

if __name__ == "__main__":
    app.run(debug=True)