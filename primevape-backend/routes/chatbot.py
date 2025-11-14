from flask import Blueprint, request, jsonify
from models import Product
import os
from huggingface_hub import InferenceClient

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Hugging Face API configuration
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
GPT_OSS_MODEL = "meta-llama/Llama-3.2-3B-Instruct"

def get_hf_client():
    """Get Hugging Face client (lazy initialization)"""
    if not HUGGINGFACE_API_KEY:
        return None
    return InferenceClient(token=HUGGINGFACE_API_KEY)


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


def call_ai_model(prompt, system_context, conversation_history=None):
    """Call AI model via Hugging Face (Free Open Source!)"""

    try:
        client = get_hf_client()
        if not client:
            raise Exception("Hugging Face API key not configured. Please add HUGGINGFACE_API_KEY to your .env file.")

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

        # Call Hugging Face Llama 3.2 - FREE open source!
        response = client.chat.completions.create(
            model=GPT_OSS_MODEL,
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )

        # Extract the response text
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Log the error and provide a helpful message
        error_msg = str(e)
        print(f"AI Model Error: {error_msg}")
        raise Exception(f"AI service error: {error_msg}")


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
