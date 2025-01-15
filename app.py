from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

app = Flask(__name__)
app.config["SECRET_KEY"] = "qwerty"

filename = "feedback.txt"

menu = [
    {
        "pizza": "Пепперони",
        "ingredients": "Протёртые томаты, моцарелла, салями, пикантные пепперони. Аллергены: злаки, лактоза.",
        "price": 305
    },
    {
        "pizza": "Сырная",
        "ingredients": "Моцарелла бейби, фета, пармезан, горгонзола, проволоне, моцарелла. Аллергены: глютен, лактоза.",
        "price": 280
    },
    {
        "pizza": "Маргарита",
        "ingredients": "Протёртые томаты, моцарелла, базилик. Аллергены: злаки, лактоза.",
        "price": 190
    },
    {
        "pizza": "Гавайская",
        "ingredients": "Курица, ананас, моцарелла, томатный соус. Аллергены: злаки, лактоза.",
        "price": 250
    },
    {
        "pizza": "Вегетарианская",
        "ingredients": "Цукини, баклажан, томаты черри, перец болгарский, моцарелла, томатный соус. Аллергены: злаки, лактоза.",
        "price": 220
    }
]

class FeedbackForm(FlaskForm):
    visitor_name = StringField("Ваше имя", [validators.DataRequired()])
    pizza_name = StringField("Название пиццы", [validators.DataRequired()])
    service = StringField("Обслуживание (оценка от 1 до 5)", [validators.DataRequired()])
    comment = StringField("Ваш отзыв", [validators.DataRequired()])
    submit = SubmitField("Отправить отзыв")

@app.route("/")
def index():
    return render_template("index.html", menu=menu)

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback_data = {
            "visitor_name": form.visitor_name.data,
            "pizza_name": form.pizza_name.data,
            "service": form.service.data,
            "comment": form.comment.data
        }
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{feedback_data}\n")
        return render_template("thankyou.html", message="Спасибо за отзыв!")
    return render_template("feedback.html", form=form)

@app.route("/result")
def result():
    with open(filename, "r", encoding="utf-8") as file:
        feedbacks = [eval(line.strip()) for line in file.readlines()]
    return render_template("result.html", feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
