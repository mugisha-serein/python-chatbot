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
  <li><strong>Tkinter GUI</strong> with chat bubbles, animation, and responsive layout</li>
  <li>Layered controller → service → engine structure keeps responsibilities clear</li>
  <li>User and bot messages aligned left/right with distinct colors</li>
  <li>Keyword-based intent matching with priority ordering</li>
  <li>Persistent preferences (name, favorites, likes) stored locally</li>
  <li>Modular folder per layer: <code>interface/gui</code>, <code>controller</code>, <code>service</code>, <code>engine</code>, <code>data</code>, <code>knowledge</code>, and <code>preferences</code></li>
  <li>Fallback responses for unknown input</li>
  <li>Built-in intents for time, date, jokes, weather tips, facts, reminders, and small talk</li>
  <li>Live weather lookup through the Open-Meteo API when you specify a location</li>
  <li>Voice input from the interface via the microphone button (depends on <code>SpeechRecognition</code> plus a microphone backend such as PyAudio or SoundDevice)</li>
  <li>Service layer handles chat orchestration, context, personalization, and security before invoking the engine</li>
  <li>Hybrid engine splits into rule-based intents, a placeholder NLP classifier, and a decision engine</li>
  <li>Data layer combines JSONL history, optional PostgreSQL persistence, and Redis caching</li>
  <li>Advanced NLP support via optional transformer models for better intent classification</li>
  <li>Easily extensible for new intents or AI integration</li>
  <li>Intent reference in <code>documentation.md</code></li>
</ul>

<hr>

<h2 id="architecture">Architecture</h2>

<pre>
User Input -> [GUI (Tkinter)] -> [Controller (controller.py)] -> [Service Layer (service.py)] -> [Engine (rule+NLP+decision)] -> [Data Layer (data.py + Postgres/Redis + history.py)] -> [External Integrations (Open-Meteo, etc.)]
</pre>

<h3>Layer Responsibilities</h3>
<ul>
  <li><strong>Interface Layer</strong>: Tkinter GUI remains the entry point and only interacts with the controller.</li>
  <li><strong>Controller Layer</strong>: Validates inputs, enforces rate limits, persists history, and forwards messages to the service.</li>
  <li><strong>Service Layer</strong>: Central orchestration—manages conversation context, personalization (via preferences), security checks, and caching before invoking the engine.</li>
  <li><strong>Engine Layer</strong>: Hybrid NLP that runs a rule-based intent matcher, pluggable NLP classifier, and decision engine to choose the best response (time/date/weather handled dynamically within the decision path).</li>
  <li><strong>Data Layer</strong>: JSONL history plus optional PostgreSQL persistence (`CHATBOT_POSTGRES_DSN`) and Redis caching (`CHATBOT_REDIS_URL`), with an in-memory fallback for environments without those services.</li>
  <li><strong>External Integrations</strong>: Live weather via Open-Meteo and any future connectors (wrapped through the service/engine to keep the GUI unaware of network logic).</li>
</ul>

<h3>Message Processing Pipeline</h3>
<pre>
receive_input()
    ↓
validate_input()
    ↓
load_user_context()
    ↓
clean_text()
    ↓
intent = detect_intent()
        ↓
        (rule intent? use it : fall back to `unknown`)
decision = choose_response_strategy()
response = generate_response()
store_message()
return response
</pre>

<hr>

<h2 id="project-structure">Project Structure</h2>

<pre>
python-chatbot/
|
+-- interface/
++-- gui/
+++-- gui.py           # Tkinter GUI front end
+-- controller/
++-- controller.py     # Coordinates GUI and Service
+-- service/
++-- service.py        # Orchestrates context, personalization, and caching
+-- engine/
++-- engine.py         # Hybrid rule/NLP/decision logic
+-- data/
++-- data.py           # Persistent storage interface
++-- history.py        # JSONL history helpers used by the data layer
+-- knowledge/
++-- knowledge.py      # Intent database
+-- preferences/
++-- preferences.py    # Persistent preference parsing
+-- README.md          # Project documentation
</pre>

<hr>

<h2 id="setup--installation">Setup & Installation</h2>

<ol>
  <li>Clone repository:
    <pre>git clone &lt;your-repo-url&gt;
  cd python-chatbot</pre>
  </li>
  <li>Install dependencies:
    <pre>pip install requests</pre>
    <p><em>Optional</em>: install <code>psycopg2-binary</code> if you plan to enable PostgreSQL support via the data layer (<code>pip install psycopg2-binary</code>).</p>
    <p><em>Optional</em>: install <code>redis</code> and export <code>CHATBOT_REDIS_URL</code> when you want Redis-backed caching (<code>pip install redis</code>).</p>
    <p><em>Optional</em>: install <code>transformers</code> and a backend such as <code>torch</code> to unlock the advanced NLP pipeline; configure the model via <code>CHATBOT_NLP_MODEL</code> (default: <code>typeform/distilbert-base-uncased-mnli</code>).</p>
    <p>Set environment variables before launching the GUI if you enable persistence:</p>
    <ul>
      <li><code>CHATBOT_POSTGRES_DSN</code>: PostgreSQL connection string (e.g., <code>postgresql://user:pass@host:5432/dbname</code>).</li>
      <li><code>CHATBOT_REDIS_URL</code>: Redis URL (e.g., <code>redis://localhost:6379/0</code>).</li>
    </ul>
  </li>
  <li>Run the chatbot:
    <pre>python -m interface.gui.gui</pre>
  </li>
</ol>

<p><em>Note:</em> Tkinter comes pre-installed in most Python distributions.</p>

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
  <li>Preferences are parsed first to capture things like names and favorites.</li>
  <li><code>detect_intent()</code> scans intents in priority order (except <code>"unknown"</code>) for the first keyword match.</li>
  <li>If no match -> fallback <code>"unknown"</code> intent.</li>
  <li><code>select_response()</code> picks a random response from the intent.</li>
  <li>Response is displayed in the chat GUI.</li>
</ol>

<p><strong>Note:</strong> Uses priority-based matching to avoid collisions (e.g., <code>what can you do</code> vs <code>do</code>).</p>

<hr>

<h2 id="future-updates--expansion">Future Updates & Expansion</h2>

<ul>
  <li>Advanced NLP integration (machine learning, transformer models)</li>
  <li>Context awareness for multi-turn conversation</li>
  <li>Optional packaging and distribution setup</li>
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
<p>feel free to use, modify, and distribute for personal or educational purposes.</p>

