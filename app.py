from flask import Flask, request, render_template, redirect, flash
from flask import session, make_response
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
    """Home page to begin survery"""
    return render_template('survey.html', survey=satisfaction_survey)

@app.route('/questions/<int:qID>')
def display_question(qID):
    """Displays question for user"""
    qnumber = len(session['responses'])
    
    if (qID != len(session['responses'])): # true if user edited url for invalid question
        flash("Invalid. Cannot access the requested question.")
        return redirect(f'/questions/{qnumber}')
    
    elif (len(session['responses']) >= num_questions): # true if the user is done and changes url to show a question
        return redirect('/done')
    
    else: # display next question for user
        return render_template('question.html', qID=qID, survey=satisfaction_survey, qty=num_questions)

@app.route('/questions/answer', methods=['POST'])
def add_answer():
    """post method that saves survey answer and moves to next question"""
    ans = list(request.form.keys())[0]
    responses.append(ans)
    session['responses'] = responses
    qnumber = len(session['responses'])
    
    if (len(session['responses']) >= num_questions): # Shows final page if no more questions
        return redirect('/done')
    
    else: # moves to next question
        return redirect(f'/questions/{qnumber}')

@app.route('/storage', methods=['POST'])
def store_data():
    """stores survery answers on session"""
    session['responses']=[]
    
    return redirect('/questions/0')
    

@app.route('/done')
def display_done():
    """Page to show user that the survery is done"""
    
    return '<h1>Survey completed, thank you!</h1>'