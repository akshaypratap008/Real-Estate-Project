import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title='Recommend Similar Societies')

# load files
data = pickle.load(open(r'C:\Users\apaks\Desktop\Real Estate Project\artifacts\location_df.pkl', 'rb'))
cos_sim1 = pickle.load(open(r'C:\Users\apaks\Desktop\Real Estate Project\artifacts\cos_sim1.pkl', 'rb'))
cos_sim2 = pickle.load(open(r'C:\Users\apaks\Desktop\Real Estate Project\artifacts\cos_sim2.pkl', 'rb'))
cos_sim3 = pickle.load(open(r'C:\Users\apaks\Desktop\Real Estate Project\artifacts\cos_sim3.pkl', 'rb'))

def recomend_properties(property_name, top_n = 5):
    cosine_matrix = 0.2*cos_sim1 + 0.8*cos_sim2 + 0.1*cos_sim3

    # get the similarity scores from the cosine_matrix using the property name as index
    sim_scores = list(enumerate(cosine_matrix[data.index.get_loc(property_name)]))

    # sort properties based on similarity score
    sorted_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)

    # get the indicies and scores
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    #retrieve names of top properties using indices
    top_properties = data.index[top_indices].tolist()

    # dataframe to show results
    recommendation_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendation_df

st.markdown('## Location and Radius')
st.markdown('Select a landmark and radius to find societies with in the radius')

col1, col2, col3 = st.columns(3, vertical_alignment="bottom")

landmark = col1.selectbox(label = 'Select a Landmark', options = sorted(data.columns))

distance = col2.number_input('Enter radius in KMs', min_value = 1, max_value=60, value= 1, step = 1)

if "search_triggered" not in st.session_state:
    st.session_state.search_triggered = False

if col3.button('Search', icon=":material/search:"):
    st.session_state.search_triggered = True

# --- Now use the persistent state ---
if st.session_state.search_triggered:

    col1, col2 = st.columns(2)

    with col1:
        st.divider()
        nearby_properties_dict = (
            data[data[landmark].values < (distance * 1000)][landmark].sort_values().to_dict()
        )

        if len(nearby_properties_dict) == 0:
            st.warning('No available socities. Try increasing the radius')

        else:
            st.markdown('### Nearby Societies')

            options = [
                f'{key} -- {round(value * 0.001, 1)} Kms'
                for key, value in nearby_properties_dict.items()
            ]

            selected_society = st.radio(
                label='Select a society for recommendations',
                options=options,
                index=None,
                key="society_radio"
            )

            # --- ACTION when a society is selected ---
            with col2:
                st.divider()
                if selected_society:
                    society_name = selected_society.split(" -- ")[0]
                    st.success(f"Recommended properties for {society_name}")

                    recomendation_df = recomend_properties(society_name)
                    st.dataframe(recomendation_df)



