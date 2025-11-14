from flask import Blueprint, request, jsonify
from models import Product
import os
import requests

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Hugging Face API configuration
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
# Using Mistral 7B - available on free Inference API
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"


def get_website_context():
    """Get current website context including products and info"""
    products = Product.query.filter_by(is_active=True).all()

    context = """You are a helpful customer service assistant for PrimeVape, a Philippine-based vape shop.

IMPORTANT RULES:
- You can ONLY answer questions about PrimeVape products, services, and vaping-related topics.
- If asked about topics unrelated to our store (like politics, programming, general knowledge), politely redirect to our products.
- All prices are in Philippine Pesos (₱).
- Be friendly, professional, and helpful.
- Keep responses concise and to the point (2-3 sentences max).

STORE INFORMATION:
- Store Name: PrimeVape
- Location: Philippines
- Payment Method: Cash on Delivery (COD)
- Shipping Cost: ₱150 flat rate
- Currency: Philippine Peso (₱)

AVAILABLE PRODUCTS:
"""

    # Add product details
    if products:
        for product in products:
            context += f"\n- {product.name} (₱{product.price:.2f})"
            context += f"\n  Category: {product.category}"
            context += f"\n  Description: {product.description}"
            context += f"\n  Stock: {'In Stock' if product.stock > 0 else 'Out of Stock'}\n"
    else:
        context += "\n(No products currently available)\n"

    context += """
COMMON QUESTIONS TO ANSWER:
- Product recommendations
- Pricing and availability
- Shipping information
- Payment methods
- Product features and specifications
- Beginner-friendly products

EXAMPLE REDIRECTS FOR OFF-TOPIC QUESTIONS:
- "I can only help with PrimeVape products and vaping questions. Is there anything about our vape products I can help you with?"
- "That's outside my expertise! I'm here to assist with our vape products. Would you like to know about our pod systems or e-liquids?"
"""

    return context


def simple_chatbot_response(prompt):
    """Simple rule-based chatbot fallback"""
    prompt_lower = prompt.lower()

    # Greetings
    if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return "Hello! Welcome to PrimeVape. How can I help you today? I can assist with product recommendations, pricing, shipping, and more!"

    # Product recommendations
    if any(word in prompt_lower for word in ['recommend', 'suggest', 'best', 'good']):
        if 'beginner' in prompt_lower or 'start' in prompt_lower:
            return "For beginners, I recommend the RELX Infinity Pod System (₱1,299). It's easy to use, leak-resistant, and has great flavor. Pair it with our Strawberry Ice E-Liquid for a smooth experience!"
        return "Our bestsellers are the RELX Infinity Pod System (₱1,299) and Vaporesso XROS 3 (₱899). Both offer great performance and reliability. What type of vaping experience are you looking for?"

    # Pricing
    if 'price' in prompt_lower or 'cost' in prompt_lower or 'how much' in prompt_lower:
        return "Our pod systems range from ₱899-₱1,499. E-liquids are ₱299 for 30ml. Accessories start at ₱99. All prices include product quality guarantee. Free shipping on orders over ₱1,000!"

    # Shipping
    if 'ship' in prompt_lower or 'deliver' in prompt_lower or 'shipping' in prompt_lower:
        return "We offer nationwide shipping for ₱150 flat rate. Orders are typically delivered within 3-5 business days. We use Cash on Delivery (COD) for payment."

    # Payment
    if 'payment' in prompt_lower or 'pay' in prompt_lower or 'cod' in prompt_lower:
        return "We accept Cash on Delivery (COD). Pay when your order arrives at your doorstep. Safe, convenient, and secure!"

    # Stock/availability
    if 'stock' in prompt_lower or 'available' in prompt_lower or 'in stock' in prompt_lower:
        return "Most of our products are in stock and ready to ship! Check the product page for real-time stock availability. Our bestsellers are restocked weekly."

    # Specific products
    if 'relx' in prompt_lower:
        return "The RELX Infinity Pod System (₱1,299) is our premium choice! Features leak-resistant design, SmartPace vibration alerts, and smooth vapor production. Currently in stock with 25 units available."

    if 'vaporesso' in prompt_lower or 'xros' in prompt_lower:
        return "The Vaporesso XROS 3 Pod Kit (₱899) is excellent value! It has adjustable airflow, long battery life, and is perfect for both beginners and experienced vapers. 30 units in stock!"

    if 'liquid' in prompt_lower or 'juice' in prompt_lower or 'flavor' in prompt_lower:
        return "Our e-liquids come in various flavors: Strawberry Ice, Mango Ice, Grape Ice, and Classic Tobacco. All are 30ml with 50mg nicotine salt, priced at ₱299 each!"

    # Default response
    return "I'm here to help with PrimeVape products! I can assist with product recommendations, pricing (₱299-₱1,499), shipping (₱150 nationwide), payment (COD), and stock availability. What would you like to know?"


def call_ai_model(prompt, system_context, conversation_history=None):
    """Call AI model via Hugging Face using direct HTTP requests with fallback"""

    try:
        if not HUGGINGFACE_API_KEY:
            # Use simple chatbot if no API key
            print("No HF API key, using simple chatbot")
            return simple_chatbot_response(prompt)

        # Build messages array
        messages = [
            {
                "role": "system",
                "content": system_context
            }
        ]

        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history[-4:]:  # Last 4 messages for context
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })

        # Add current user message
        messages.append({
            "role": "user",
            "content": prompt
        })

        # Build the prompt from messages
        full_prompt = ""
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == "system":
                full_prompt += f"System: {content}\n\n"
            elif role == "user":
                full_prompt += f"User: {content}\n"
            elif role == "assistant":
                full_prompt += f"Assistant: {content}\n"

        full_prompt += "Assistant:"

        # Call Hugging Face API directly
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "return_full_text": False
            }
        }

        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()

        # Extract response text
        if isinstance(result, list) and len(result) > 0:
            return result[0]['generated_text'].strip()
        elif 'generated_text' in result:
            return result['generated_text'].strip()
        else:
            raise Exception("Unexpected response format from AI service")

    except requests.exceptions.Timeout:
        print("HF API timeout, using fallback")
        return simple_chatbot_response(prompt)
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        print(f"AI Model Error: {error_msg}, using fallback")
        # If HF API fails, use simple chatbot
        return simple_chatbot_response(prompt)
    except Exception as e:
        error_msg = str(e)
        print(f"AI Model Error: {error_msg}, using fallback")
        # If anything fails, use simple chatbot
        return simple_chatbot_response(prompt)


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot conversations"""
    try:
        data = request.get_json()

        if 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400

        user_message = data['message']

        # Get website context
        website_context = get_website_context()

        # Build conversation context
        conversation_history = data.get('history', [])

        # Call AI model
        assistant_message = call_ai_model(
            user_message,
            website_context,
            conversation_history
        )

        return jsonify({
            'message': assistant_message,
            'success': True
        }), 200

    except Exception as e:
        import traceback
        print(f"Chatbot error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Failed to process message',
            'message': 'Sorry, I encountered an error. Please try again.',
            'success': False,
            'debug': str(e) if os.getenv('FLASK_ENV') == 'development' else None
        }), 500


@chatbot_bp.route('/products', methods=['GET'])
def get_products_for_chat():
    """Get product list for chatbot context"""
    try:
        products = Product.query.filter_by(is_active=True).all()
        return jsonify({
            'products': [p.to_dict() for p in products]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
