from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Словарь функций, которые пользователь может выбрать
FUNCTIONS = {
    'x2': lambda x: x ** 2,
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'exp': lambda x: math.exp(x),
    'sqrt': lambda x: math.sqrt(x) if x >= 0 else None,
}

# Создали функцию index и далее возвращаем уже из папки "index.html"
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        # Получаем данные из формы
        func_name = request.form.get("function")
        a = float(request.form.get("a"))
        b = float(request.form.get("b"))
        n = int(request.form.get("n"))

        # Проверяем, что a < b
        if a >= b:
            return render_template("calculator.html", error="Предел a должен быть меньше b")

        # Проверяем, что n > 0
        if n <= 0:
            return render_template("calculator.html", error="Количество разбиений n должно быть больше 0")

        # Вычисляем интеграл
        result = compute_integral(FUNCTIONS[func_name], a, b, n)

        # Показываем страницу с результатом
        return render_template("result.html",
                               func_name=func_name,
                               a=a,
                               b=b,
                               n=n,
                               result=result)

    # Если GET-запрос, просто показываем форму
    return render_template("calculator.html")


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/about/<func_name>")
def about_function(func_name):
    functions_info = {
        'x2': 'Функция x² — парабола. Интеграл от 0 до 1 равен 1/3.',
        'sin': 'Функция sin(x) — синусоида. Интеграл от 0 до π равен 2.',
        'cos': 'Функция cos(x) — косинусоида. Интеграл от 0 до π/2 равен 1.',
        'exp': 'Функция eˣ — экспонента. Интеграл от 0 до 1 равен e-1 ≈ 1.718.',
        'sqrt': 'Функция √x — квадратный корень. Интеграл от 0 до 1 равен 2/3.',
    }
    info = functions_info.get(func_name, "Информация не найдена")
    return render_template("about_function.html", func_name=func_name, info=info)
def compute_integral(func, a, b, n):
    """Вычисляет определённый интеграл методом прямоугольников"""
    h = (b - a) / n  # ширина каждого прямоугольника
    integral = 0

    for i in range(n):
        x = a + i * h  # левая граница i-го прямоугольника
        y = func(x)  # значение функции в этой точке
        integral += y * h  # площадь прямоугольника

    return integral


if __name__ == "__main__":
    app.run(debug=True)