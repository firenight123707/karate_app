from flask import Flask, render_template, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "dojo_secret"

japan_lang = [
    "Hachiji Dachi", "Fudo Dachi", "Heisoku Dachi", "Zenkutsu Dachi",
    "Tsuru Dachi", "Mae Tsuru Dachi", "Neko Dachi",
    "Ko Neko Dachi", "Kagi Dachi", "Sanchin Dachi",
    "Hangetsu Dachi", "Soshen Dachi", "Shiko Dachi",
    "Kokutsu Dachi", "Mitsurin Dachi", "Kiba Dachi"
]

english_lang = [
    "ready stance", "attention stance", "formal attention stance",
    "forward stance", "crane stance", "cross step stance",
    "cat stance", "laid out cat stance", "hook stance",
    "hourglass stance", "wide hourglass stance",
    "diagonal horse stance", "duck stance",
    "back stance", "jungle stance", "horse stance"
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/stances")
def stances():
    session["used"] = []
    session["score"] = 0
    return render_template("stances.html")

@app.route("/get_question")
def get_question():
    used = session.get("used", [])

    if len(used) == len(japan_lang):
        return jsonify({"finished": True, "score": session["score"]})

    while True:
        index = random.randint(0, len(japan_lang) - 1)
        if index not in used:
            used.append(index)
            session["used"] = used
            session["current_answer"] = english_lang[index]
            break

    return jsonify({
        "japanese": japan_lang[index],
        "finished": False
    })

@app.route("/check_answer/<user_answer>")
def check_answer(user_answer):
    correct = session.get("current_answer", "").lower()
    words = correct.split()
    if "stance" in words:
        words.remove("stance")

    is_correct = any(word in user_answer.lower() for word in words)

    if is_correct:
        session["score"] += 1

    return jsonify({
        "correct": is_correct,
        "score": session["score"]
    })

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)


# -----------------------
# KICKS DATA
# -----------------------

kicks = [
    {"japanese": "Mae geri", "english": "front snap kick"},
    {"japanese": "Mae ken geri", "english": "front snap instep kick"},
    {"japanese": "Mae kemoki geri", "english": "front thrust kick"},
    {"japanese": "Mawashi geri", "english": "round kick"},
    {"japanese": "Yoko sokuto geri", "english": "side kick (knife edge)"},
    {"japanese": "Yoko geri", "english": "side kick (ball of foot)"},
    {"japanese": "Yoko kekomi geri", "english": "side thrust kick"},
    {"japanese": "Kakato geri", "english": "heel kick"},
    {"japanese": "Ushiro geri", "english": "back kick"},
    {"japanese": "Ushiro kekomi geri", "english": "back thrust kick"},
    {"japanese": "Hiza geri", "english": "knee kick"},
    {"japanese": "Mae fumi komi geri", "english": "front stomp kick"},
    {"japanese": "Kangetsu geri", "english": "joint kick"},
    {"japanese": "Kagi geri", "english": "hook kick"},
    {"japanese": "Mae tobi geri", "english": "jump front kick"},
    {"japanese": "Yoko tobi geri", "english": "jump side kick"},
    {"japanese": "Mawashi tobi geri", "english": "jump round kick"},
    {"japanese": "Mikazuke geri", "english": "crescent kick"},
    {"japanese": "Gyaku mikazuke geri", "english": "reverse crescent kick"},
]

kick_index = 0
kick_score = 0



@app.route("/kicks")
def kicks_page():
    return render_template("kicks.html")


@app.route("/get_kick_question")
def get_kick_question():
    global kick_index

    if kick_index >= len(kicks):
        return jsonify({"finished": True, "score": kick_score})

    return jsonify({
        "japanese": kicks[kick_index]["japanese"],
        "finished": False
    })


@app.route("/check_kick_answer/<answer>")
def check_kick_answer(answer):
    global kick_index, kick_score

    correct_answer = kicks[kick_index]["english"].lower()

    if answer.lower().strip() == correct_answer:
        kick_score += 1
        kick_index += 1
        return jsonify({"correct": True, "score": kick_score})
    else:
        return jsonify({"correct": False, "score": kick_score})
