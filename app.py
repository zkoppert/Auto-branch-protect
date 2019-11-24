from flask import Flask, request
import requests
import json
import os
import time

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	# Store incoming json data from webhook
	payload = request.get_json()
	user = 'zkoppert'
	cred = os.environ['GH_TOKEN']
	if payload is None:
		print('POST was not formatted in JSON')

	# Verify the repo was created
	try:
		if payload['action'] == 'created':
			# Delay needed for server to be create the page, otherwise a 404 returns
			time.sleep(1)
			# Create branch protection for the master branch of the repo
			branch_protection = {
               "required_status_checks": { "strict": True, "contexts": [ "default" ] },
               "enforce_admins": False,
               "required_pull_request_reviews": None,
               "restrictions": None
            }
			session = requests.session()
			session.auth = (user, cred)
			response = session.put(payload['repository']['url'] + '/branches/master/protection', json.dumps(branch_protection))
			if response.status_code == 200:
				print('Branch protection created successfully. Status code: ', response.status_code)
			else:
				print(response.content)
				print('Unable to create branch protection. Status code: ',  response.status_code)
	except KeyError:
		# Ignore POST payload since it is not a create action
		pass

	return 'OK'

if __name__ == '__main__':
    app.run()
