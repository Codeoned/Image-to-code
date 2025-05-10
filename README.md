# Screenshot-to-Code

Upload a screenshot and convert it to clean HTML & CSS, including Figma frames. Runs directly with the GPT-4 API 
no Plus plan needed!
<a href="https://youtu.be/X2BYD6TrREU" target="_blank">
    <img src="https://img.youtube.com/vi/X2BYD6TrREU/hqdefault.jpg" alt="Watch the video">
</a>

**for more Accurate Conversions**: Custom-trained AI model with 95% accuracy.
 **Try for Free**: Visit [Mantiscode](https://mantiscode.com).

## Features

* **Direct API Integration**: Utilizes OpenAI GPT-4 API.
* **Supported Models**: GPT 4o, HTML/CSS.

## Prerequisites

* Python v3.13.2 or higher.
* Visual Studio Code (VS Code).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Codeoned/screenshot-to-code.git
   ```
2. Navigate to the project directory:

   ```bash
   cd screenshot-to-code
   ```
3. Install dependencies:

   ```bash
   pip install openai argparse
   ```

## How to Run

1. Open the Python file **"screenshot\_to\_code.py"** in your IDE (VS Code recommended).
2. Locate your image file on your PC and copy its path (e.g., `C:\Users\dham\OneDrive\Desktop\Screenshot.png`).

   * Replace the file path on **line 197** in the script.
   * Ensure file separators are `\` and not `/`.
3. Add your OpenAI API key on **line 199**:

   ```python
   help = "Your OpenAI API key (optional if set as environment variable)"
   ```

   * [How to get your API key](https://github.com/Codeoned/screenshot-to-code/blob/main/Key.md)
4. Run the script:

   ```bash
   python screenshot_to_code.py
   ```
5. Your HTML/CSS code will be generated within 1-2 minutes.

## FIGMA TO HTML/CSS
<a href="https://youtu.be/zkr-rGoi4NA" target="_blank">
    <img src="https://img.youtube.com/vi/zkr-rGoi4NA/hqdefault.jpg" alt="Watch the video">
</a>

## Troubleshooting

* If you encounter issues, please open a new issue on the [GitHub repository](https://github.com/Codeoned/screenshot-to-code/issues).

## Contributing

Contributions are welcome! Feel free to fork the project and submit pull requests.

## License

This project is licensed under the MIT License.



