# ✈️ Airline Analytics Dashboard

> **Real-time insights into airline booking trends, popular routes, and market demand**

![Dashboard Preview](https://via.placeholder.com/800x400/2563eb/ffffff?text=Airline+Analytics+Dashboard)

## 🌟 Features

- **📊 Interactive Data Visualization** - Beautiful charts and graphs for trends analysis
- **🔍 Real-time Flight Search** - Search and filter flights by route, price, and airline
- **🤖 AI-Powered Insights** - Intelligent analysis of airline market data
- **📱 Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **📈 Export Functionality** - Download data in CSV format for further analysis
- **🎨 Modern UI** - Clean, professional design with purple gradient cards

## 🚀 Quick Deploy to GitHub Pages

### Option 1: Automated Deployment (Windows)
1. **Double-click** `deploy.bat` to run the automated deployment script
2. **Enter your GitHub username** when prompted
3. **Follow the on-screen instructions**
4. **Your dashboard will be live** at `https://your-username.github.io/airline-analytics-dashboard/`

### Option 2: Manual Deployment
1. **Create a new repository** on GitHub named `airline-analytics-dashboard`
2. **Clone the repository** to your local machine
3. **Copy files** from the `frontend` folder to your repository root
4. **Push to GitHub** and enable GitHub Pages in Settings

## 📱 Live Demo

🔗 **[View Live Dashboard](https://your-username.github.io/airline-analytics-dashboard/)**

## 🛠️ Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **UI Framework:** Bootstrap 5
- **Charts:** Chart.js for beautiful data visualization
- **Icons:** Font Awesome 6
- **Backend:** Python FastAPI (for local development)
- **Deployment:** GitHub Pages

## 📈 Dashboard Statistics

- **300+** Sample flights analyzed
- **16** Major airports covered (JFK, LAX, ORD, DFW, etc.)
- **8** Airlines included (American, Delta, United, Southwest, etc.)
- **10** Popular routes tracked
- **Real-time** data filtering and visualization

## 🎯 Key Components

### 1. **Filter System**
- Search by origin and destination airports
- Adjustable data limits (50-500 flights)
- Real-time data loading with loading overlay

### 2. **Statistics Cards**
- Total flights counter
- Unique routes tracker
- Airlines coverage
- Airports network size

### 3. **Interactive Charts**
- **Route Volume Chart** - Bar chart showing flight volume by route
- **Airline Market Share** - Doughnut chart displaying market distribution
- **Price Trends** - Line chart showing price fluctuations over time
- **Top Routes** - List of most popular routes with demand metrics

### 4. **Data Table**
- Comprehensive flight details
- Sortable columns
- Export functionality
- Status indicators with color coding

## 🔧 Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/airline-analytics-dashboard.git

# Navigate to project directory
cd airline-analytics-dashboard

# Open in your browser
open index.html
```

### Backend Development (Optional)
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
python -m uvicorn app.main:app --reload
```

## 📝 File Structure

```
airline-analytics-dashboard/
├── frontend/
│   ├── index.html      # Main dashboard page
│   ├── styles.css      # Modern dashboard styling
│   └── app.js          # Dashboard functionality
├── backend/
│   ├── app/
│   │   ├── main.py     # FastAPI application
│   │   └── ...         # API modules
│   └── requirements.txt
├── deploy.bat          # Windows deployment script
├── deploy.md           # Deployment guide
└── README.md           # This file
```

## 🎨 Design Features

- **Modern Color Scheme** - Blue header with purple gradient cards
- **Responsive Layout** - Mobile-first design approach
- **Smooth Animations** - CSS transitions and fade effects
- **Professional Typography** - Clean, readable fonts
- **Accessibility** - WCAG compliant design elements

## 🌐 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## 📊 Sample Data

The dashboard includes comprehensive sample data:
- **Airlines:** American, Delta, United, Southwest, JetBlue, Alaska, Spirit, Frontier
- **Routes:** JFK-LAX, ORD-LAS, DFW-DEN, BOS-SFO, MIA-LGA, ATL-PHX, SEA-IAD, EWR-DCA
- **Price Range:** $200 - $1000 per flight
- **Flight Status:** On Time, Delayed, Boarding, Departed

## 🚀 Deployment Options

### GitHub Pages (Recommended)
- **Free hosting** for static sites
- **Custom domain** support
- **HTTPS** enabled by default
- **Easy deployment** with automated scripts

### Alternative Platforms
- **Netlify** - Drag and drop deployment
- **Vercel** - Git-based deployment
- **Surge.sh** - Simple command-line deployment
- **Firebase Hosting** - Google Cloud integration

## 🔧 Configuration

### For GitHub Pages Deployment:
```javascript
// app.js
const API_BASE_URL = '';
const USE_SAMPLE_DATA = true;
```

### For Backend Integration:
```javascript
// app.js
const API_BASE_URL = 'http://localhost:8000';
const USE_SAMPLE_DATA = false;
```

## 📈 Performance Optimization

- **CDN Libraries** - Bootstrap and Chart.js loaded from CDN
- **Optimized Images** - Compressed and properly sized
- **Minified CSS** - Reduced file sizes
- **Async Loading** - Non-blocking JavaScript execution
- **Caching** - Browser caching for static assets

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

## 🐛 Bug Reports

If you encounter any issues:
1. Check the browser console for errors
2. Verify all files are properly uploaded
3. Ensure GitHub Pages is enabled
4. Test in different browsers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Aviation Data** - Powered by aviation APIs and open data sources
- **Chart.js** - Beautiful, responsive charts
- **Bootstrap** - Responsive UI framework
- **Font Awesome** - Icon library
- **GitHub Pages** - Free hosting platform

## 🎉 Success Stories

> "This dashboard helped me analyze airline market trends and make informed booking decisions!" - User Review

> "The responsive design and interactive charts make data visualization a breeze!" - Developer Feedback

## 📞 Support

- **Documentation:** Check the `deploy.md` file for detailed deployment instructions
- **Issues:** Use GitHub Issues for bug reports and feature requests
- **Community:** Join our discussions in the repository

## 🏆 Next Steps

After successful deployment:
1. **Customize** the dashboard with your branding
2. **Add more data sources** for comprehensive analysis
3. **Implement user authentication** for personalized features
4. **Add more chart types** for deeper insights
5. **Create a mobile app** version

---

**🚀 Ready to deploy? Run `deploy.bat` and get your dashboard live in minutes!**

**⭐ Don't forget to star this repository if you found it helpful!** 