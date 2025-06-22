# ⚔️ Stock Market Fighter Creator - Tournament Edition

Transform any publicly traded company into an epic fighting game character! This AI-powered application creates realistic, Mortal Kombat-style fighters based on stock market companies, complete with backstories, combat abilities, artwork, and battle cries.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-Web%20Interface-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎮 Features

- **🥊 Realistic Fighter Generation**: Creates dark, intimidating fighters inspired by Shadow Fight and Mortal Kombat
- **🎨 AI-Generated Artwork**: DALL-E 3 powered character portraits with photorealistic rendering
- **🔊 Voice Acting**: Text-to-speech battle cries with character-appropriate voice selection
- **📊 Educational Content**: Learn about companies through their fighter profiles and combat abilities
- **🌐 Web Interface**: Easy-to-use Gradio interface for creating and viewing fighters
- **⚔️ Tournament Ready**: Dark theme and professional fighting game aesthetics

## 🚀 Demo

Enter any company name or ticker symbol (like `AAPL`, `Tesla`, `Amazon`) and watch as the AI forges a deadly corporate warrior with:

- Detailed combat backstory based on company history
- Fighting style reflecting business model
- Signature moves inspired by company strengths
- Weaknesses based on market vulnerabilities  
- Menacing battle cry with voice acting
- Realistic fighter artwork

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key with access to:
  - GPT-4 (for character generation)
  - DALL-E 3 (for artwork)
  - TTS-1 (for voice synthesis)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-market-fighter-creator.git
   cd stock-market-fighter-creator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   python stock_fighter_creator.py
   ```

The web interface will automatically open in your browser at `http://localhost:7860`

## 📦 Dependencies

Create a `requirements.txt` file with:

```
openai>=1.0.0
gradio>=4.0.0
python-dotenv>=1.0.0
Pillow>=10.0.0
```

## 🎯 Usage

1. **Launch the app** and navigate to the web interface
2. **Enter a company** name or ticker symbol (e.g., "Apple", "TSLA", "Microsoft")
3. **Click "FORGE FIGHTER!"** to generate your warrior
4. **View the results**:
   - Character profile with combat abilities
   - Realistic fighter artwork
   - Downloadable battle cry audio

### Example Companies to Try

**🔥 Tech Titans**: Apple, Microsoft, Google, Amazon, Meta
**⚡ Electric Warriors**: Tesla, Ford, Rivian  
**💰 Financial Assassins**: JPMorgan Chase, Goldman Sachs, Berkshire Hathaway
**🎮 Entertainment Gladiators**: Disney, Netflix, Sony

## 🎨 Character Design Philosophy

Each fighter is designed with:

- **Realistic aesthetics** inspired by modern fighting games
- **Corporate warfare themes** mixing business concepts with martial arts
- **Educational value** teaching about company business models through combat abilities
- **Dark, mature tone** suitable for serious fighting tournaments
- **Detailed combat gear** reflecting company identity and market position

## 🔧 Customization

### Modify Fighting Styles

Edit the `system_message` variable to adjust character generation:
- Change tone (dark/light, serious/humorous)
- Adjust detail level (brief/comprehensive)
- Modify fighting game references

### Adjust Artwork Style

Modify the `fighter_artist()` function prompts:
- Change art style (realistic/anime/pixel art)
- Adjust lighting and atmosphere
- Modify character poses and expressions

### Voice Selection

Customize voice mapping in `select_fighter_voice()`:
- Add new voice types
- Modify selection criteria
- Adjust speech speed and tone

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

- This is an educational and entertainment project
- Not financial advice - fighters are fictional representations
- Requires OpenAI API credits for full functionality
- Generated content reflects AI interpretation, not official company positions

## 🐛 Troubleshooting

### Common Issues

**API Key Issues**
- Ensure your OpenAI API key is valid and has sufficient credits
- Check that the key is properly set in your `.env` file

**Image Generation Fails**
- DALL-E 3 has content policies - some prompts may be rejected
- The app includes fallback prompts for failed generations

**Audio Playback Issues**
- Audio files are saved locally and opened with system default player
- Ensure your system can play MP3 files

**Gradio Interface Issues**
- Try refreshing the browser page
- Check console for JavaScript errors
- Ensure all dependencies are properly installed

## 🙏 Acknowledgments

- OpenAI for GPT-4, DALL-E 3, and TTS-1 APIs
- Gradio team for the excellent web interface framework
- Fighting game community for inspiration (Mortal Kombat, Shadow Fight, Tekken)
- Stock market data providers for company information

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/stock-market-fighter-creator/issues) page
2. Create a new issue with detailed description
3. Include error messages and system information

---

**Ready to build your corporate fighting tournament roster? Let the market battles begin! ⚔️**