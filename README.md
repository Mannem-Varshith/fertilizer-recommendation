# 🌱 Fertilizer Recommendation System

A Streamlit-based web application that recommends the best fertilizer based on crop type and soil NPK values.

## 🚀 Features

- **Crop Selection**: Choose from 15+ different crops
- **NPK Input**: Input your soil's Nitrogen, Phosphorus, and Potassium values
- **Smart Recommendations**: Get fertilizer recommendations based on similarity scoring
- **Visual Analysis**: Interactive charts and comparisons
- **Detailed Analysis**: Gap analysis and detailed breakdowns

## 📊 Available Crops

- Rice, Maize, Soyabean
- Brinjal, Cabbage, Cucumber
- Onion, Potato, Garlic, Tomato
- Ginger, Turmeric, Cotton, Sunflower

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project files**
   ```
   # Make sure you have these files in your directory:
   - app.py
   - requirements.txt
   - Fertilizer_Composition_For_Model.csv
   - Filtered_Fertilizer.csv
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python -m streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, manually navigate to the URL

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended) ✅

1. **Your GitHub repository is ready**: `https://github.com/Mannem-Varshith/fertilizer-recommendation.git`

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `Mannem-Varshith/fertilizer-recommendation`
   - Set the path to your app: `app.py`
   - Click "Deploy!"
   - Your app will be live at: `https://your-app-name.streamlit.app`

### Option 2: Heroku

1. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy to Heroku**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Local Deployment

For local deployment with custom settings:

```bash
python -m streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

## 📁 File Structure

```
fertilizer-recommender/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── README.md                          # This file
├── Fertilizer_Composition_For_Model.csv  # Fertilizer database
└── Filtered_Fertilizer.csv           # Crop requirements database
```

## 🎯 How It Works

1. **Data Loading**: The app loads two CSV files:
   - `Fertilizer_Composition_For_Model.csv`: Contains NPK composition of various fertilizers
   - `Filtered_Fertilizer.csv`: Contains crop-specific NPK requirements

2. **User Input**: Users select a crop and input their soil NPK values

3. **Recommendation Algorithm**: 
   - Combines crop requirements (70% weight) with user input (30% weight)
   - Uses cosine similarity to find the best matching fertilizer
   - Ranks fertilizers by similarity score

4. **Visualization**: Provides interactive charts and detailed analysis

## 📊 Data Sources

- **Fertilizer Database**: Contains 8 different fertilizers with their NPK compositions
- **Crop Database**: Contains NPK requirements for 15+ crops across different pH levels

## 🔧 Customization

### Adding New Fertilizers
Edit `Fertilizer_Composition_For_Model.csv`:
```csv
Fertilizer_Name,N (%),P (%),K (%)
New_Fertilizer,20,20,20
```

### Adding New Crops
Edit `Filtered_Fertilizer.csv`:
```csv
Crop,N,P,K,pH
New_Crop,100,50,50,6.0
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   python -m streamlit run app.py --server.port 8502
   ```

2. **Missing dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **CSV file not found**
   - Ensure CSV files are in the same directory as `app.py`
   - Check file names match exactly

### Error Messages

- **"No data available for [crop]"**: The crop doesn't exist in the database
- **"Module not found"**: Install missing dependencies with `pip install -r requirements.txt`

## 📈 Performance

- **Load Time**: ~2-3 seconds on first run (data caching)
- **Recommendation Speed**: Instant after data loading
- **Memory Usage**: ~50MB for typical usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue on GitHub

---

**Happy Farming! 🌾** 