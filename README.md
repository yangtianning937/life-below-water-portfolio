# Life Below Water - Marine Environment Data Platform

This project is a marine environment education and data display platform focused on **Port Phillip Bay** in Melbourne, Australia. It was built as a team project for a Monash University course and is now organized as a portfolio project.

The website combines ocean protection education, water quality information, nearby beach recommendations, volunteer activities, quizzes, and a fish identity feature. The goal is to help users understand marine environmental issues in a clearer and more interactive way.

## Live Demo

[https://yangtianning937.github.io/life-below-water-portfolio/](https://yangtianning937.github.io/life-below-water-portfolio/)

Demo password:

```text
TA26
```

Note: the GitHub Pages demo deploys the frontend as a static website. Features that depend on backend APIs may require the FastAPI backend to run separately.

## Project Highlights

- Built a multi-page Vue application around the theme of **Life Below Water**
- Designed learning pages for marine ecosystems, Port Phillip Bay beaches, and ocean protection
- Integrated water quality data display and Tableau visualization
- Added nearby beach search and recommendation features based on location data
- Created a volunteer activity module with activity listing and registration flow
- Developed a Marine Quiz with multiple question types and score feedback
- Added a Fish Buddy feature that generates a personalized fish identity and avatar-style result
- Deployed the frontend to GitHub Pages for online portfolio display

## Main Features

### 1. Home Page

The home page introduces the Port Phillip Protectors theme and guides users to different parts of the platform. It includes marine facts, activity cards, and basic explanations of water quality indicators such as dissolved oxygen, salinity, nitrogen, phosphorus, and suspended solids.

### 2. Learning Module

The learning module is designed for simple and guided ocean education. It includes:

- Introduction to marine ecosystems
- Beaches near Port Phillip Bay
- Ways to protect the bay
- A learning quiz section

The module uses tabs, progress indicators, images, and quiz components to make the content easier to follow.

### 3. Water Quality Page

The project includes a water quality page with an embedded Tableau dashboard. This page helps users explore environmental data in a visual way instead of reading raw data tables.

### 4. Nearby Beach Finder

The nearby beach feature allows users to search for a place or use their current location. It connects with location-related APIs and displays:

- Nearest beach information
- Beach images
- Recommended activities
- Nearby attractions
- Nearby restaurants

### 5. Volunteer Activity Module

The activity module shows environmental activities such as clean-ups and learning events. Users can browse activity details and complete a registration form.

### 6. Marine Quiz

The Marine Quiz includes several question types:

- Multiple choice
- True or false
- Matching
- Picture identification

It gives immediate answer feedback, tracks progress, and shows a final score after submission.

### 7. Fish Buddy

The Fish Buddy feature asks the user for basic input such as name, energy level, and personality traits. It then creates a personalized fish identity result and displays a real fish image together with a cartoon-style avatar area.

## Tech Stack

### Frontend

- Vue 3
- Vite
- Vue Router
- JavaScript / TypeScript
- Tailwind CSS
- Chart.js
- Leaflet
- Axios

### Backend

- FastAPI
- Python
- SQLAlchemy
- Pydantic
- Uvicorn
- CSV data processing
- Google Places / geocoding related services
- PyTorch model files for recommendation and fish-related features

### Data and Visualization

- Tableau public dashboard
- CSV files for activity, site, fish, and water quality data
- Static image assets for learning modules and quiz pages

## Project Structure

```text
Life-Below-Water/
├── Frontend/                 # Vue 3 frontend application
│   ├── src/
│   │   ├── pages/            # Main pages such as Home, Quiz, Nearby Beach
│   │   ├── components/       # Reusable UI and learning components
│   │   ├── assets/           # Images, styles, API utilities, auth logic
│   │   ├── data/             # Quiz data and frontend CSV data
│   │   ├── router/           # Vue Router configuration
│   │   └── main.js           # Frontend entry file
│   ├── public/               # Static images for learning and quiz pages
│   ├── package.json
│   └── vite.config.js
│
├── Backend/                  # FastAPI backend application
│   ├── main.py               # API entry point
│   ├── request_model.py      # Pydantic request models
│   ├── db/                   # Database connection and models
│   ├── data/                 # CSV data files
│   ├── fish/                 # Fish identity and avatar logic
│   ├── geocode/              # Location and place search services
│   ├── recommend/            # Beach recommendation logic
│   └── requirements.txt
│
└── AI/                       # Data processing and model notebooks
```

## How to Run Locally

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:8080
```

### Backend

```bash
cd Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

The backend API will run at:

```text
http://localhost:8000/api
```

## Build for Production

```bash
cd Frontend
npm run build
```

The production files will be generated in:

```text
Frontend/dist
```

## Deployment

The portfolio version is deployed with GitHub Pages. The frontend build output is published from the `gh-pages` branch.

Main website:

[https://yangtianning937.github.io/life-below-water-portfolio/](https://yangtianning937.github.io/life-below-water-portfolio/)

## My Contributions

My work mainly focused on frontend development, page implementation, route configuration, UI adjustment, API integration, and portfolio deployment. I worked with Vue pages and components, connected frontend views with backend data interfaces, improved the display of learning and quiz modules, and deployed the project as an online portfolio using GitHub Pages.

## Team Project Context

This was originally a team project. The repository has been reorganized and deployed as a personal portfolio version to show the project outcome, technical structure, and my development experience.
