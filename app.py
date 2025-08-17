from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from main import describe_linkedin_profile

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    name = request.form.get('name')
    output, profile_pic = describe_linkedin_profile(name)
    print(output)
    print(profile_pic)
    return jsonify({
        'summary_and_facts': output.to_dict(),
        'photoUrl': profile_pic
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
