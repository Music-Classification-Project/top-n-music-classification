# Music Model API Contract (v1)

This document describes the current REST API the frontend should use. It matches the live OpenAPI served by the Flask app.

## Base URL

- `http://127.0.0.1:5000`

## How To Run (dev)

- PowerShell (Windows):
  - `$env:FLASK_APP = "model_interface.flask_app"`
  - `$env:FLASK_ENV = "development"`
  - `$env:USE_DUMMY_SERVICE = "true"`  # enables demo GET responses and uses Dummy class
  - `flask run`

## Docs & Contract

- Swagger UI: `GET /docs`
- OpenAPI (JSON): `GET /openapi.json`

You can also pin the contract for FE/CI by exporting a static spec:

- `curl http://127.0.0.1:5000/openapi.json -o docs/openapi.v1.json`

## Endpoints

- `GET /v1/status`
  - Purpose: service metadata and readiness.
  - Response (subset):
    ```json
    {
      "status": "ok",
      "loaded": true,
      "version": "dummy-1.0",
      "genres": ["rock", "pop", "jazz", ...],
      "model_name": "dummy-music-model",
      "dummy_mode": true,
      "class_count": 10,
      "sample_rate": 22050,
      "input_duration_sec": 10,
      "channels": 1,
      "feature_types": ["mel_spec", "mfcc"],
      "n_mels": 128,
      "n_mfcc": 13,
      "n_fft": 2048,
      "hop_length": 512,
      "max_file_mb": 32,
      "max_top_k": 10
    }
    ```

- `GET /v1/genres`
  - Purpose: minimal metadata for UI.
  - Response:
    ```json
    { "data": { "genres": ["rock", "pop", ...], "model_version": "dummy-1.0" } }
    ```

- `POST /v1/genres/music`
  - Purpose: predict top genres for uploaded audio.
  - Request: multipart/form-data
    - `file`: binary (required)
    - `top_k`: integer (optional; default `5`)
  - Response:
    ```json
    { "predictions": [ { "genre": "rock", "confidence": 0.85 } ], "top_k": 5 }
    ```

- `POST /v1/genres/recommendations`
  - Purpose: similar-song recommendations for uploaded audio.
  - Request: multipart/form-data
    - `file`: binary (required)
    - `limit`: integer (optional; default `5`)
  - Response:
    ```json
    {
      "recommendations": [
        { "title": "Black Hole Sun", "artist": "Soundgarden", "genre": "rock", "similarity_score": 0.95 }
      ],
      "limit": 5
    }
    ```

### Demo GETs (only when `USE_DUMMY_SERVICE=true`)

- `GET /v1/genres/music?top_k=5` → `{ predictions, top_k, demo: true }`
- `GET /v1/genres/recommendations?limit=5` → `{ recommendations, limit, demo: true }`

## CORS

- Dev-friendly CORS headers are enabled; FE can call from localhost without extra setup.

## Frontend Usage Examples

Predict (POST):

```ts
const form = new FormData();
form.append("file", file);
form.append("top_k", "5");
const res = await fetch("http://127.0.0.1:5000/v1/genres/music", { method: "POST", body: form });
const json = await res.json(); // { predictions, top_k }
```

Recommendations (POST):

```ts
const form = new FormData();
form.append("file", file);
form.append("limit", "5");
const res = await fetch("http://127.0.0.1:5000/v1/genres/recommendations", { method: "POST", body: form });
const json = await res.json(); // { recommendations, limit }
```

Curl examples:

```bash
curl -F "file=@path/to/clip.wav" -F "top_k=5" http://127.0.0.1:5000/v1/genres/music
curl -F "file=@path/to/clip.wav" -F "limit=5" http://127.0.0.1:5000/v1/genres/recommendations
```

## Field Names

- Predictions: `prediction.genre` (not `label`)
- Minimal metadata: `data.genres`, `data.model_version`
- Status metadata: `genres` under `/v1/status`

## Stability Notes

- Response shapes are stable and JSON-safe.
- When the real model replaces the dummy service, these shapes will remain unchanged.

