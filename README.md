# 🌀 NEO Token Extractor

A futuristic Facebook Token Generator with cyberpunk UI.

## Features
- 🎨 Futuristic cyberpunk interface
- ⚡ Real-time token extraction
- 🔒 Secure cookie processing
- 📱 Fully responsive design
- 🚀 API endpoint for developers

## Live Demo
Visit: [https://neo-token-extractor.onrender.com](https://neo-token-extractor.onrender.com)

## API Usage

```bash
# Health check
curl https://neo-token-extractor.onrender.com/health

# Extract token
curl -X POST https://neo-token-extractor.onrender.com/api \
  -H "Content-Type: application/json" \
  -d '{"cookies": "c_user=12345; xs=abc123xyz456"}'
