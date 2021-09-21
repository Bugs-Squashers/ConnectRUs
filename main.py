from flask import Flask
import random

# Create a flask app
app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

# Index page
@app.route('/')
def hello():
  return "Hello World!"

#Amanda's HTTP Request
@app.route("/number/<input>")
def number(input):
  input = int(input)
  if (input%2==0):
    return "even!"
  else:
    return "odd!"

#Sandra's HTTP Request
def ftoc(ftemp):
   return (ftemp-32.0)*(5.0/9.0)

@app.route('/ftoc/<ftempString>')
def convertFtoC(ftempString):
    ftemp = 0.0
    try:
        ftemp = float(ftempString)
        ctemp = ftoc(ftemp)
        return ftempString + "° degree Farenheit is " + str(ctemp) +" in Celsius "
    except ValueError:
        return "Sorry.  Could not convert " + ftempString + " to a number"

#Jonathan's HTTP Request
@app.route("/randomno/<input>")
def randomno(x,y,z):
    ran = []
    for i in range(z):
      ran.append(random.randint(x, y))
    return ran
    # Driver Code
    n = int(input("How many Random Numbers displayed? :"))
    s = int(input("Enter Starting number :"))
    e = int(input("Enter Ending number :"))
    print(randomno(x, y, z))
   
#Julia's HTTP Request
@app.route("/factorial/<n>")
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    n = int(input("Input a number to compute the factiorial : "))
    print(factorial(n))

#Chelsea's HTTP Request
@app.route("/square/<n>")
def square(n):
    n = int(n)
    n_sq = n ** 2
    return "The square of " + str(n) + " is " + str(n_sq)

app.run(host = "0.0.0.0")
