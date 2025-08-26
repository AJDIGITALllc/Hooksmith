🎵 Hooksmith

Forge lyrics. Shape songs. Train creativity with AI.
Proprietary — All Rights Reserved (AJ DIGITAL LLC)

Overview

Hooksmith is a proprietary songwriting AI toolkit that ingests lyric URLs, structures them into datasets, builds artist style profiles (constraints + formulas), and generates Suno MetaTag prompts. It integrates Perplexity (web + analysis), Claude (JSON validation), Gemini (normalization/summarization), OpenAI (generation/embeddings), and Ideogram (artist profile images). Firebase powers the web UI: Hosting, Firestore, Storage, Auth.

Core outcomes

Ingest lyric URLs → structured sections (verse/chorus/bridge)

Extract themes, mood, rhyme schemes, hook types, formulas

Build per-artist style profiles in /catalog

Export to Suno MetaTag prompt blocks

Optional: generate artist profile images with Ideogram

Features

Artist Catalog – JSON profiles (BPM hints, hook bias, devices, dataset counts)

Lyric Analyzer – Perplexity → Claude → Gemini pipeline for clean JSON

Dataset Builder – CSV/JSON aligned with Hooksmith schema

Prompt Composer – Auto-assemble prompts from intake questionnaire

Suno Exporter – Output [genre: …] [bpm: …] [mood: …] prompt blocks

Ideogram Support – Generate artist profile images

Firebase UI – Host a private dashboard; persist data in Firestore; store assets in Storage

Tech Stack

Python: pipeline (ingest, validate, normalize, export)

APIs: Perplexity, Claude, Gemini, OpenAI, Ideogram

Firebase: Hosting, Firestore, Storage, Auth

(Optional) Frontend: Vite/React or any SPA

Installation (Backend / Pipeline)
git clone git@github.com:AJDIGITALllc/Hooksmith.git
cd Hooksmith


Create .env (use .env.example as reference):

OPENAI_API_KEY=your-key
PERPLEXITY_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
GEMINI_API_KEY=your-key
IDEOGRAM_API_KEY=your-key


Install Python deps:

pip install -r requirements.txt


Repo structure

Hooksmith/
│── src/
│   ├── clients/           # OpenAI, Perplexity, Claude, Gemini, Ideogram
│   ├── pipeline/          # ingest_artist() → dataset rows + artist profile
│   ├── exporter/          # Suno MetaTag formatter
│   └── config/            # settings loader
│── catalog/               # artist profiles (+ optional images)
│── data/                  # datasets & templates
│── docs/                  # documentation
│── tests/                 # unit tests
│── .env.example
│── .gitignore
│── README.md
│── LICENSE

Usage (Pipeline)
1) Ingest lyrics for an artist
from src.pipeline.ingest import ingest_artist

ingest_artist(
  artist="Bryson Tiller",
  urls=[
    "https://genius.com/Bryson-tiller-exchange-lyrics",
    "https://genius.com/Bryson-tiller-dont-lyrics"
  ],
  out_csv="data/trapsoul_dataset.csv"
)


Pipeline: Perplexity → Claude → Gemini → writes rows to CSV and updates /catalog/bryson_tiller.json.

2) Export Suno MetaTags
from src.exporter.suno_formatter import to_suno_metatags
import pandas as pd

df = pd.read_csv("data/trapsoul_dataset.csv")
print(to_suno_metatags(df.iloc[0].to_dict()))

3) Generate artist profile image (optional)
from src.clients.ideogram_client import generate_artist_image
generate_artist_image(
  artist="Bryson Tiller (Trap-Soul profile)",
  style_tags=["cinematic","album cover","moody"],
  out_path="catalog/bryson_tiller.png"
)

Firebase Setup (Frontend + Data)

If content is king, context is god. Keep config in envs and lock data with Rules.

1) Install & login
npm install -g firebase-tools
firebase login

2) Initialize
firebase init


Select:

Hosting (SPA)

Firestore

Storage

(Auth works from the client SDK; no init step here)

Recommended answers:

Public dir: dist (or build for CRA)

Configure as SPA: Yes

GitHub deploys: optional

This creates firebase.json and .firebaserc.

3) Client SDK bootstrap

Create src/firebase.js in your web app (Vite/React recommended):

import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,    // use env, not hard-coded
  authDomain: "gen-lang-client-0960626274.firebaseapp.com",
  projectId: "gen-lang-client-0960626274",
  storageBucket: "gen-lang-client-0960626274.appspot.com",
  messagingSenderId: "650997065313",
  appId: "1:650997065313:web:7ddc4b42230830aee6ec20",
  measurementId: "G-P342F03E4T"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const storage = getStorage(app);
export const auth = getAuth(app);


Vite env: create .env.local (not committed)

VITE_FIREBASE_API_KEY=your-public-web-api-key

4) Minimal Security Rules (start here, tighten later)

Firestore Rules (lock by auth; adjust as needed):

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function isSignedIn() { return request.auth != null; }

    match /artists/{doc} {
      allow read: if true;              // public read of artist catalog (optional)
      allow write: if isSignedIn();     // only signed-in users write
    }
    match /datasets/{doc} {
      allow read: if isSignedIn();
      allow write: if isSignedIn();
    }
  }
}


Storage Rules (images & exports):

rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    function isSignedIn() { return request.auth != null; }
    match /catalog/{allPaths=**} {
      allow read: if true;              // public images (optional)
      allow write: if isSignedIn();
    }
    match /exports/{allPaths=**} {
      allow read, write: if isSignedIn();
    }
  }
}


Fine-tune later: per-user docs, roles/claims, rate-limited Cloud Functions, etc.

5) Build & Deploy (SPA)
npm run build
firebase deploy


Hosting URLs will be shown (e.g. *.web.app and *.firebaseapp.com).

Suggested Firestore Collections (Frontend)

artists/{style_id}: { name, bpm_range, hook_bias, devices_bias, profile_image, dataset_count, updated_at }

requests/{request_id}: user generation requests (genre, themes, structure, artist_ref, status)

outputs/{output_id}: generated lyrics + Suno MetaTags + timestamps

Security & Key Management

Never commit .env, secrets, or private keys.

Client Firebase API key is public by design, but Rules must enforce access.

Rotate external API keys if exposed; use server-side proxies for sensitive operations.

Roadmap

UI: Intake questionnaire → prompt composer → Suno exporter

JSONL exporter for model fine-tuning

BPM/key detection & auto-calibration

Role-based access control (creators vs. admins)

Cloud Functions for server-side API calls (optional hardening)

Contributing

Closed-source/private; collaborators by invitation.

License

Proprietary License — All Rights Reserved
Copyright © 2025 AJ DIGITAL LLC.

No copying, publishing, distributing, sublicensing, or selling without written permission.