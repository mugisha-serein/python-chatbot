<h1 align="center">Python Chatbot</h1>

<p align="center">
A modular and extensible chatbot built with <strong>pure Python</strong>, <strong>Tkinter GUI</strong>, and a <strong>keyword-based intent system</strong>.
</p>

<hr>

<h2>Table of Contents</h2>
<ul>
  <li><a href="#features">Features</a></li>
  <li><a href="#architecture">Architecture</a></li>
  <li><a href="#project-structure">Project Structure</a></li>
  <li><a href="#setup--installation">Setup & Installation</a></li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#how-it-works">How it Works</a></li>
  <li><a href="#future-updates--expansion">Future Updates & Expansion</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#license">License</a></li>
</ul>

<hr>

<h2 id="features">Features</h2>
<ul>
  <li>Lightweight Python chatbot using <strong>pure Python</strong> (no frameworks required)</li>
  <li><strong>Tkinter GUI</strong> with scrollable chat history</li>
  <li>User messages displayed on <span style="color:blue;">right</span>, bot responses on <span style="color:green;">left</span></li>
  <li>Keyword-based intent matching (first match)</li>
  <li>Modular design: <code>knowledge.py</code>, <code>engine.py</code>, <code>gui.py</code></li>
  <li>Fallback responses for unknown input</li>
  <li>Easily extensible for new intents or AI integration</li>
</ul>

<hr>

<h2 id="architecture">Architecture</h2>

<pre>
User Input → [GUI] → [Engine] → [Knowledge Base] → Response → [GUI Display]
</pre>

<h3>Components:</h3>
<ul>
  <li><strong>GUI (gui.py)</strong>: Handles user input and display using Tkinter.</li>
  <li><strong>Engine (engine.py)</strong>: Cleans message, detects intent, selects response.</li>
  <li><strong>Knowledge Base (knowledge.py)</strong>: Dictionary of intents, keywords, and responses.</li>
</ul>

<hr>

<h2 id="project-structure">Project Structure</h2>

<pre>
python-chatbot/
│
├─ gui.py               # Tkinter GUI
├─ engine.py            # Chatbot logic and intent matching
├─ knowledge.py         # Intent database
└─ README.md            # Project documentation
</pre>

<hr>

<h2 id="setup--installation">Setup & Installation</h2>

<ol>
  <li>Clone repository:
    <pre>git clone &lt;your-repo-url&gt;
         cd python-chatbot</pre>
  </li>
  <li>Run the chatbot:
    <pre>python gui.py</pre>
  </li>
</ol>

<p><em>Note:</em> Tkinter comes pre-installed in most Python distributions. For Docker, see Dockerfile instructions.</p>

<hr>

<h2 id="usage">Usage</h2>

<ol>
  <li>Type a message in the input box.</li>
  <li>Press <strong>Enter</strong> or click <strong>Send</strong>.</li>
  <li>Bot will display a response in the scrollable chat area.</li>
</ol>

<hr>

<h2 id="how-it-works">How it Works</h2>

<ol>
  <li>GUI captures user input using Tkinter.</li>
  <li>Engine calls <code>clean_message()</code> to normalize text.</li>
  <li><code>detect_intent()</code> scans all intents (except <code>"unknown"</code>) for the first keyword match.</li>
  <li>If no match → fallback <code>"unknown"</code> intent.</li>
  <li><code>select_response()</code> picks a random response from the intent.</li>
  <li>Response is displayed in the chat GUI.</li>
</ol>

<p><strong>Note:</strong> Currently uses first-matched keyword logic for simplicity and predictability.</p>

<hr>

<h2 id="future-updates--expansion">Future Updates & Expansion</h2>

<ul>
  <li>Add more intents: <em>time, date, jokes, weather, etc.</em></li>
  <li>Advanced NLP integration (machine learning, transformer models)</li>
  <li>Context awareness for multi-turn conversation</li>
  <li>Persistent knowledge: conversation history and user preferences</li>
  <li>GUI improvements: chat bubble colors, animations, left/right alignment, responsive resizing</li>
  <li>Docker improvements: GUI support in Linux containers, headless mode for testing</li>
</ul>

<hr>

<h2 id="contributing">Contributing</h2>

<ul>
  <li>Fork the repository</li>
  <li>Add new intents to <code>knowledge.py</code></li>
  <li>Extend <code>engine.py</code> for new logic</li>
  <li>Update GUI in <code>gui.py</code> if needed</li>
  <li>Submit a pull request</li>
</ul>

<hr>

<h2 id="license">License</h2>
<p>feel  free to use, modify, and distribute for personal or educational purposes.</p>