from flask import Flask, render_template_string, request, jsonify
import random
import time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Fake Terminal</title>
  <style>
    .prompt { color: #00ffff; font-family: monospace; }
    #terminal-input {
      background: transparent;
      border: none;
      color: #fff;
      font-family: monospace;
      outline: none;
      width: 60%;
      min-width: 100px;
      max-width: 100%;
      font-size: 1em;
    }
    .terminal {
      width: 700px;
      max-width: 98vw;
      height: 400px;
      max-height: 80vh;
      background: #111;
      border: 3px solid cyan;
      border-radius: 8px;
      margin: 40px auto;
      padding: 1.5rem;
      box-sizing: border-box;
      box-shadow: 2px 4px 8px rgba(0,0,0,0.9);
      overflow-y: auto;
      color: #fff;
      font-size: 1.1em;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      transition: width 0.2s, height 0.2s;
    }
    body {
      background-color: #222;
      color: white;
      font-family: monospace;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0;
    }
    @media (max-width: 800px) {
      .terminal {
        width: 98vw;
        height: 60vh;
        padding: 1rem;
        font-size: 1em;
      }
      #terminal-input {
        width: 90%;
        font-size: 0.95em;
      }
    }
    @media (max-width: 500px) {
      .terminal {
        width: 100vw;
        height: 60vh;
        padding: 0.5rem;
        font-size: 0.95em;
      }
      #terminal-input {
        width: 100%;
        font-size: 0.9em;
      }
    }
  </style>
</head>
<body>
  <div class="terminal">
    <div id="terminal-output"></div>
  </div>
  <script>
    const output = document.getElementById('terminal-output');

    function createPrompt() {
      const promptWrapper = document.createElement('div');
      promptWrapper.className = 'prompt-line';
      promptWrapper.innerHTML = `<span class="prompt">~/projects/terminal: </span>`;
      const input = document.createElement('input');
      input.type = 'text';
      input.autofocus = true;
      input.autocomplete = 'off';
      input.className = 'terminal-input';
      input.style.background = 'transparent';
      input.style.border = 'none';
      input.style.color = '#fff';
      input.style.fontFamily = 'monospace';
      input.style.outline = 'none';
      input.style.width = '60%';
      promptWrapper.appendChild(input);
      output.appendChild(promptWrapper);
      output.scrollTop = output.scrollHeight;
      input.focus();

      input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          const query = input.value;
          input.disabled = true;
          fetch('/fake_install', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query})
          })
          .then(res => res.json())
          .then(data => {
            let index = 0;
            const steps = data.steps;

            function showNextStep() {
              if (index < steps.length) {
                const stepLine = document.createElement('div');
                stepLine.textContent = steps[index];
                output.appendChild(stepLine);
                output.scrollTop = output.scrollHeight;
                index++;
                setTimeout(showNextStep, 1000);
              } else {
                const successLine = document.createElement('div');
                successLine.textContent = data.success;
                output.appendChild(successLine);
                output.scrollTop = output.scrollHeight;
                // After done, create a new prompt/input for next command
                createPrompt();
              }
            }
            showNextStep();
          });
        }
      });
    }

    // Remove the initial prompt/input from HTML and use JS to create it
    output.innerHTML = '';
    createPrompt();
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/fake_install', methods=['POST'])
def fake_install():
    data = request.get_json()
    query = data.get('query', '').strip()

    
    install_steps = [
        f"Downloading {query}...",
        "Resolving dependencies...",
        "Extracting files...",
        "Configuring installation...",
        "Finalizing setup..."
    ]

    
    time.sleep(random.uniform(1, 3))  

    return jsonify({
        "steps": install_steps,
        "success": f"✅ Successfully installed {query}"
    })

if __name__ == '__main__':
    app.run()
