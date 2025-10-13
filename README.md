# Life Below Water – Port Phillip Bay Education Website

## Project Overview
This project was developed as part of **FIT5120 (Final Project)**.  
Our goal was to design and build an interactive and educational website for children aged **10–12 years old**, focusing on **Port Phillip Bay in Melbourne, Australia**.

The website presents engaging and age-appropriate information about:
- The geography of Port Phillip Bay
- Its marine life and biodiversity
- Environmental challenges (e.g., pollution, conservation)
- Fun facts and activities designed to help children learn while exploring

By combining clear educational content with an interactive design, the project supports awareness and understanding of the importance of **sustainable ecosystems** and aligns with the UN Sustainable Development Goal: **Life Below Water**.

---

## Features
- **Kid-friendly design**: Simple language, visuals, and interactive activities for ages 10–12
- **Informative content**: Facts about Port Phillip Bay's marine life, history, and environmental concerns
- **Interactive learning modules**: Step-by-step educational content with quizzes and activities
- **Marine quiz system**: Comprehensive quiz with multiple question types (MCQ, True/False, Matching, Picture identification)
- **Water quality data visualization**: Interactive Tableau dashboards showing environmental data
- **Volunteer activity management**: Registration system for environmental activities
- **Fish identification tool**: AI-powered marine life recognition
- **Nearby beach finder**: Location-based beach recommendations with activities
- **Responsive design**: Accessible across desktop, tablet, and mobile devices

---

## Technologies Used

### Frontend
- **Vue.js 3**: Modern reactive framework with Composition API
- **Vue Router**: Client-side routing and navigation
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Chart.js**: Data visualization and charting library
- **Leaflet**: Interactive maps for location features
- **Axios**: HTTP client for API requests

### Backend
- **FastAPI**: Modern Python web framework for APIs
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Uvicorn**: ASGI server for FastAPI
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **PyTorch**: Machine learning framework for AI features
- **Pillow**: Python imaging library

### Data & Visualization
- **Tableau**: Interactive data visualization dashboards
- **CSV**: Data storage and management
- **Papa Parse**: CSV parsing in the frontend

---

