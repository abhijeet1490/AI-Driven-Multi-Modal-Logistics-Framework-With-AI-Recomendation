# AI-Driven-Multi-Modal-Logistics-Framework-for-Rural-Areas

## 📋 Project Overview

This is a modular and scalable prototype for an **AI-powered logistics optimization system**. The application allows users to input shipment details (Origin, Destination, Transport Mode, Weight, Distance, Traffic Level) and receive intelligent route recommendations alongside visual interactive mapping. 

The system yields three key metrics:

- **💰 Total Cost** - Estimated freight cost in USD (dynamically scaled by Transport Mode)
- **⏱️ Time Estimate** - Approximate transit time in hours
- **🌱 CO₂ Emissions** - Carbon footprint in kilograms

The system uses a machine learning model (RandomForest) trained on synthetic logistics data to predict these metrics, with a graceful fallback to mock calculations if the model is unavailable. It features interactive map visualizations using Leaflet and Nominatim geocoding.

---

## 🏗️ Architecture & Components

The project follows a **modular 3-tier architecture**:

### 1. **AI Engine** (`ai_engine/train_model.py`)
- **Technology**: Python + Scikit-learn
- **Model**: RandomForestRegressor wrapped in MultiOutputRegressor
- **Purpose**: Generates synthetic training data and trains a multi-output regression model
- **Output**: Saves trained model as `backend/models/logistics_model.pkl`

### 2. **Backend API** (`backend/app.py`)
- **Technology**: Python + Flask
- **Structure**:
  - `routes/`: API endpoint definitions
  - `services/`: Business logic and prediction functions
  - `utils/`: Helpers like model loading
- **Features**:
  - CORS enabled for frontend communication
  - Graceful fallback to mock mode if model file is missing
  - Input validation and error handling
- **Port**: Runs on `http://127.0.0.1:5001` (configurable)

### 3. **Frontend** (`frontend/index.html`)
- **Technology**: Vanilla HTML/CSS/JavaScript
- **Styling**: Tailwind CSS (via CDN)
- **Mapping**: Leaflet JS + OpenStreetMap + Nominatim API for geocoding
- **Purpose**: Single-page web interface for user interaction
- **Features**:
  - Live Map visualization showing Origin/Destination markers
  - Route tracing between shipping endpoints
  - Transport Mode selection (Truck, Rail, Air)
  - Interactive Results Dashboard

---

## 🚀 Setup & Installation

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)

### **Step 1: Install Dependencies**

Create a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

### **Step 2: Train the Model**

Generate the machine learning model:

```bash
python ai_engine/train_model.py
```

This creates `logistics_model.pkl` in the `backend/models/` directory.

---

## ▶️ Running the Project

### **Step 1: Start the Backend Server**

Run the backend from the project root:

```bash
python backend/app.py
```

### **Step 2: Open the Frontend**

Open `frontend/index.html` in your web browser.

---

## 📁 File Structure

```
ai-logistics-india/
│
├── backend/
│   ├── app.py                      # Flask backend server entry wrapper
│   ├── routes/
│   │    └── prediction_routes.py   # API routing
│   ├── services/
│   │    └── prediction_service.py  # Prediction functions
│   ├── models/
│   │    └── logistics_model.pkl    # Trained ML model
│   └── utils/
│        └── model_loader.py        # Model loading logic
│
├── ai_engine/
│   └── train_model.py              # ML model training script
│
├── frontend/
│   └── index.html                  # Web interface
│
├── data/                           # Directory for datasets
│
├── requirements.txt                # Python dependencies
└── README.md                       # This documentation file
```

---

## 🔌 API Endpoints

### **GET /health**
Check server status and model availability.

### **POST /predict_route**
Get route predictions for a shipment.

---

**Version**: 2.0.0 (Modular Refactor)


