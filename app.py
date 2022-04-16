from http.client import responses
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret1'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route('/')
def welcome():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions
    return render_template('home.html', title=title, instructions=instructions, questions=questions)

@app.route('/start', methods=["POST"])
def redirect_first():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def add_answer():
    
    responses = session[RESPONSES_KEY]
    answer = request.form['answer']
    session[RESPONSES_KEY].append(answer)
    session[RESPONSES_KEY] = responses
    
    if(len(session[RESPONSES_KEY]) == len(satisfaction_survey.questions)):
        return redirect('/completed')
    else:
        return redirect(f'/questions/{len(session[RESPONSES_KEY])}')

@app.route('/questions/<int:question_num>')
def start_questions(question_num):
    answers = session.get(RESPONSES_KEY)

    if answers is None:
        return redirect('/')

    if (len(answers) == len(satisfaction_survey.questions)):
        return redirect('/completed')

    if (len(answers) != question_num):
        flash('Invalid question. Redirecting you to correct question')
        return redirect(f'/questions/{len(answers)}')
    
    question = satisfaction_survey.questions[question_num]
    return render_template('question.html', question=question, question_num=question_num)

@app.route('/completed')
def show_answers():
    answers = session[RESPONSES_KEY]
    survey_questions = enumerate(satisfaction_survey.questions)
    return render_template('completed.html', responses=answers, questions=survey_questions)

@app.route('/secret')
def input_secret():
    return render_template('secret.html')


@app.route('/handle_secret')
def enter_secret():
    secret = 'secret1'
    secret_code = request.args['secret']
    if secret_code == secret:
        session['code-enter'] = True
        return redirect ('/welcome')
    else:
        flash('Incorrect secret code')
        return redirect('/secret')

@app.route('/welcome')
def welcome_secret():
    if session['code-enter']:
        flash("WELCOME! YOU'VE MADE IT")
        return render_template('welcome.html')
    else:
        return redirect('/secret')