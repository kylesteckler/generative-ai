#### Example API for serving predictions with Gemini Pro asyncronously using aiohttp and FastAPI. 

Build and push to Google Artifact registry: 
- `docker build -t ARTIFACT_REGISTRY_IMAGE_URI .`
- `docker push ARTIFACT_REGISTRY_IMAGE_URI`

Deploy to Cloud Run 
- `gcloud run deploy SERVICE_NAME --image=ARTIFACT_REGISTRY_IMAGE_URI --region=REGION` 
