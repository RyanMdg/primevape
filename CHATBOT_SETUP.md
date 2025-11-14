# AI Chatbot Setup Guide

## Overview
Your PrimeVape website now has an AI-powered chatbot assistant using **Claude AI from Anthropic**. The chatbot can only answer questions about your vape shop products and services.

## Features
✅ **Product-Specific Answers**: Only answers questions about PrimeVape products
✅ **Smart Redirects**: Politely redirects off-topic questions back to products
✅ **Real-time Product Data**: Uses current product information from database
✅ **Conversational**: Maintains conversation history
✅ **Floating UI**: Clean black & white chat interface in bottom-right corner

---

## Setup Instructions

### Step 1: Get Your Anthropic API Key

1. Go to: **https://console.anthropic.com/**
2. Sign in or create an account
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-...`)

### Step 2: Add API Key to Backend

1. Open the file: `/primevape-backend/.env`
2. Find the line: `ANTHROPIC_API_KEY=your-anthropic-api-key-here`
3. Replace `your-anthropic-api-key-here` with your actual API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...
   ```
4. Save the file

### Step 3: Restart Backend Server

The Flask backend will automatically reload when you save the `.env` file. If not, restart it manually:

```bash
cd primevape-backend
source venv/bin/activate
python app.py
```

### Step 4: Test the Chatbot

1. Open your website: **http://localhost:5173**
2. Look for the **black circular button** in the bottom-right corner
3. Click it to open the chat window
4. Try asking questions like:
   - "What vape pods do you have?"
   - "How much does RELX Infinity cost?"
   - "Do you have strawberry flavored e-liquids?"
   - "What's your shipping cost?"
   - "Tell me about your accessories"

---

## How It Works

### Backend (`/primevape-backend/routes/chatbot.py`)

The chatbot endpoint:
- **URL**: `POST /api/chatbot/chat`
- **Uses**: Claude 3.5 Sonnet model
- **Context**: Automatically includes all active products, pricing, and store info
- **Restrictions**: Configured to ONLY answer questions about PrimeVape

### Frontend (`/primevape-frontend/src/components/Chatbot.jsx`)

The chat UI:
- **Floating button**: Toggle chat window
- **Message history**: Keeps last 10 messages for context
- **Real-time responses**: Shows typing indicator while Claude thinks
- **Clean design**: Matches your black & white aesthetic

---

## What the Chatbot CAN Do

✅ Recommend products based on user needs
✅ Provide pricing and availability information
✅ Explain product features and specifications
✅ Share shipping and payment details
✅ Help beginners choose starter products
✅ Compare different products
✅ Answer vaping-related questions

## What the Chatbot CANNOT Do

❌ Answer general knowledge questions (e.g., "Who is the president?")
❌ Teach programming or other off-topic subjects
❌ Process orders (it only provides information)
❌ Access user account data
❌ Make actual product recommendations without context

---

## Example Conversations

### ✅ Good Questions (Will Answer)
```
User: "What's the cheapest e-liquid you have?"
Bot: "Our most affordable e-liquid is the Classic Tobacco 50ml at ₱599.00..."

User: "I'm new to vaping. What should I buy?"
Bot: "For beginners, I'd recommend the JUUL Starter Kit at ₱1,299..."

User: "Do you ship to Manila?"
Bot: "Yes! We ship throughout the Philippines with a flat rate of ₱150..."
```

### ❌ Off-Topic Questions (Will Redirect)
```
User: "Teach me JavaScript"
Bot: "That's outside my expertise! I'm here to assist with our vape products. Would you like to know about our pod systems or e-liquids?"

User: "Who is the president?"
Bot: "I can only help with PrimeVape products and vaping questions. Is there anything about our vape products I can help you with?"
```

---

## Customization

### Update Store Information

Edit `/primevape-backend/routes/chatbot.py` in the `get_website_context()` function:

```python
STORE INFORMATION:
- Store Name: PrimeVape
- Location: Philippines
- Payment Method: Cash on Delivery (COD)
- Shipping Cost: ₱150 flat rate
```

### Change AI Model

In `chatbot.py`, you can change the model:

```python
response = anthropic_client.messages.create(
    model="claude-3-5-sonnet-20241022",  # Change this
    max_tokens=1024,
    ...
)
```

Available models:
- `claude-3-5-sonnet-20241022` (Best quality, recommended)
- `claude-3-opus-20240229` (Most capable, slower)
- `claude-3-haiku-20240307` (Fastest, cheaper)

### Adjust Response Length

Change `max_tokens` to control response length:
- `512` = Shorter responses
- `1024` = Medium (current setting)
- `2048` = Longer, detailed responses

---

## Costs

**Anthropic Claude Pricing** (as of 2024):
- **Claude 3.5 Sonnet**: ~$3 per million input tokens, ~$15 per million output tokens
- **Typical chat message**: ~500-1000 tokens total
- **Estimated cost**: $0.005-0.02 per conversation

💡 **Cost Saving Tips**:
1. Use Claude 3 Haiku for lower costs
2. Reduce `max_tokens` to limit response length
3. Keep conversation history to last 5-10 messages only
4. Set usage limits in Anthropic Console

---

## Troubleshooting

### Chatbot Button Not Showing
1. Check browser console for errors
2. Make sure `/components/Chatbot.jsx` is imported in `App.jsx`
3. Clear browser cache and refresh

### "Failed to process message" Error
1. Verify API key is correct in `.env` file
2. Check backend server is running: `http://localhost:5001`
3. Check Anthropic API status: https://status.anthropic.com/
4. Check backend logs for detailed error

### Off-Topic Questions Getting Answered
1. Update the system prompt in `get_website_context()`
2. Make the restrictions more explicit
3. Add more example redirects

### Chatbot Responds Slowly
1. This is normal - Claude typically responds in 2-5 seconds
2. Consider using Claude 3 Haiku for faster responses
3. Reduce `max_tokens` for shorter responses

---

## Files Modified/Created

### Backend
- ✅ `routes/chatbot.py` - Chatbot API endpoint
- ✅ `app.py` - Registered chatbot blueprint
- ✅ `.env` - Added ANTHROPIC_API_KEY

### Frontend
- ✅ `components/Chatbot.jsx` - Chat UI component
- ✅ `App.jsx` - Added Chatbot component
- ✅ `index.css` - Added chatbot styles

---

## Security Notes

🔒 **API Key Security**:
- Never commit `.env` file to version control
- Keep your API key private
- Rotate keys if exposed
- Set spending limits in Anthropic Console

🔒 **User Privacy**:
- Chat history is NOT stored in database
- Conversations are sent to Anthropic API
- Review Anthropic's privacy policy: https://www.anthropic.com/privacy

---

## Next Steps

1. **Add API key** to `.env` file
2. **Test the chatbot** on your website
3. **Customize responses** in `get_website_context()`
4. **Monitor usage** in Anthropic Console
5. **Set spending limits** to avoid unexpected costs

---

**Need Help?**
- Anthropic Docs: https://docs.anthropic.com/
- API Reference: https://docs.anthropic.com/claude/reference/
- Support: support@anthropic.com

**Your chatbot is ready! Just add your API key and start chatting! 🤖**
