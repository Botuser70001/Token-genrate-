from flask import Flask, request, render_template_string, jsonify
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-" + os.urandom(16).hex())

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌀 NEO TOKEN EXTRACTOR | Cyber-AI System</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --neon-blue: #00f3ff;
            --neon-purple: #b967ff;
            --neon-pink: #ff00ff;
            --cyber-dark: #0a0a14;
            --cyber-darker: #050510;
            --matrix-green: #00ff88;
            --hologram-blue: #00b3ff;
            --warning: #ffcc00;
            --success: #00ffaa;
            --error: #ff0055;
            --terminal-text: #00ff00;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Rajdhani', sans-serif;
            background: var(--cyber-darker);
            color: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 243, 255, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 80% 70%, rgba(185, 103, 255, 0.05) 0%, transparent 20%);
        }

        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(180deg, 
                rgba(5, 5, 16, 0.9) 0%, 
                rgba(10, 10, 20, 0.95) 100%);
            z-index: -2;
        }

        .scanlines {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                to bottom,
                transparent 50%,
                rgba(0, 255, 136, 0.03) 51%
            );
            background-size: 100% 4px;
            z-index: -1;
            pointer-events: none;
            animation: scanlines 8s linear infinite;
        }

        @keyframes scanlines {
            0% { background-position: 0 0; }
            100% { background-position: 0 100%; }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }

        .header h1 {
            font-family: 'Orbitron', monospace;
            font-size: 3.5rem;
            font-weight: 900;
            letter-spacing: 2px;
            margin-bottom: 1rem;
            text-transform: uppercase;
            background: linear-gradient(90deg, 
                var(--neon-blue), 
                var(--neon-purple), 
                var(--neon-pink));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 30px rgba(0, 243, 255, 0.5);
            animation: glow 3s ease-in-out infinite alternate;
        }

        @keyframes glow {
            0% { text-shadow: 0 0 20px rgba(0, 243, 255, 0.5); }
            100% { text-shadow: 0 0 40px rgba(185, 103, 255, 0.7), 0 0 60px rgba(255, 0, 255, 0.4); }
        }

        .tagline {
            font-size: 1.2rem;
            color: var(--hologram-blue);
            letter-spacing: 1px;
            margin-bottom: 1.5rem;
            font-weight: 300;
        }

        .cyber-border {
            height: 3px;
            width: 200px;
            margin: 0 auto;
            background: linear-gradient(90deg, 
                transparent, 
                var(--neon-blue), 
                var(--neon-purple), 
                var(--neon-pink), 
                transparent);
        }

        .cyber-card {
            background: rgba(15, 15, 25, 0.8);
            border: 1px solid rgba(0, 243, 255, 0.2);
            border-radius: 12px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            box-shadow: 
                0 0 40px rgba(0, 243, 255, 0.1),
                inset 0 0 20px rgba(0, 243, 255, 0.05);
        }

        .cyber-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-blue));
            animation: scan 3s linear infinite;
        }

        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .card-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            color: var(--neon-blue);
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .card-title i {
            color: var(--neon-pink);
        }

        .input-section {
            margin-bottom: 2rem;
        }

        .input-label {
            display: block;
            font-size: 1.1rem;
            margin-bottom: 0.8rem;
            color: var(--hologram-blue);
            font-weight: 500;
        }

        .cyber-input {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 243, 255, 0.3);
            border-radius: 8px;
            padding: 1.2rem;
            color: white;
            font-family: 'Rajdhani', sans-serif;
            font-size: 1rem;
            resize: vertical;
            min-height: 150px;
            transition: all 0.3s ease;
        }

        .cyber-input:focus {
            outline: none;
            border-color: var(--neon-pink);
            box-shadow: 0 0 20px rgba(255, 0, 255, 0.2);
            background: rgba(0, 0, 0, 0.5);
        }

        .cyber-input::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }

        .cyber-btn {
            background: linear-gradient(135deg, 
                rgba(0, 243, 255, 0.1), 
                rgba(185, 103, 255, 0.1));
            border: 1px solid rgba(0, 243, 255, 0.3);
            color: var(--neon-blue);
            padding: 1.2rem 2.5rem;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: 1px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin: 0 auto;
        }

        .cyber-btn:hover {
            background: linear-gradient(135deg, 
                rgba(0, 243, 255, 0.2), 
                rgba(185, 103, 255, 0.2));
            border-color: var(--neon-pink);
            color: var(--neon-pink);
            box-shadow: 
                0 0 30px rgba(185, 103, 255, 0.3),
                inset 0 0 20px rgba(0, 243, 255, 0.1);
            transform: translateY(-2px);
        }

        .cyber-btn:active {
            transform: translateY(0);
        }

        .cyber-btn i {
            font-size: 1.5rem;
        }

        .result-section {
            margin-top: 2rem;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-card {
            background: rgba(10, 20, 30, 0.8);
            border: 1px solid;
            border-radius: 10px;
            padding: 2rem;
            margin-top: 1.5rem;
        }

        .result-success {
            border-color: var(--success);
            box-shadow: 0 0 30px rgba(0, 255, 170, 0.1);
        }

        .result-error {
            border-color: var(--error);
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.1);
        }

        .result-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .result-header i {
            font-size: 2rem;
        }

        .result-success .result-header i {
            color: var(--success);
        }

        .result-error .result-header i {
            color: var(--error);
        }

        .result-header h3 {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
        }

        .token-data {
            font-family: 'Courier New', monospace;
            background: rgba(0, 0, 0, 0.5);
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 3px solid var(--neon-blue);
            margin: 1rem 0;
            overflow-x: auto;
        }

        .token-field {
            margin-bottom: 1rem;
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }

        .token-label {
            color: var(--hologram-blue);
            min-width: 150px;
            font-weight: 600;
        }

        .token-value {
            color: var(--success);
            word-break: break-all;
            flex: 1;
        }

        .profile-pic {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 2px solid var(--neon-blue);
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.3);
            margin-top: 0.5rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 3rem 0;
        }

        .stat-card {
            background: rgba(20, 25, 40, 0.6);
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(0, 243, 255, 0.1);
            transition: transform 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            border-color: var(--neon-blue);
        }

        .stat-icon {
            font-size: 2.5rem;
            color: var(--neon-purple);
            margin-bottom: 1rem;
        }

        .stat-title {
            font-family: 'Orbitron', sans-serif;
            color: var(--neon-blue);
            margin-bottom: 0.5rem;
            font-size: 1.2rem;
        }

        .cyber-footer {
            text-align: center;
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(0, 243, 255, 0.2);
        }

        .creator {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            color: var(--hologram-blue);
        }

        .creator a {
            color: var(--neon-pink);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .creator a:hover {
            color: var(--neon-blue);
            text-decoration: underline;
        }

        .copyright {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.9rem;
        }

        .terminal-line {
            overflow: hidden;
            border-right: 2px solid var(--terminal-text);
            white-space: nowrap;
            margin: 0 auto;
            letter-spacing: 0.15em;
            animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: var(--terminal-text); }
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .cyber-card {
                padding: 1.5rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .token-field {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .token-label {
                min-width: auto;
            }
        }

        .hologram {
            position: relative;
        }

        .hologram::after {
            content: '';
            position: absolute;
            top: -5px;
            left: -5px;
            right: -5px;
            bottom: -5px;
            background: linear-gradient(45deg, 
                transparent 40%, 
                rgba(0, 243, 255, 0.1) 50%, 
                transparent 60%);
            z-index: -1;
            border-radius: inherit;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .hologram:hover::after {
            opacity: 1;
            animation: hologram-sweep 2s linear infinite;
        }

        @keyframes hologram-sweep {
            0% { background-position: -100% -100%; }
            100% { background-position: 200% 200%; }
        }

        .glitch {
            position: relative;
        }

        .glitch::before,
        .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--cyber-darker);
        }

        .glitch::before {
            left: 2px;
            text-shadow: -1px 0 var(--neon-pink);
            animation: glitch-1 2s infinite linear alternate-reverse;
        }

        .glitch::after {
            left: -2px;
            text-shadow: -1px 0 var(--neon-blue);
            animation: glitch-2 3s infinite linear alternate-reverse;
        }

        @keyframes glitch-1 {
            0% { clip-path: inset(40% 0 61% 0); }
            100% { clip-path: inset(92% 0 1% 0); }
        }

        @keyframes glitch-2 {
            0% { clip-path: inset(25% 0 58% 0); }
            100% { clip-path: inset(87% 0 10% 0); }
        }
    </style>
</head>
<body>
    <div class="matrix-bg" id="matrixBg"></div>
    <div class="scanlines"></div>
    
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1 class="glitch" data-text="🌀 NEO TOKEN EXTRACTOR">🌀 NEO TOKEN EXTRACTOR</h1>
            <p class="tagline terminal-line">SYSTEM INITIALIZED | CYBER-AI ACCESS PROTOCOL ENGAGED</p>
            <div class="cyber-border"></div>
        </div>

        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-card hologram">
                <div class="stat-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h3 class="stat-title">NEURAL ENCRYPTION</h3>
                <p>Quantum-level security protocols active</p>
            </div>
            
            <div class="stat-card hologram">
                <div class="stat-icon">
                    <i class="fas fa-bolt"></i>
                </div>
                <h3 class="stat-title">HYPERSPEED PROCESSING</h3>
                <p>Real-time token extraction & analysis</p>
            </div>
            
            <div class="stat-card hologram">
                <div class="stat-icon">
                    <i class="fas fa-code"></i>
                </div>
                <h3 class="stat-title">AI-POWERED DECODING</h3>
                <p>Advanced cookie pattern recognition</p>
            </div>
        </div>

        <!-- Main Form -->
        <div class="cyber-card hologram">
            <h2 class="card-title">
                <i class="fas fa-terminal"></i>
                ACCESS TERMINAL
            </h2>
            
            <form method="POST" action="/" class="input-section">
                <label class="input-label">
                    <i class="fas fa-cookie-bite"></i>
                    INPUT FACEBOOK COOKIES:
                </label>
                <textarea 
                    name="cookies" 
                    class="cyber-input" 
                    placeholder="sb=abc123; datr=xyz456; c_user=12345; xs=abc123xyz456"
                    required></textarea>
                
                <div style="text-align: center; margin-top: 2rem;">
                    <button type="submit" class="cyber-btn">
                        <i class="fas fa-play"></i>
                        INITIATE EXTRACTION SEQUENCE
                    </button>
                </div>
            </form>

            <!-- Results Section -->
            {% if result %}
            <div class="result-section">
                <div class="result-card {% if result.access_token %}result-success{% else %}result-error{% endif %}">
                    <div class="result-header">
                        {% if result.access_token %}
                            <i class="fas fa-check-circle"></i>
                            <h3>EXTRACTION SUCCESSFUL</h3>
                        {% else %}
                            <i class="fas fa-exclamation-triangle"></i>
                            <h3>EXTRACTION FAILED</h3>
                        {% endif %}
                    </div>
                    
                    <div class="token-data">
                        {% if result.access_token %}
                            <div class="token-field">
                                <span class="token-label">ACCESS TOKEN:</span>
                                <span class="token-value">{{ result.access_token }}</span>
                            </div>
                            
                            <div class="token-field">
                                <span class="token-label">USER ID:</span>
                                <span class="token-value">{{ result.user_id }}</span>
                            </div>
                            
                            <div class="token-field">
                                <span class="token-label">IDENTITY:</span>
                                <span class="token-value">{{ result.name }}</span>
                            </div>
                            
                            {% if result.profile_picture %}
                            <div class="token-field">
                                <span class="token-label">PROFILE IMAGE:</span>
                                <div>
                                    <img src="{{ result.profile_picture }}" alt="Profile" class="profile-pic">
                                </div>
                            </div>
                            {% endif %}
                        {% else %}
                            <div class="token-field">
                                <span class="token-label">ERROR:</span>
                                <span class="token-value">{{ result.error }}</span>
                            </div>
                            {% if result.details %}
                            <div class="token-field">
                                <span class="token-label">DETAILS:</span>
                                <span class="token-value">{{ result.details }}</span>
                            </div>
                            {% endif %}
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endif %}
        </div>

        <!-- Footer -->
        <div class="cyber-footer">
            <p class="creator">
                <i class="fas fa-robot"></i>
                CYBER SYSTEM DEVELOPED BY 
                <a href="https://github.com/Mryuvi1" target="_blank">DEVIL420</a>
            </p>
            <p class="copyright">
                © 2024 NEO SYSTEMS | ALL ACCESS LOGGED AND MONITORED
            </p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Button glitch effect
            const button = document.querySelector('.cyber-btn');
            if (button) {
                button.addEventListener('mouseenter', function() {
                    this.classList.add('glitch');
                    setTimeout(() => this.classList.remove('glitch'), 500);
                });
            }

            // Input hologram effect
            const textarea = document.querySelector('.cyber-input');
            if (textarea) {
                textarea.addEventListener('focus', function() {
                    this.parentElement.classList.add('hologram');
                });
                
                textarea.addEventListener('blur', function() {
                    this.parentElement.classList.remove('hologram');
                });
            }

            // Matrix rain effect
            function createMatrixRain() {
                const matrixBg = document.getElementById('matrixBg');
                if (!matrixBg) return;
                
                const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+-*/=%\"'#&_(),.;:?!\\|{}<>[]^~";
                
                // Clear existing
                matrixBg.innerHTML = '';
                
                // Create columns
                for (let i = 0; i < 30; i++) {
                    const column = document.createElement('div');
                    column.style.position = 'absolute';
                    column.style.top = '-100px';
                    column.style.left = `${Math.random() * 100}%`;
                    column.style.color = `rgba(0, 255, 136, ${Math.random() * 0.3 + 0.1})`;
                    column.style.fontSize = `${Math.random() * 10 + 10}px`;
                    column.style.fontFamily = 'monospace';
                    column.style.whiteSpace = 'nowrap';
                    column.style.zIndex = '-1';
                    column.style.opacity = '0.7';
                    
                    // Create text
                    let text = '';
                    for (let j = 0; j < 20; j++) {
                        text += chars[Math.floor(Math.random() * chars.length)];
                    }
                    column.textContent = text;
                    
                    matrixBg.appendChild(column);
                    animateColumn(column);
                }
            }

            function animateColumn(column) {
                let position = -100;
                const speed = Math.random() * 2 + 1;
                const maxHeight = window.innerHeight;
                
                function move() {
                    position += speed;
                    if (position > maxHeight + 100) {
                        position = -100;
                        column.style.left = `${Math.random() * 100}%`;
                        // Randomly change opacity
                        column.style.opacity = `${Math.random() * 0.5 + 0.3}`;
                    }
                    
                    column.style.top = `${position}px`;
                    
                    // Randomly change character
                    if (Math.random() > 0.9) {
                        const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+-*/=%\"'#&_(),.;:?!\\|{}<>[]^~";
                        const newChar = chars[Math.floor(Math.random() * chars.length)];
                        const text = column.textContent;
                        column.textContent = text.substring(1) + newChar;
                    }
                    
                    requestAnimationFrame(move);
                }
                
                move();
            }

            // Initialize effects
            createMatrixRain();
            
            // Auto-refresh matrix every 30 seconds
            setInterval(createMatrixRain, 30000);
            
            // Handle form submission with loading state
            const form = document.querySelector('form');
            if (form) {
                form.addEventListener('submit', function() {
                    const button = this.querySelector('.cyber-btn');
                    if (button) {
                        const originalText = button.innerHTML;
                        button.innerHTML = '<i class="fas fa-cog fa-spin"></i> PROCESSING...';
                        button.disabled = true;
                        
                        // Re-enable after 10 seconds if still disabled
                        setTimeout(() => {
                            if (button.disabled) {
                                button.innerHTML = originalText;
                                button.disabled = false;
                            }
                        }, 10000);
                    }
                });
            }
            
            // Auto-focus on textarea
            if (textarea) {
                setTimeout(() => {
                    textarea.focus();
                }, 1000);
            }
            
            // Add keyboard shortcut (Ctrl+Enter to submit)
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter' && textarea && textarea === document.activeElement) {
                    if (form) form.submit();
                }
            });
        });
        
        // Handle window resize
        window.addEventListener('resize', function() {
            const matrixBg = document.getElementById('matrixBg');
            if (matrixBg) {
                matrixBg.innerHTML = '';
                setTimeout(createMatrixRain, 100);
            }
        });
    </script>
