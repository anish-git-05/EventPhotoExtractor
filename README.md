# Event Photo Extractor

A full-stack AI web application designed to automatically curate massive folders of event photos. It uses deep learning to analyze images, group duplicates, and extract only the sharpest, highest-quality photos, delivering a single downloadable ZIP file of the perfect event album.

## Deployment Link
https://event-photo-extractor.vercel.app

## Key Features

* **AI-Powered Curation:** Uses an ONNX deep learning model to generate 1280-dimensional embeddings, combined with DBSCAN clustering (Cosine similarity) to group identical scenes.
* **Lightning Fast Uploads:** Implements Client-Side Compression (`browser-image-compression`), reducing 4K image payloads by over 95% before they ever hit the network.
* **Memory-Safe Architecture:** Designed to survive strict hardware limits (like Render's 512MB Free Tier). Features automated chunked uploads and aggressive Python garbage collection (`gc.collect()`).
* **Two-Phase Pipeline:** Decouples the upload process from the heavy AI mathematical processing to prevent server timeouts and ensure global context clustering.
* **Automated Delivery:** Server automatically packages the curated AI selections into a ready-to-download `.zip` archive.

## Tech Stack

**Frontend:**
* React.js
* Vite
* `browser-image-compression` (Frontend Optimization)

**Backend:**
* Python / Flask
* ONNX Runtime (Machine Learning Inference)
* Scikit-Learn (DBSCAN Clustering)
* OpenCV / PIL (Image Processing)
* Gunicorn (WSGI Server)

## How It Works (Under the Hood)

1.  **Ingestion:** The user selects dozens (or hundreds) of heavy event photos.
2.  **Compression & Chunking:** React shrinks the photos to 1080p and sends them to the Flask server in micro-batches (e.g., 10 photos per request) to prevent network lag and browser memory crashes.
3.  **Feature Extraction:** The Python backend runs the images through an ONNX model, converting every picture into a unique mathematical vector.
4.  **Clustering:** DBSCAN groups the vectors based on the angle between them (Cosine distance). The AI identifies the single best photo from each cluster and discards the blurry duplicates.
5.  **Delivery:** The server zips the winning photos and sends them back to the user, instantly cleaning up its internal hard drive to prepare for the next user.

## Technical Architecture & Design Decisions

This application was specifically engineered to run complex machine learning tasks on strictly limited server hardware (e.g., 512MB RAM free-tier instances). To prevent memory exhaustion and network timeouts, the pipeline is split into several highly optimized stages.

### 1. Client-Side Preprocessing & Chunking
Sending raw 4K event photos (often 15MB+ each) over HTTP causes massive network bottlenecks and immediate server memory spikes during deserialization.
* **Compression:** The React frontend utilizes `browser-image-compression` via a Web Worker to resize images to a maximum of 1080p and cap file sizes at ~500KB. This reduces network payloads by over 95% while retaining more than enough pixel density for the AI to extract accurate features.
* **Micro-Batching:** Instead of a single massive `POST` request, the frontend iterates through the dataset and uploads files in chunks (e.g., 10 photos per request). A new `FormData` object is instantiated and destroyed inside the loop to prevent browser memory leaks.

### 2. The Two-Phase Server Pipeline
To bypass standard WSGI server timeout limits (e.g., Gunicorn's 120-second guillotine), the backend decouples ingestion from processing.
* **Phase 1 (Ingestion):** The `/upload` endpoint strictly handles saving the chunked file streams to disk. It runs in milliseconds and returns `200 OK`, preventing HTTP timeouts.
* **Phase 2 (Execution):** The `/process` endpoint acts as the trigger. Because all files are fully staged on the server, the AI can load them and maintain global mathematical context across the entire dataset.

### 3. Machine Learning: Feature Extraction
The application utilizes a quantized ONNX deep learning model to "read" the photos. 
* Rather than doing basic pixel-matching (which fails if the lighting changes or a subject moves slightly), the ONNX model processes the image through its neural network and outputs a **1280-dimensional embedding**. 
* This vector mathematically represents the semantic meaning of the photo (the subjects, the background, the composition).

### 4. Machine Learning: DBSCAN Clustering
Once every photo is converted into a 1280-D vector, the system uses the Scikit-Learn `DBSCAN` algorithm to find the duplicates.
* **Distance Metric:** The model uses `cosine` similarity to measure the angle between vectors in the high-dimensional space, rather than Euclidean distance.
* **Hyperparameters:** `min_samples` is strictly set to `2` to catch pairs of duplicates. The `eps` (Epsilon) radius is carefully tuned to group photos of the same scene while splitting photos where the subject has meaningfully changed their pose.
* **Dimensionality Preservation:** PCA (Principal Component Analysis) is intentionally bypassed for large datasets to avoid compressing the vectors, allowing DBSCAN to calculate similarities using the pure, unadulterated intelligence of the 1280 dimensions.

### 5. Memory Safety & Cleanup
Processing 1280-D arrays and generating `.zip` archives creates significant memory bloat. 
* The backend forcefully invokes the Python Garbage Collector (`gc.collect()`) immediately after the AI inference step to free up RAM *before* `shutil` loads the final `.zip` file into the memory buffer for delivery.
* A `finally` block ensures that regardless of success or failure, the temporary `/uploads` and `/curated` directories are wiped clean, keeping the ephemeral server disk completely stateless for the next user.

## Local Setup

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/yourusername/EventPhotoExtractor.git
cd EventPhotoExtractor
\`\`\`

### 2. Setup the Backend (Flask)
\`\`\`bash
cd Server/Backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
\`\`\`
*The server will start on http://localhost:5000*

### 3. Setup the Frontend (React)
Go to Client/src/api.js
Comment out the deployment server and remove the comment from the localhost server.
Open a new terminal window:
\`\`\`bash
cd Frontend
npm install
npm run dev
\`\`\`
*The client will start on http://localhost:5173*

## Usage
1. Open the React frontend in your browser.
2. Click **Select Event Photos** and upload a diverse mix of event pictures (including duplicates).
3. Click **Extract Best Photos**.
4. Wait for the pipeline to finish, and your `curated_album.zip` will automatically download.
