from crypt import methods
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"

class Calculator:
    def __init__(self, val1: int, val2: int) -> None:
        self.val1 = val1
        self.val2 = val2
    
    @staticmethod
    def validParams(val1, val2, operation) -> bool:
        val1Valid = type(val1) is int
        val2Valid = type(val2) is int
        
        operationIsValid = (type(operation) is str) and (Calculator.__isOperationValid(operation))
        return val1Valid and val2Valid and operationIsValid

    @staticmethod
    def __isOperationValid(operation) -> bool:
        return (
            operation == '+' or 
            operation == '-' or 
            operation == '*' or 
            operation == '/'
        )

    def getResult(self, operation):
        if operation == '+':
            return self.val1 + self.val2
        if operation == '-':
            return self.val1 - self.val2
        if operation == '*':
            return self.val1 * self.val2
        if operation == '/':
            return self.val1 / self.val2

@app.route('/calculator')
def simple_calculator():
    return render_template("calculator.html")

@app.route('/calculator-answer', methods=['GET', 'POST'])
def calculator_answer():
    val1 = int(request.form['val1'])
    val2 = int(request.form['val2'])
    operation = request.form['operation']

    if not Calculator.validParams(val1, val2, operation):
        return jsonify({ "message": "Invalid Parameters"}), 400

    calculator = Calculator(val1, val2)
    return jsonify({ "result": calculator.getResult(operation)}), 200
    