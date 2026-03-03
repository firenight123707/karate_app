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
@app.route("/kicks")
def kicks():
    session["used_kicks"] = []
    session["kick_score"] = 0
    return render_template("kicks.html")


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





# -----------------------
# KICKS DATA
# -----------------------

kicks_japanese = [
    "Mae geri",
    "Mae ken geri",
    "Mae kemoki geri",
    "Mawashi geri",
    "Yoko sokuto geri",
    "Yoko geri",
    "Yoko kekomi geri",
    "Kakato geri",
    "Ushiro geri",
    "Ushiro kekomi geri",
    "Hiza geri",
    "Mae fumi komi geri",
    "Kangetsu geri",
    "Kagi geri",
    "Mae tobi geri",
    "Yoko tobi geri",
    "Mawashi tobi geri",
    "Mikazuke geri",
    "Gyaku mikazuke geri"
]

kicks_english = [
    "front snap kick",
    "front snap instep kick",
    "front thrust kick",
    "round kick",
    "side kick knife edge",
    "side kick ball of foot",
    "side thrust kick",
    "heel kick",
    "back kick",
    "back thrust kick",
    "knee kick",
    "front stomp kick",
    "joint kick",
    "hook kick",
    "jump front kick",
    "jump side kick",
    "jump round kick",
    "crescent kick",
    "reverse crescent kick"
]


kick_index = 0
kick_score = 0



@app.route("/kicks")
def kicks_page():
    return render_template("kicks.html")


@app.route("/get_kick_question")
def get_kick_question():
    used = session.get("used_kicks", [])

    if len(used) == len(kicks_japanese):
        return jsonify({"finished": True, "score": session["kick_score"]})

    while True:
        index = random.randint(0, len(kicks_japanese) - 1)
        if index not in used:
            used.append(index)
            session["used_kicks"] = used
            session["current_kick_answer"] = kicks_english[index]
            break

    return jsonify({
        "japanese": kicks_japanese[index],
        "finished": False
    })



@app.route("/check_kick_answer/<user_answer>")
def check_kick_answer(user_answer):
    correct = session.get("current_kick_answer", "").lower()
    words = correct.split()

    if "kick" in words:
        words.remove("kick")

    is_correct = any(word in user_answer.lower() for word in words)

    if is_correct:
        session["kick_score"] += 1

    return jsonify({
        "correct": is_correct,
        "score": session["kick_score"]
    })

if __name__ == "__main__":
    app.run(debug=True)