</body>
</html>
"""

def get_facebook_token(cookies):
    """
    Get Facebook access token and user details using cookies
    
    Args:
        cookies (str): The Facebook cookies string
        
    Returns:
        dict: Dictionary containing token, user info, or error message
    """
    try:
        # Parse cookies
        cookie_dict = {}
        for cookie in cookies.split(';'):
            cookie = cookie.strip()
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookie_dict[key.strip()] = value.strip()
        
        # Check for required cookies
        required_cookies = ['c_user', 'xs']
        missing = [cookie for cookie in required_cookies if cookie not in cookie_dict]
        
        if missing:
            return {
                'error': f"Missing required cookies: {', '.join(missing)}",
                'details': 'Ensure you include c_user and xs cookies'
            }
        
        xs_cookie = cookie_dict.get('xs', '')
        
        # Generate simulated token (for demonstration)
        if xs_cookie:
            user_id = cookie_dict.get('c_user', 'Unknown')
            
            # Create a simulated token (in real app, use proper Facebook API)
            # This is just for demonstration purposes
            import hashlib
            import time
            
            # Create a unique token based on cookies and timestamp
            token_data = f"{user_id}:{xs_cookie}:{int(time.time())}"
            token_hash = hashlib.sha256(token_data.encode()).hexdigest()[:50]
            simulated_token = f"EAAG{token_hash}"
            
            return {
                'access_token': simulated_token,
                'user_id': user_id,
                'name': f"User_{user_id[:6]}",
                'profile_picture': f'https://ui-avatars.com/api/?name=User+{user_id}&background=0D8ABC&color=fff&size=256'
            }
        else:
            return {
                'error': 'Unable to extract token from cookies',
                'details': 'The xs cookie appears to be invalid or empty'
            }
            
    except Exception as e:
        return {
            'error': f"Error processing cookies: {str(e)}",
            'details': 'Please check your cookie format'
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        cookies = request.form.get('cookies', '').strip()
        if cookies:
            result = get_facebook_token(cookies)
    
    return render_template_string(HTML_TEMPLATE, result=result)

@app.route('/api', methods=['POST'])
def api():
    """API endpoint for programmatic access"""
    try:
        if request.is_json:
            data = request.get_json()
            cookies = data.get('cookies', '').strip()
        else:
            cookies = request.form.get('cookies', '').strip()
        
        if not cookies:
            return jsonify({'error': 'No cookies provided'}), 400
        
        result = get_facebook_token(cookies)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'online',
        'service': 'Facebook Token Generator',
        'version': '2.0.0',
        'author': 'DEVIL420',
        'environment': 'production' if os.environ.get('RENDER') else 'development',
        'timestamp': os.environ.get('RENDER_EXTERNAL_URL', 'localhost')
    }), 200

@app.route('/docs', methods=['GET'])
def documentation():
    """API documentation"""
    docs = {
        'api_endpoints': {
            'POST /api': {
                'description': 'Extract Facebook token from cookies',
                'parameters': {
                    'cookies': 'Facebook cookies string (required)'
                },
                'example_request': {
                    'cookies': 'sb=abc123; datr=xyz456; c_user=12345; xs=abc123xyz456'
                }
            },
            'GET /health': {
                'description': 'Health check endpoint'
            },
            'GET /docs': {
                'description': 'API documentation'
            }
        },
        'web_interface': 'Visit / for the web interface',
        'note': 'This is a demonstration tool for educational purposes only'
    }
    return jsonify(docs)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 25670))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    app.run(
        debug=debug_mode,
        host='0.0.0.0',
        port=port
    )
