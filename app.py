from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests

app = Flask(__name__)

# Configuration storage (in-memory for simplicity)
config = {
    'plex_token': '',
    'radarr_url': '',
    'radarr_api_key': '',
    'sonarr_url': '',
    'sonarr_api_key': ''
}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/configure', methods=['POST'])
def configure():
    config['plex_token'] = request.form['plex_token']
    config['radarr_url'] = request.form['radarr_url']
    config['radarr_api_key'] = request.form['radarr_api_key']
    config['sonarr_url'] = request.form['sonarr_url']
    config['sonarr_api_key'] = request.form['sonarr_api_key']
    return redirect(url_for('home'))

@app.route('/webhook', methods=['POST'])
def plex_webhook():
    data = request.json
    # Example: Check if the event is a new item added to the watchlist
    if data.get('event') == 'media.play':
        # Extract relevant information from the webhook
        title = data['Metadata']['title']
        media_type = data['Metadata']['type']

        if media_type == 'movie':
            # Send request to Radarr
            radarr_payload = {
                'title': title,
                'apikey': config['radarr_api_key']
            }
            requests.post(f"{config['radarr_url']}/api/movie", json=radarr_payload)
        elif media_type == 'show':
            # Send request to Sonarr
            sonarr_payload = {
                'title': title,
                'apikey': config['sonarr_api_key']
            }
            requests.post(f"{config['sonarr_url']}/api/series", json=sonarr_payload)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 