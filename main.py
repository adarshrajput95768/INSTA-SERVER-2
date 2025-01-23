from flask import Flask, request, render_template
import requests
import time

app = Flask(__name__)

# Instagram Graph API से Message भेजने का Function
def send_instagram_message(access_token, recipient_id, message, interval):
    url = f"https://graph.facebook.com/v17.0/{recipient_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    while True:  # Infinite Loop for Sending Unlimited Messages
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message}
        }

        try:
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print(f"Failed to send message: {response.status_code}, {response.text}")

        except Exception as e:
            print(f"An error occurred: {e}")

        # समय अंतराल डालें
        time.sleep(interval)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Form से प्राप्त होने वाली इनपुट
        access_token = request.form['access_token']
        recipient_id = request.form['recipient_id']
        message_file = request.files['message_file']
        interval = int(request.form['interval'])

        # Message File से Text पढ़ना
        try:
            message = message_file.read().decode('utf-8')
        except Exception as e:
            return f"Error reading message file: {e}"

        # Send Messages
        send_instagram_message(access_token, recipient_id, message, interval)

        return "Messages are being sent continuously!"

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
