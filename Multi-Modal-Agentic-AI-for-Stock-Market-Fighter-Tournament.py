# Stock Market Fighter Character Creator - Enhanced Fighting Game Style

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Some imports for handling images
import base64
from io import BytesIO
from PIL import Image

# Some imports for handling audio
import tempfile
import os
import webbrowser
from datetime import datetime

# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4o-mini"
openai = OpenAI()

system_message = """You are a creative character designer for a dark, mature fighting game based on stock market companies, similar to Mortal Kombat or Shadow Fight. 
When given a company ticker symbol or name, create a detailed fighter character profile including:
1. Fighter name and dark/mysterious backstory with corporate themes
2. Brutal fighting style and signature finishing moves
3. Strengths based on company advantages (presented as combat abilities)
4. Weaknesses based on company vulnerabilities (presented as combat weaknesses)
5. A menacing catchphrase or battle cry
6. Detailed physical appearance description emphasizing combat gear, scars, weapons, and intimidating features

Make the character dark, gritty, and intimidating while still being educational about the company's business model. Think corporate warfare meets martial arts tournament. Keep responses engaging and around 300-400 words with emphasis on combat details."""

# Tool for generating fighter characters
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_fighter_character",
            "description": "Generate a fighting character based on a stock market company",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": "The company name or ticker symbol to create a fighter for"
                    }
                },
                "required": ["company"]
            }
        }
    }
]

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    
    if function_name == "create_fighter_character":
        company = function_args["company"]
        result_message = f"Forging a deadly warrior from the essence of {company}..."
        
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result_message
        }, company
    
    return None, None

def fighter_artist(company, character_description):
    """Generate realistic fighting game character artwork using DALL-E"""
    try:
        # Create a dark, realistic fighting game prompt
        company_safe = "".join(c for c in company if c.isalnum() or c in (' ', '-', '_')).strip()
        
        # Extract key visual elements from character description
        desc_lower = character_description.lower()
        
        # Determine fighting style elements
        style_elements = []
        if 'ninja' in desc_lower or 'shadow' in desc_lower:
            style_elements.append("ninja assassin")
        if 'armor' in desc_lower or 'metal' in desc_lower:
            style_elements.append("armored warrior")
        if 'tech' in desc_lower or 'cyber' in desc_lower:
            style_elements.append("cyberpunk fighter")
        if 'suit' in desc_lower or 'corporate' in desc_lower:
            style_elements.append("corporate warrior")
        
        style_desc = ", ".join(style_elements) if style_elements else "martial arts fighter"
        
        # Enhanced prompt for realistic fighting game character
        image_prompt = f"""A powerful {style_desc} inspired by {company_safe}, in the style of Mortal Kombat or Tekken character design. 
        Realistic 3D rendered fighter with detailed combat gear, battle scars, and intimidating presence. 
        Dark atmospheric lighting, dramatic pose in fighting stance, 
        professional video game character concept art, highly detailed textures, 
        muscular build, combat-ready outfit with corporate-themed elements, 
        fierce expression, tournament fighter aesthetic, 
        photorealistic rendering style, dark background with subtle lighting effects."""
        
        print(f"🎨 Generating realistic fighter with prompt: {image_prompt[:100]}...")
        
        image_response = openai.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            n=1,
            response_format="b64_json",
        )
        image_base64 = image_response.data[0].b64_json
        image_data = base64.b64decode(image_base64)
        return Image.open(BytesIO(image_data))
        
    except Exception as e:
        print(f"Error generating image: {e}")
        print("Trying alternative realistic prompt...")
        
        # Fallback with simpler but still realistic prompt
        try:
            fallback_prompt = f"""A fierce martial arts warrior representing {company_safe}, 
            realistic fighting game character design, detailed combat outfit, 
            professional fighter appearance, dramatic lighting, 
            3D rendered game character style"""
            
            image_response = openai.images.generate(
                model="dall-e-3",
                prompt=fallback_prompt,
                size="1024x1024",
                n=1,
                response_format="b64_json",
            )
            image_base64 = image_response.data[0].b64_json
            image_data = base64.b64decode(image_base64)
            return Image.open(BytesIO(image_data))
            
        except Exception as e2:
            print(f"Fallback also failed: {e2}")
            return None

