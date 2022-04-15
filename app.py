from crypt import methods
from pydoc import render_doc
from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret1'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def welcome():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions
    return render_template('home.html', title=title, instructions=instructions, questions=questions)

@app.route('/start', methods=["POST"])
def redirect_first():
    # RESPONSES_KEY = []
    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def add_answer():
    answers_list = responses
    answer = request.form['answer']
    answers_list.append(answer)
    print(answer, answers_list)
    if(len(answers_list) == len(satisfaction_survey.questions)):
        return redirect('/completed')
    else:
        return redirect(f'/questions/{len(answers_list)}')

@app.route('/questions/<int:question_num>')
def start_questions(question_num):
    answers = responses

    if answers is None:
        return redirect('/')
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/completed')
    if (len(responses) != question_num):
        flash('Invalid question. Redirecting you to correct question')
        return redirect(f'/questions/{len(responses)}')
    else:
        question = satisfaction_survey.questions[question_num]
        return render_template('question.html', question=question, question_num=question_num)


@app.route('/completed')
def show_answers():
    answers = responses
    questions = satisfaction_survey.questions
    print(responses)

    return render_template('completed.html', responses=answers, questions=questions)