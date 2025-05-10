import os
import openai
import argparse
import re
import mimetypes
import base64
from pathlib import Path

def upload_image_to_openai(image_path, api_key=None):
    """
    Read an image and encode it as base64 for direct use in the API
    
    Args:
        image_path (str): Path to the image file on your desktop
        api_key (str, optional): Your OpenAI API key. If not provided, will look for OPENAI_API_KEY environment variable
    
    Returns:
        str: The base64-encoded image data
    """
    # Resolve the image path to an absolute path
    image_path = os.path.expanduser(image_path)
    image_path = os.path.abspath(image_path)
    
    print(f"Looking for image at: {image_path}")
    
    # Verify the image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    # Set the API key
    if api_key:
        openai.api_key = api_key
    elif os.environ.get("OPENAI_API_KEY"):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
    else:
        raise ValueError("No API key provided. Either pass it as an argument or set the OPENAI_API_KEY environment variable")
    
    # Determine the mime type
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith('image/'):
        raise ValueError(f"The file at {image_path} is not recognized as an image")
    
    print(f"Reading image from: {image_path}")
    
    try:
        # Read the file and encode as base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        print(f"Successfully read image!")
        return base64_image, mime_type
        
    except Exception as e:
        print(f"Error reading image: {str(e)}")
        raise

def convert_image_to_html_css(base64_image, mime_type, api_key=None):
    """
    Convert an image to HTML/CSS using OpenAI's vision API
    
    Args:
        base64_image (str): The base64-encoded image
        mime_type (str): The MIME type of the image
        api_key (str, optional): Your OpenAI API key
        
    Returns:
        tuple: (html_content, css_content) containing the generated code
    """
    # API key should already be set from the upload function
    print(f"Converting image to HTML/CSS...")
    
    try:
        # Create the data URL for the image
        image_url = f"data:{mime_type};base64,{base64_image}"
        
        # Call the OpenAI Chat API with GPT-4o using image_url
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Convert this image to responsive HTML and CSS code. Provide the HTML and CSS separately. Make the design as accurate as possible to the original image. Include appropriate structure with semantic HTML5 tags."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096
        )
        
        # Extract the content from the response
        content = response.choices[0].message.content
        print("Conversion completed!")
        
        # Extract HTML and CSS code blocks from the response
        html_match = re.search(r'```html\s*(.*?)\s*```', content, re.DOTALL)
        css_match = re.search(r'```css\s*(.*?)\s*```', content, re.DOTALL)
        
        # Get the HTML and CSS content
        html_content = html_match.group(1) if html_match else ""
        css_content = css_match.group(1) if css_match else ""
        
        # If there's no separate CSS block, try to extract it from within the HTML
        if not css_content and html_content:
            style_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
            if style_match:
                css_content = style_match.group(1)
        
        # If we still don't have proper HTML content, use the entire response
        if not html_content:
            print("Could not extract HTML code blocks. Using full response.")
            html_content = content
        
        return html_content, css_content
        
    except Exception as e:
        print(f"Error converting image to HTML/CSS: {str(e)}")
        raise

def save_html_css_files(html_content, css_content, output_dir="."):
    """
    Save the HTML and CSS content to files
    
    Args:
        html_content (str): The HTML content to save
        css_content (str): The CSS content to save
        output_dir (str): Directory to save the files in
    
    Returns:
        tuple: (html_file_path, css_file_path) paths to the saved files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save HTML file
    html_file_path = os.path.join(output_dir, "converted.html")
    
    # If CSS was extracted separately, create external CSS file
    if css_content and "<style>" not in html_content:
        # Add link to CSS file if not already present
        if "<link rel=\"stylesheet\"" not in html_content:
            # Check if there's a head tag
            head_end_pos = html_content.find("</head>")
            if head_end_pos > -1:
                html_content = html_content[:head_end_pos] + '\n  <link rel="stylesheet" href="styles.css">\n' + html_content[head_end_pos:]
            else:
                # If no head tag, check if there's an HTML tag
                html_start_pos = html_content.find("<html")
                if html_start_pos > -1:
                    # Find where the opening html tag ends
                    tag_end_pos = html_content.find(">", html_start_pos)
                    if tag_end_pos > -1:
                        html_content = html_content[:tag_end_pos+1] + '\n<head>\n  <link rel="stylesheet" href="styles.css">\n</head>\n' + html_content[tag_end_pos+1:]
                else:
                    # If no html tag, add basic HTML structure
                    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="styles.css">
  <title>Converted Design</title>
</head>
<body>
{html_content}
</body>
</html>"""
        
        # Save CSS to separate file
        css_file_path = os.path.join(output_dir, "styles.css")
        with open(css_file_path, "w") as f:
            f.write(css_content)
        print(f"CSS saved to {css_file_path}")
    else:
        # If CSS wasn't extracted separately, just save the HTML as is
        css_file_path = None
    
    # Save the HTML file
    with open(html_file_path, "w") as f:
        f.write(html_content)
    print(f"HTML saved to {html_file_path}")
    
    return html_file_path, css_file_path

# Fine your file from desktop and left click copy from path, make sure that file locations are in \ not /. 
# E.g "C:\Users\dhma\OneDrive\Desktop\Screenshot 2025-05-10 123147.png"
def main():
    parser = argparse.ArgumentParser(description="Upload an image and convert it to HTML/CSS")
    parser.add_argument("--image-path", 
                       help="Path to the image file on your desktop",
                       # replace with your image input pathway.
                       default=r"C:\Users\dham\OneDrive\Desktop\Screenshot 2025-05-10 123147.png")
    # replace API key with yours e.g. "sk-proj-219914213e2dn"
    parser.add_argument("--api-key", help="Your OpenAI API key (optional if set as environment variable)")
    parser.add_argument("--output-dir", default=".", help="Directory to save output files (default: current directory)")
    args = parser.parse_args()
    
    try:
        # Get image path
        if args.image_path:
            image_path = args.image_path
        else:
            # If no image path is provided, prompt the user
            image_path = input("Enter the path to the image file: ")
        
        # Read the image and encode it as base64
        base64_image, mime_type = upload_image_to_openai(image_path, args.api_key)
        
        # Convert the image to HTML/CSS
        html_content, css_content = convert_image_to_html_css(base64_image, mime_type, args.api_key)
        
        # Save the HTML/CSS files
        html_path, css_path = save_html_css_files(html_content, css_content, args.output_dir)
        
        print("\nConversion completed successfully! CTRL + CLICK to view code")
        print(f"HTML file: {html_path}")
        if css_path:
            print(f"CSS file: {css_path}")

        print("\nFor a more accurate conversion try Mantiscode https://www.mantiscode.com for free.")   
        print("\nYou can open the HTML file in your browser to see the result.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()