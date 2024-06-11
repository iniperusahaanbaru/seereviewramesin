import streamlit as st
from google.cloud import firestore
import os
import json
from google.oauth2 import service_account



# This needs to be the first Streamlit command used in your script.
st.set_page_config(page_title='Review Book Ramesindong', layout='wide')



# Google Cloud configuration
BUCKET_NAME = "fotorestoran"
FIRESTORE_COLLECTION = "reviews"

# Initialize Google Cloud clients using environment variables
credentials_dict = {
    'type': st.secrets['GOOGLE_CREDENTIALS_JSON']['type'],
    'project_id': st.secrets['GOOGLE_CREDENTIALS_JSON']['project_id'],
    'private_key_id': st.secrets['GOOGLE_CREDENTIALS_JSON']['private_key_id'],
    # Ensure the private_key's newline characters are handled correctly
    'private_key': st.secrets['GOOGLE_CREDENTIALS_JSON']['private_key'].replace('\\n', '\n'),
    'client_email': st.secrets['GOOGLE_CREDENTIALS_JSON']['client_email'],
    'client_id': st.secrets['GOOGLE_CREDENTIALS_JSON']['client_id'],
    'auth_uri': st.secrets['GOOGLE_CREDENTIALS_JSON']['auth_uri'],
    'token_uri': st.secrets['GOOGLE_CREDENTIALS_JSON']['token_uri'],
    'auth_provider_x509_cert_url': st.secrets['GOOGLE_CREDENTIALS_JSON']['auth_provider_x509_cert_url'],
    'client_x509_cert_url': st.secrets['GOOGLE_CREDENTIALS_JSON']['client_x509_cert_url'],
}

# Create a credentials object from the service account info
credentials = service_account.Credentials.from_service_account_info(credentials_dict)

# Initialize Google Cloud clients with the credentials

firestore_db = firestore.Client(project=credentials_dict['project_id'], credentials=credentials)


def fetch_reviews(limit=100):  # Example limit added
    reviews_query = firestore_db.collection(FIRESTORE_COLLECTION) \
        .where("restoran_name", "==", "Restoran Tes12") \
        .order_by("timestamp", direction=firestore.Query.DESCENDING) \
        .limit(limit)  # Limit the results
        
    docs = reviews_query.stream()
    reviews = [doc.to_dict() for doc in docs]
    return reviews

def display_review(review):
    st.image(review['image_url'], use_column_width=True)
    with st.expander("See Review"):
        st.write(review['review_text'])
        st.write(f"Reviewer: {review['reviewer_name']}")
        st.write(f"Rating: {review['rating']}")
        st.write(f"Date: {review['timestamp'].strftime('%Y-%m-%d')}")

def main():
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.title('Review Book Tes123')
    # Fetch and cache reviews
    reviews = fetch_reviews()

    if not reviews:
        st.warning("No reviews found for Restoran 123.")
        st.image("placeholder.jpg", use_column_width=True)
    else:
        cols = st.columns(5)
        for index, review in enumerate(reviews):
            with cols[index % 5]:
                display_review(review)



if __name__ == "__main__":
    main()