def select_fighter_voice(company, character_description):
    """Select appropriate voice based on character gender and fighting style"""
    description_lower = character_description.lower()
    
    # Determine gender from character description
    male_indicators = ['he ', 'his ', 'him ', 'man', 'male', 'guy', 'brother', 'father', 'king', 'lord', 'warrior', 'knight']
    female_indicators = ['she ', 'her ', 'woman', 'female', 'girl', 'sister', 'mother', 'queen', 'lady', 'princess', 'goddess']
    
    is_male = any(indicator in description_lower for indicator in male_indicators)
    is_female = any(indicator in description_lower for indicator in female_indicators)
    
    # Select voice based on character type and fighting style
    if is_female:
        # Female voices: nova (clean/tech), shimmer (dramatic/powerful)
        if any(word in description_lower for word in ['assassin', 'shadow', 'stealth', 'ninja']):
            return "nova"  # Clean, controlled female voice for stealthy fighters
        elif any(word in description_lower for word in ['brutal', 'fierce', 'dominating', 'crushing']):
            return "shimmer"  # More dramatic female voice for aggressive fighters
        else:
            return "nova"  # Default clean female voice
    
    elif is_male:
        # Male voices: onyx (deep/powerful), echo (authoritative)
        if any(word in description_lower for word in ['brutal', 'crushing', 'dominating', 'destroyer']):
            return "onyx"  # Deep, menacing male voice for brutal fighters
        elif any(word in description_lower for word in ['strategic', 'calculated', 'precise', 'mastermind']):
            return "echo"  # Authoritative male voice for tactical fighters
        else:
            return "onyx"  # Default powerful male voice
    
    else:
        # If gender unclear, use versatile voice
        return "alloy"  # Versatile unisex voice

