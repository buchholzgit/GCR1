gcloud builds submit --tag gcr.io/rosenbaumnagy/webapp1 --project=rosenbaumnagy --timeout=1200

gcloud run deploy --image gcr.io/rosenbaumnagy/webapp1  --platform managed  --project=rosenbaumnagy --allow-unauthenticated