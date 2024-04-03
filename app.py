from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
responses = []
num_questions = len(satisfaction_survey.questions)

@app.route('/')
def show_form(): 
    return render_template('survey.html', survey=satisfaction_survey)

@app.route('/questions/<int:qID>')
def display_question(qID):
    if (qID != len(responses)):
        flash("Invalid. Cannot access the requested question.")
        return redirect(f'/questions/{len(responses)}')
    elif (len(responses) >= num_questions):
        return redirect('/done')
    else:
        return render_template('question.html', qID=qID, survey=satisfaction_survey, qty=num_questions)

@app.route('/questions/answer', methods=['POST'])
def add_answer():
    ans = list(request.form.keys())[0]
    responses.append(ans)
    if (len(responses) >= num_questions):
        return redirect('/done')
    else:
        return redirect(f'/questions/{len(responses)}')
    
@app.route('/done')
def display_done():
    return '<h1>Survey completed, thank you!</h1>'
 
@app.route('/oldpage')
def redirect_to():
    flash('Message for user!', 'error')
    return redirect('/pathway')