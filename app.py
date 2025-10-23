import streamlit as st
import pickle
import pandas as pd

MODEL_FILE = "linear_regression_model.pkl"

def load_model():
    """Loads the model from the pickle file."""
    try:
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        # This error occurs if the model file is missing
        st.error(f"❌ ERROR: Model file '{MODEL_FILE}' not found. Please ensure it is uploaded.")
        return None
    except ModuleNotFoundError as e:
        # This commonly occurs if scikit-learn (or another library used to create the model) is missing
        st.error(f"❌ ERROR: Cannot load model due to missing package: {e}. ")
        st.markdown("**Please ensure `scikit-learn` is included in your `requirements.txt` file.**")
        return None
    except Exception as e:
        # Catch any other unexpected errors during loading
        st.error(f"❌ An unexpected error occurred while loading the model: {e}")
        return None

# The rest of the app logic remains the same
model = load_model()

st.title("💰 Sales Prediction App")
st.markdown("Estimate sales based on advertising budget")

if model:
    st.header("Advertising Budget (in thousands)")
    youtube = st.slider("YouTube", 0.0, 100.0, 50.0, 0.1)
    tiktok = st.slider("TikTok", 0.0, 100.0, 50.0, 0.1)
    instagram = st.slider("Instagram", 0.0, 100.0, 50.0, 0.1)
    
    if st.button("Predict Sales"):
        # Ensure the column names match the model's expected features
        input_data = pd.DataFrame({
            "youtube": [youtube],
            "tiktok": [tiktok],
            "instagram": [instagram]
        })
        # Note: Added error handling for model prediction as well, just in case
        try:
            pred = model.predict(input_data)[0]
            st.success(f"Estimated Sales: ${pred:,.2f}K")
        except Exception as e:
            st.error(f"Prediction Error: {e}")
