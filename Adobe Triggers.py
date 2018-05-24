#Instructions:
#1.Set up Trigger in Adobe
#2.Subscribe to the Trigger through Adobe i/o - you will need to provide SSL cert. 
#3.Run this script in terminal - edit for specific trigger
#4.Run ngrok to generate webhook:   command ngrok http 5000
#5.Provide Adobe with ngrok url 


from flask import Flask, request, Response
import json
import urllib as ul
from mechanize import Browser

adobe_target_profile = 'profile.abandonbasket=1' # Target profile 

app = Flask(__name__)
 
@app.route('/' , methods=['GET','POST'])  
def abtrigger():
	if request.method == 'GET':
			challenge = request.args.get('challenge')
			return challenge
			resp = Response(challenge,status='200')  # first respond back to Adobe with 200 status and challenge
			return resp 
	else:
			print (request.is_json)

			content = request.get_json()
			
			mcid = content ['event']['com.adobe.mcloud.pipeline.pipelineMessage']['com.adobe.mcloud.protocol.trigger']['mcId']
			
			try:
				tracking_id = content ['event']['com.adobe.mcloud.pipeline.pipelineMessage']['com.adobe.mcloud.protocol.trigger']['enrichments']['analyticsHitSummary']['dimensions']['eVar56']['data'][0]

				print tracking_id
				print mcid
				url = 'http://britishskybroadcasti.tt.omtrdc.net/m2/britishskybroadcasti/profile/update?mbox3rdPartyId='+tracking_id+'&profile.attr=0&'+adobe_target_profile+''
				print url
				br =  Browser()
				br.set_handle_robots(False)
				response = br.open(url)
				response.read()
				print response
				return 'JSON posted'

			except IndexError:

				print "no tracking_id"
				return 'No tracking ID'

			

if __name__ == '__main__':

	context = ('local.crt', 'local.key')
	app.run()

