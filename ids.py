from flask import Flask, jsonify, render_template
import random
import json
import threading
import time

app = Flask(__name__)

alerts = []

def log_alert(alert):
    """Logs an alert to a JSON file."""
    with open('alerts_log.json', 'a') as log_file:
        json.dump(alert, log_file)
        log_file.write('\n')  # Add a newline for readability

def sniff_packets():
    """Simulates packet sniffing and detects suspicious activity."""
    while True:
        source_ip = random.choice(["192.168.1.6", "192.168.1.100"])
        destination_ip = random.choice(["20.205.253.130", "10.0.0.5"])
        
        if random.random() > 0.5:  # Randomly trigger suspicious activity
            alert = {
                "source": source_ip,
                "destination": destination_ip,
                "status": "Suspicious activity detected"
            }
            alerts.append(alert)
            log_alert(alert)  # Log the alert to a file
            print(f"ALERT: {alert['status']} from {alert['source']} to {alert['destination']}!")

        time.sleep(1)  # Sleep for a short duration before the next sniff

@app.route('/')
def home():
    """Home route for the IDS."""
    return jsonify({"message": "Intrusion Detection System is running"}), 200

@app.route('/alerts', methods=['GET'])
def get_alerts():
    """Route to get the list of alerts."""
    return render_template('alerts.html', alerts=alerts)

if __name__ == '__main__':
    # Start sniffing packets in a separate thread
    sniffing_thread = threading.Thread(target=sniff_packets)
    sniffing_thread.start()

    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000)