## Project Structure
```
Life-Below-Water_TA26/
├── Frontend/                      # Vue.js frontend application
│   ├── src/
│   │   ├── components/            # Reusable Vue components
│   │   │   ├── epic1/            # Epic 1 specific components
│   │   │   ├── learning/         # Learning module components
│   │   │   ├── decorations/      # UI decoration components
│   │   │   ├── AppHeader.vue     # Main header component
│   │   │   ├── AppFooter.vue     # Main footer component
│   │   │   └── FullscreenMessage.vue  # Error/message modal
│   │   ├── pages/                # Page components
│   │   │   ├── HomePage.vue      # Landing page
│   │   │   ├── FishIdentity.vue  # Fish buddy generator
│   │   │   ├── BacteriaPatrol.vue # Water quality dashboard
│   │   │   ├── Epic1Page.vue     # Data visualization page
│   │   │   ├── Epic2List.vue     # Activity listing
│   │   │   ├── Epic2Register.vue # Activity registration
│   │   │   ├── LearningModule.vue # Educational modules
│   │   │   ├── MarineQuiz.vue    # Marine life quiz
│   │   │   ├── NearbyBeach.vue   # Beach finder
│   │   │   └── LockPage.vue      # Access control page
│   │   ├── router/               # Vue Router configuration
│   │   │   └── index.js          # Route definitions
│   │   ├── assets/               # Static assets and utilities
│   │   │   ├── ts/              # TypeScript utilities
│   │   │   ├── images/          # Image assets
│   │   │   ├── security/        # Security utilities
│   │   │   └── global.css       # Global styles
│   │   ├── data/                # Quiz data and CSV files
│   │   │   ├── learningQuiz.js  # Learning module quizzes
│   │   │   ├── marineQuiz.js    # Marine life quizzes
│   │   │   └── *.csv            # Water quality data
│   │   ├── utils/               # Utility functions
│   │   └── main.js              # Application entry point
│   ├── public/                  # Public static files
│   │   ├── learning/            # Learning module assets
│   │   └── quiz/                # Quiz images
│   ├── dist/                    # Production build output
│   ├── package.json             # Frontend dependencies
│   ├── vite.config.js           # Vite configuration
│   └── tailwind.config.js       # Tailwind CSS configuration
│
├── Backend/                     # FastAPI backend application
│   ├── db/                      # Database layer
│   │   ├── db.py               # Database connection
│   │   └── models.py           # SQLAlchemy models
│   ├── data/                    # CSV data files
│   │   ├── activity_data.csv   # Activity information
│   │   ├── fish_names.csv      # Fish species data
│   │   ├── site_metadata.csv   # Site information
│   │   └── water_quality_data.csv # Water quality records
│   ├── fish/                    # Fish identity system
│   │   ├── info.py             # Fish identity generation
│   │   ├── avatar.py           # Image cartoon processing
│   │   └── fne.pt              # PyTorch model weights
│   ├── recommend/               # AI recommendation system
│   │   ├── model.py            # Recommendation model
│   │   ├── process.py          # Processing pipeline
│   │   └── fav2.pt             # Model weights
│   ├── geocode/                 # Geocoding services
│   │   └── geocode.py          # Google Maps API integration
│   ├── utils/                   # Utility functions
│   │   └── csv_utils.py        # CSV processing utilities
│   ├── img/                     # Image assets
│   ├── dist/                    # Frontend production build
│   ├── main.py                  # FastAPI application entry point
│   ├── request_model.py         # Pydantic request models
│   ├── dynamic_cors_middleware.py # CORS middleware
│   ├── fish_mapping.py          # Fish data mapping
│   └── requirements.txt         # Python dependencies
│
└── AI/                          # Data processing and ML models
    ├── data_processing_code/    # Data analysis notebooks
    │   ├── e1_datap_code.ipynb # Data processing
    │   ├── site_averages_recent_year_lll.csv
    │   └── water_quality_classified_lll.csv
    ├── e3_model/                # Recommendation model
    │   ├── main.ipynb          # Model training
    │   └── model.py            # Model definition
    ├── fish.ipynb              # Fish identity experiments
    └── fne.pt                  # Fish neural network weights
```

---

## Team Members
- **Aaditya Sharma**
- **Haojun Huang**
- **Tianning**
- **Yixuan**
- **Napatcha**
- **Vida Zhang**

---

## How to Run Locally

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Git

### Frontend Setup
1. Navigate to the Frontend directory:
   ```bash
   cd Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

### Backend Setup
1. Navigate to the Backend directory:
   ```bash
   cd Backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the FastAPI server:
   ```bash
   python main.py
   ```

6. The API will be available at `http://localhost:8000`

### Production Build
To build the frontend for production:
```bash
cd Frontend
npm run build
```

The built files will be in the `dist/` directory.

---

## Key Features Documentation

### Learning Modules
- **Introduction Module**: Overview of Port Phillip Bay and marine ecosystems
- **Beaches Module**: Information about local beaches and safety guidelines
- **Protection Module**: Environmental conservation and protection strategies

### Quiz System
- Multiple question types: Multiple Choice, True/False, Matching, Picture Identification
- Age-appropriate content for 10-12 year olds
- Immediate feedback and scoring system
- Progress tracking and completion certificates

### Data Visualization
- Interactive Tableau dashboards for water quality data
- Real-time environmental monitoring information
- Historical data trends and analysis

### AI Features
- Fish identification using computer vision
- Recommendation system for activities and locations
- Image processing for marine life recognition

---

## Contributing
This is an educational project developed for FIT5120. For questions or contributions, please contact the team members.

---

## License
This project is developed for educational purposes as part of the FIT5120 Final Project.