def catchphrase_speaker(catchphrase, company, character_description):
    """Generate menacing audio for the fighter's battle cry"""
    try:
        # Select voice based on character
        voice = select_fighter_voice(company, character_description)
        
        # Make catchphrase more menacing and fighting-focused
        if not any(word in catchphrase.lower() for word in ['fight', 'battle', 'defeat', 'destroy', 'crush', 'dominate']):
            dramatic_catchphrase = f"{catchphrase} Prepare for battle!"
        else:
            dramatic_catchphrase = catchphrase
        
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=dramatic_catchphrase,
            speed=0.9  # Slightly slower for more dramatic effect
        )
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_company = "".join(c for c in company if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"fighter_{safe_company}_{timestamp}.mp3"
        
        # Save audio file
        with open(filename, "wb") as f:
            f.write(response.content)
        
        print(f"🎵 Battle cry saved as: {filename}")
        
        # Play with system player
        print("⚔️ Playing battle cry...")
        webbrowser.open(filename)
        
        return filename, voice
        
    except Exception as e:
        print(f"Error generating battle cry: {e}")
        return None, None

def chat(history):
    messages = [{"role": "system", "content": system_message}] + history
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    image = None
    audio_file = None
    audio_info = ""
    
    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response_msg, company = handle_tool_call(message)
        messages.append(message)
        messages.append(response_msg)
        
        # Generate the character profile
        response = openai.chat.completions.create(model=MODEL, messages=messages)
        character_profile = response.choices[0].message.content
        
        # Generate realistic fighter artwork
        image = fighter_artist(company, character_profile)
        
        # Extract catchphrase/battle cry for audio
        lines = character_profile.split('\n')
        catchphrase = "Your portfolio ends here!"  # Default battle cry
        for line in lines:
            if any(keyword in line.lower() for keyword in ['catchphrase', 'battle cry', 'signature phrase', 'says']):
                if '"' in line:
                    # Extract text between quotes
                    start = line.find('"')
                    end = line.rfind('"')
                    if start != -1 and end != -1 and start != end:
                        catchphrase = line[start+1:end]
                        break
                elif ':' in line and len(line.split(':', 1)[1].strip()) > 0:
                    # Extract text after colon
                    catchphrase = line.split(':', 1)[1].strip().strip('"')
                    break
        
        # Generate and play battle cry
        audio_file, voice_used = catchphrase_speaker(catchphrase, company, character_profile)
        if audio_file:
            audio_info = f"\n\n⚔️ **Battle Cry Generated:** {audio_file}\n🎭 **Voice:** {voice_used.upper()}\n📢 **Phrase:** \"{catchphrase}\""
        
        reply = character_profile + audio_info
        history += [{"role": "assistant", "content": reply}]
        
        return history, image, audio_file
    
    reply = response.choices[0].message.content
    history += [{"role": "assistant", "content": reply}]
    
    return history, image, audio_file

# Enhanced Gradio interface for realistic Stock Market Fighters

with gr.Blocks(title="Stock Market Fighter Creator - Tournament Edition") as ui:
    gr.Markdown("# ⚔️ Stock Market Fighter Creator - Tournament Edition")
    gr.Markdown("**Enter a company name or ticker to forge a deadly warrior for the Corporate Combat Championship!**")
    gr.Markdown("*Realistic fighting game characters inspired by Shadow Fight and Mortal Kombat*")
    
    with gr.Row():
        chatbot = gr.Chatbot(height=500, type="messages", label="⚡ Fighter Dossier")
        image_output = gr.Image(height=500, label="🥊 Fighter Portrait")
    
    with gr.Row():
        audio_download = gr.File(label="⚔️ Download Battle Cry Audio", interactive=False)
    
    with gr.Row():
        entry = gr.Textbox(
            label="🏢 Enter Company Name or Ticker Symbol:",
            placeholder="Forge a warrior: AAPL, Tesla, Amazon, Microsoft..."
        )
    
    with gr.Row():
        create_btn = gr.Button("⚔️ FORGE FIGHTER! ⚔️", variant="primary", size="lg")
        clear = gr.Button("🔄 Clear Arena", variant="secondary")

    def do_entry(message, history):
        if not message.strip():
            return "", history
        # Format the message as a fighter creation request
        formatted_message = f"Create a deadly fighting tournament character for {message}"
        history += [{"role": "user", "content": formatted_message}]
        return "", history

    def create_fighter(message, history):
        if message.strip():
            new_history = do_entry(message, history)
            result = chat(new_history[1])
            if len(result) == 3:
                return result[0], result[1], result[2]  # history, image, audio_file
            else:
                return result[0], result[1], None  # fallback
        return history, None, None

    entry.submit(do_entry, inputs=[entry, chatbot], outputs=[entry, chatbot]).then(
        chat, inputs=chatbot, outputs=[chatbot, image_output, audio_download]
    )
    
    create_btn.click(create_fighter, inputs=[entry, chatbot], outputs=[chatbot, image_output, audio_download])
    clear.click(lambda: (None, None, None), inputs=None, outputs=[chatbot, image_output, audio_download], queue=False)

# Tournament roster suggestions
with ui:
    gr.Markdown("""
    ### 🏆 **TOURNAMENT ROSTER SUGGESTIONS:**
    
    **🔥 TECH TITANS:**  
    Apple (AAPL) • Microsoft (MSFT) • Google (GOOGL) • Amazon (AMZN) • Meta (META)
    
    **⚡ ELECTRIC WARRIORS:**  
    Tesla (TSLA) • Ford (F) • General Motors (GM) • Rivian (RIVN)
    
    **💰 FINANCIAL ASSASSINS:**  
    JPMorgan Chase (JPM) • Goldman Sachs (GS) • Berkshire Hathaway (BRK.A) • Bank of America (BAC)
    
    **🎮 ENTERTAINMENT GLADIATORS:**  
    Disney (DIS) • Netflix (NFLX) • Sony (SONY) • Activision Blizzard
    
    **⚔️ Create your ultimate corporate fighting tournament roster!**
    """)

if __name__ == "__main__":
    ui.launch(inbrowser=True)