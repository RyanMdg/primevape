# Hugging Face Chatbot Setup Guide - Mistral-7B

## Overview
Your PrimeVape chatbot now uses **Mistral-7B-Instruct** from Hugging Face - a powerful open-source AI model that's **FREE to use**!

## ✅ What Changed
- ❌ Removed: Anthropic Claude (requires paid credits)
- ✅ Added: Hugging Face Mistral-7B-Instruct (FREE!)
- ✅ Same features: Product-only responses, conversation history, smart redirects

---

## 🎯 How to Get Your FREE Hugging Face API Key

### Step 1: Create Hugging Face Account

1. Go to: **https://huggingface.co/**
2. Click **"Sign Up"** in the top right
3. Create a free account with your email

### Step 2: Generate API Token

1. After logging in, click on your **profile picture** (top right)
2. Go to **"Settings"**
3. Click **"Access Tokens"** in the left sidebar
4. Click **"New token"** button
5. Give it a name (e.g., "PrimeVape Chatbot")
6. Select role: **"Read"** (this is enough for inference)
7. Click **"Generate token"**
8. **Copy the token** - it starts with `hf_...`

### Step 3: Add API Key to Your Project

1. Open file: `/primevape-backend/.env`
2. Find the line: `HUGGINGFACE_API_KEY=your-huggingface-api-key-here`
3. Replace with your token:
   ```
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
4. Save the file

### Step 4: Restart Backend Server

```bash
cd primevape-backend
# Kill the current server (Ctrl+C if running)
source venv/bin/activate
python app.py
```

### Step 5: Test the Chatbot!

1. Open: **http://localhost:5173**
2. Click the **black chat button** in bottom-right corner
3. Ask questions like:
   - "What vape pods do you have?"
   - "How much is the RELX Infinity?"
   - "I'm new to vaping, what do you recommend?"

---

## 🆓 Pricing - It's FREE!

**Hugging Face Inference API:**
- ✅ **FREE tier** with rate limits
- ✅ **No credit card required**
- ✅ Generous limits for personal projects
- ✅ 1000s of free requests per day

**Rate Limits (Free Tier):**
- ~1000 requests per day
- Perfect for a small e-commerce chatbot
- Resets every 24 hours

**Want Unlimited?**
- Hugging Face PRO: $9/month (optional, not needed for this project)

---

## 🤖 About Mistral-7B-Instruct

**Model:** `mistralai/Mistral-7B-Instruct-v0.2`

**Capabilities:**
- 7 billion parameters
- Instruction-tuned for conversations
- Fast responses (2-5 seconds)
- Good at following instructions
- Supports multi-turn conversations

**Perfect for:**
- Customer service chatbots
- Product recommendations
- FAQ answering
- E-commerce support

---

## 📋 Quick Start Guide

**1. Get API Key (2 minutes):**
   - Sign up at https://huggingface.co/
   - Go to Settings → Access Tokens
   - Create new token (Read permissions)
   - Copy the token (starts with `hf_...`)

**2. Add to .env file:**
   ```
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**3. Restart backend:**
   ```bash
   python app.py
   ```

**4. Test chatbot:**
   - Open http://localhost:5173
   - Click chat button
   - Ask about products!

---

## 🔧 Technical Details

### API Endpoint Used:
```
https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2
```

### Request Format:
```python
{
    "inputs": "<s>[INST] {system_context} User question: {question} [/INST]",
    "parameters": {
        "max_new_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.95
    }
}
```

### Response Format:
```python
[{
    "generated_text": "AI response here..."
}]
```

---

## ⚙️ Customization

### Change Response Length

In `/routes/chatbot.py`, modify `max_new_tokens`:

```python
"parameters": {
    "max_new_tokens": 500,  # Change this (250-1000)
    "temperature": 0.7,
    "top_p": 0.95
}
```

- `250` = Shorter responses
- `500` = Medium (current)
- `1000` = Longer, detailed responses

### Make Responses More Creative

Adjust `temperature`:

```python
"temperature": 0.7,  # Change this (0.1-1.0)
```

- `0.3` = More focused, consistent
- `0.7` = Balanced (current)
- `0.9` = More creative, varied

### Use a Different Model

Replace the model URL in `chatbot.py`:

```python
# Current:
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# Other options:
# Smaller/Faster:
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"

# Larger/Better:
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
```

---

## 🐛 Troubleshooting

### "Model is currently loading" Error

**Problem:** Hugging Face models "sleep" when unused

**Solution:** Wait 20-30 seconds and try again. First request wakes up the model.

**Fix:** Send a test request when server starts:
```python
# In chatbot.py, add at bottom:
def warmup_model():
    try:
        call_mistral("Hello", "You are a helpful assistant.")
    except:
        pass

warmup_model()  # Wakes up the model
```

### "Rate limit exceeded" Error

**Problem:** Free tier has limits

**Solutions:**
1. Wait a few minutes and try again
2. Upgrade to HuggingFace PRO ($9/month)
3. Use a different model
4. Implement request caching

### Slow Responses

**Expected:** First request takes 10-30 seconds (model loading)

**Subsequent requests:** 2-5 seconds

**To improve:**
- Use smaller model (Phi-3-mini)
- Reduce `max_new_tokens`
- Upgrade to HuggingFace PRO for faster inference

### API Key Not Working

**Check:**
1. Token starts with `hf_`
2. Token has "Read" permissions
3. No extra spaces in `.env` file
4. Backend server restarted after adding key

---

## 🔒 Security

**API Key Safety:**
- ✅ Stored in `.env` file
- ✅ Not committed to git (.env is in .gitignore)
- ✅ Server-side only (not exposed to frontend)
- ⚠️ Keep your token private
- ⚠️ Regenerate if accidentally exposed

**Recommended:**
- Don't share your `.env` file
- Use different tokens for dev/production
- Rotate tokens periodically

---

## 📊 Comparison: Mistral vs Claude

| Feature | Mistral-7B (HF) | Claude 3.5 Sonnet |
|---------|----------------|-------------------|
| **Cost** | FREE | ~$3-15 per million tokens |
| **Speed** | 2-5 seconds | 2-4 seconds |
| **Quality** | Very Good | Excellent |
| **Rate Limits** | 1000/day (free) | Based on credits |
| **Setup** | Simple | Simple |
| **Best For** | Small projects | Production apps |

**Verdict:** Mistral is perfect for your vape shop chatbot!

---

## ✅ Files Modified

### Backend:
- ✅ `/routes/chatbot.py` - Switched to Hugging Face API
- ✅ `/.env` - Changed to HUGGINGFACE_API_KEY
- ✅ Installed: `huggingface-hub`, `requests`
- ✅ Removed: `anthropic` package

### Frontend:
- ✅ `/components/Chatbot.jsx` - Updated header to say "Powered by Mistral AI"

---

## 🚀 You're All Set!

**Just 3 steps:**
1. Get your FREE Hugging Face API key: https://huggingface.co/settings/tokens
2. Add it to `.env` file
3. Restart backend and start chatting!

**No credit card. No billing. Completely FREE.** 🎉

---

## 📚 Useful Links

- **Hugging Face Signup**: https://huggingface.co/join
- **API Tokens**: https://huggingface.co/settings/tokens
- **Mistral Model**: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
- **HF Inference API Docs**: https://huggingface.co/docs/api-inference/index
- **Model Explorer**: https://huggingface.co/models?pipeline_tag=text-generation

---

**Happy Chatting! Your AI assistant is ready! 🤖**
