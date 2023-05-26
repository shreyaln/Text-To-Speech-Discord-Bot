import discord
import responses
import PyPDF2
from gtts import gTTS
import os

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = TOKEN

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        # Check if the message contains attachments
        if message.attachments:
            for attachment in message.attachments:
                # Check if the attachment is a PDF file
                if attachment.filename.lower().endswith('.pdf'):
                    try:
                        # Download the PDF file
                        pdf_bytes = await attachment.read()
                        pdf_file_path = 'temp.pdf'
                        mp3_file_path = 'temp.mp3'

                        # Save the PDF file
                        with open(pdf_file_path, 'wb') as pdf_file:
                            pdf_file.write(pdf_bytes)

                        # Convert the PDF to text
                        pdf_text = ""
                        with open(pdf_file_path, 'rb') as pdf_file:
                            pdf_reader = PyPDF2.PdfReader(pdf_file)
                            for page in pdf_reader.pages:
                                pdf_text += page.extract_text()
                        # Clean up the extracted text by removing unnecessary characters
                        pdf_text = " ".join(pdf_text.split())

                        # Convert the text to an MP3 file using gTTS
                        tts = gTTS(text=pdf_text, lang='en')
                        tts.save(mp3_file_path)

                        # Send the MP3 file as a response
                        mp3_file = discord.File(mp3_file_path)
                        await message.channel.send(file=mp3_file)
                    except Exception as e:
                        print(f"Error converting PDF to MP3: {e}")
                    finally:
                        # Cleanup temporary files
                        if os.path.exists(pdf_file_path):
                            os.remove(pdf_file_path)
                        if os.path.exists(mp3_file_path):
                            os.remove(mp3_file_path)

                    return  # Skip further message processing
        
        username = str(message.author)
        user_message = str(message.content)
        print(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")
        
        if user_message and user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, True)
        else: 
            await send_message(message, user_message, False)
        
        # await send_message(message, user_message, is_private = False)
    client.run(TOKEN)

    
