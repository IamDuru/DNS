import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image
from io import BytesIO
from DnsXMusic import app

# Function to generate buttons for model selection
def generate_buttons(prompt):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Aɴɪᴍᴇ", callback_data=f"anime:{prompt}")],
            [InlineKeyboardButton("𝟹D Rᴇɴᴅᴇʀ", callback_data=f"3d:{prompt}")],
            [InlineKeyboardButton("RᴇᴀʟCᴀʀᴛᴏᴏɴ𝟹D", callback_data=f"realcartoon:{prompt}")]
        ]
    )
    return buttons

# Function to get images from the API and combine them into a 2x2 collage
def get_and_combine_images(api_url, count=4):
    images = []
    for _ in range(count):
        response = requests.get(api_url)
        response.raise_for_status()
        image_url = response.json().get('image')
        if image_url:
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            images.append(img)
    
    # Create a 2x2 grid collage if we have 4 images
    if len(images) == 4:
        widths, heights = zip(*(img.size for img in images))
        max_width = max(widths) * 2
        total_height = max(heights) * 2

        collage = Image.new('RGB', (max_width, total_height))

        # Paste the images in a 2x2 grid
        collage.paste(images[0], (0, 0))
        collage.paste(images[1], (max_width // 2, 0))
        collage.paste(images[2], (0, total_height // 2))
        collage.paste(images[3], (max_width // 2, total_height // 2))

        return collage
    else:
        return None

# Function to create "🔄️ Rᴇɢᴇɴᴇʀᴀᴛᴇ 🔄️" button
def regenerate_button(model, prompt):
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄️ Rᴇɢᴇɴᴇʀᴀᴛᴇ 🔄️", callback_data=f"regenerate:{model}:{prompt}")]]
    )
    return buttons

# Command handler for image generation
@app.on_message(filters.command(["make", "ake"], prefixes=["/", "!", ".", "M", "m"]))
async def handle_image_generation(client, message):
    prompt = ' '.join(message.command[1:])
    if not prompt:
        await message.reply_text('ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʀᴏᴍᴘᴛ.')
        return
    buttons = generate_buttons(prompt)
    await message.reply_text("Please select an image style:", reply_markup=buttons)

# Callback handler for button presses
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data
    parts = data.split(":")

    # Initialize filter_type and prompt variables
    filter_type = None
    prompt = None
    
    if len(parts) == 2:  # For the first image generation buttons
        filter_type, prompt = parts
    elif len(parts) == 3:  # For the regenerate button
        _, filter_type, prompt = parts
    else:
        await callback_query.message.reply_text("Invalid data format.")
        return
    
    # Ensure filter_type is assigned
    if not filter_type or not prompt:
        await callback_query.message.reply_text("An error occurred: Invalid filter type or prompt.")
        return

    # Display a waiting message
    wait_message = await callback_query.message.edit_text("Iᴍᴀɢᴇ Is Gᴇɴᴇʀᴀᴛɪɴɢ Pʟᴇᴀsᴇ Wᴀɪᴛ......")
    
    # Determine the API URL based on the model selected
    try:
        if filter_type == "anime":
            api_url = f"https://animeimg.apiitzasuraa.workers.dev/?prompt={prompt}"
            model_name = "Aɴɪᴍᴇ"
        elif filter_type == "3d":
            api_url = f"https://3d-image.apiitzasuraa.workers.dev/?prompt={prompt}"
            model_name = "𝟹D Rᴇɴᴅᴇʀ"
        elif filter_type == "realcartoon":
            api_url = f"https://magicimg.apiitzasuraa.workers.dev/?prompt={prompt}"
            model_name = "RᴇᴀʟCᴀʀᴛᴏᴏɴ𝟹D"
        else:
            await callback_query.message.reply_text("Invalid option selected.")
            return
    
    try:
        # Generate the 4-image collage
        collage = get_and_combine_images(api_url, count=4)
        
        # Remove the 'Generating' message
        await client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=wait_message.id)

        if collage:
            # Save the collage in memory and send it
            collage_bytes = BytesIO()
            collage.save(collage_bytes, format="PNG")
            collage_bytes.seek(0)
            
            await client.send_photo(chat_id=callback_query.message.chat.id, photo=collage_bytes)

            # Add regenerate button
            regenerate_markup = regenerate_button(filter_type, prompt)
            
            # Send details and regenerate button
            model_text = f"𝐌𝐨𝐝𝐞𝐥: {model_name}\n"
            prompt_text = f"𝐏𝐫𝐨𝐦𝐩𝐭: `{prompt}`\n"
            user_text = f"𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐁𝐲: {callback_query.from_user.mention}\n"
            
            caption = f"{model_text}{prompt_text}{user_text}"
            
            await callback_query.message.reply_text(caption, reply_markup=regenerate_markup)
        else:
            await callback_query.message.reply_text("No image found.")
    except Exception as e:
        await callback_query.message.reply_text(f"An error occurred: {e}")
