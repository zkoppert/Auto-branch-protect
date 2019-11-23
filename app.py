from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def getEvent():
	print(request.method)
	return 'OK'

if __name__ == '__main__':
    app.run()
