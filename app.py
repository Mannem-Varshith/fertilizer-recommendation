import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Fertilizer Recommendation System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    # Load fertilizer composition data
    fertilizer_df = pd.read_csv('Fertilizer_Composition_For_Model.csv')
    
    # Load crop requirements data
    crop_df = pd.read_csv('Filtered_Fertilizer.csv')
    crop_df = crop_df.drop('Unnamed: 0', axis=1, errors='ignore')
    
    return fertilizer_df, crop_df

def get_crop_requirements(crop_df, selected_crop):
    """Get NPK requirements for selected crop"""
    crop_data = crop_df[crop_df['Crop'] == selected_crop]
    if len(crop_data) > 0:
        # Return average values for the crop
        return {
            'N': crop_data['N'].mean(),
            'P': crop_data['P'].mean(),
            'K': crop_data['K'].mean(),
            'pH': crop_data['pH'].mean()
        }
    return None

def calculate_fertilizer_recommendation(fertilizer_df, crop_requirements, user_npk):
    """Calculate fertilizer recommendation based on crop requirements and user input"""
    
    # Combine crop requirements with user input (weighted average)
    target_n = (crop_requirements['N'] * 0.7 + user_npk['N'] * 0.3)
    target_p = (crop_requirements['P'] * 0.7 + user_npk['P'] * 0.3)
    target_k = (crop_requirements['K'] * 0.7 + user_npk['K'] * 0.3)
    
    # Create target vector
    target_vector = np.array([target_n, target_p, target_k])
    
    # Calculate similarity with each fertilizer
    similarities = []
    for _, row in fertilizer_df.iterrows():
        fertilizer_vector = np.array([row['N (%)'], row['P (%)'], row['K (%)']])
        similarity = cosine_similarity([target_vector], [fertilizer_vector])[0][0]
        similarities.append({
            'Fertilizer': row['Fertilizer_Name'],
            'N': row['N (%)'],
            'P': row['P (%)'],
            'K': row['K (%)'],
            'Similarity': similarity,
            'Target_N': target_n,
            'Target_P': target_p,
            'Target_K': target_k
        })
    
    # Sort by similarity
    similarities.sort(key=lambda x: x['Similarity'], reverse=True)
    return similarities

def create_npk_radar_chart(fertilizer_data, crop_requirements, user_npk):
    """Create radar chart comparing NPK values"""
    
    fig = go.Figure()
    
    # Add crop requirements
    fig.add_trace(go.Scatterpolar(
        r=[crop_requirements['N'], crop_requirements['P'], crop_requirements['K']],
        theta=['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
        fill='toself',
        name='Crop Requirements',
        line_color='green'
    ))
    
    # Add user input
    fig.add_trace(go.Scatterpolar(
        r=[user_npk['N'], user_npk['P'], user_npk['K']],
        theta=['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
        fill='toself',
        name='User Input',
        line_color='blue'
    ))
    
    # Add top 3 fertilizers
    colors = ['red', 'orange', 'purple']
    for i, fert in enumerate(fertilizer_data[:3]):
        fig.add_trace(go.Scatterpolar(
            r=[fert['N'], fert['P'], fert['K']],
            theta=['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
            fill='toself',
            name=f"{fert['Fertilizer']} (Score: {fert['Similarity']:.3f})",
            line_color=colors[i]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(crop_requirements['N'], crop_requirements['P'], crop_requirements['K'], 
                             user_npk['N'], user_npk['P'], user_npk['K'])]
            )),
        showlegend=True,
        title="NPK Comparison: Crop Requirements vs User Input vs Recommended Fertilizers"
    )
    
    return fig

def main():
    # Load data
    fertilizer_df, crop_df = load_data()
    
    # Header
    st.title("🌱 Fertilizer Recommendation System")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("📋 Input Parameters")
    
    # Crop selection
    available_crops = sorted(crop_df['Crop'].unique())
    selected_crop = st.sidebar.selectbox(
        "Select Crop:",
        available_crops,
        index=0
    )
    
    # User NPK input
    st.sidebar.subheader("Soil NPK Values (kg/ha)")
    user_n = st.sidebar.slider("Nitrogen (N):", 0, 200, 50)
    user_p = st.sidebar.slider("Phosphorus (P):", 0, 100, 30)
    user_k = st.sidebar.slider("Potassium (K):", 0, 150, 40)
    
    user_npk = {'N': user_n, 'P': user_p, 'K': user_k}
    
    # Get crop requirements
    crop_requirements = get_crop_requirements(crop_df, selected_crop)
    
    if crop_requirements:
        # Main content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"📊 Analysis for {selected_crop}")
            
            # Display crop requirements
            st.markdown("### Crop Requirements")
            req_col1, req_col2, req_col3, req_col4 = st.columns(4)
            with req_col1:
                st.metric("Nitrogen (N)", f"{crop_requirements['N']:.1f} kg/ha")
            with req_col2:
                st.metric("Phosphorus (P)", f"{crop_requirements['P']:.1f} kg/ha")
            with req_col3:
                st.metric("Potassium (K)", f"{crop_requirements['K']:.1f} kg/ha")
            with req_col4:
                st.metric("pH", f"{crop_requirements['pH']:.2f}")
        
        with col2:
            st.subheader("🎯 Your Input")
            st.metric("Nitrogen (N)", f"{user_npk['N']} kg/ha")
            st.metric("Phosphorus (P)", f"{user_p} kg/ha")
            st.metric("Potassium (K)", f"{user_k} kg/ha")
        
        # Calculate recommendations
        recommendations = calculate_fertilizer_recommendation(fertilizer_df, crop_requirements, user_npk)
        
        # Display recommendations
        st.markdown("### 🌿 Recommended Fertilizers")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Recommendations", "📊 Comparison Chart", "📈 Detailed Analysis"])
        
        with tab1:
            # Display top 5 recommendations
            for i, rec in enumerate(recommendations[:5]):
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.markdown(f"**{i+1}. {rec['Fertilizer']}**")
                        st.progress(rec['Similarity'])
                    with col2:
                        st.metric("N (%)", f"{rec['N']}")
                    with col3:
                        st.metric("P (%)", f"{rec['P']}")
                    with col4:
                        st.metric("K (%)", f"{rec['K']}")
                    st.markdown(f"*Similarity Score: {rec['Similarity']:.3f}*")
                    st.markdown("---")
        
        with tab2:
            # Create radar chart
            radar_fig = create_npk_radar_chart(recommendations, crop_requirements, user_npk)
            st.plotly_chart(radar_fig, use_container_width=True)
        
        with tab3:
            # Detailed analysis
            st.subheader("📈 Detailed Analysis")
            
            # Create comparison table
            comparison_data = []
            for rec in recommendations[:5]:
                comparison_data.append({
                    'Fertilizer': rec['Fertilizer'],
                    'N (%)': rec['N'],
                    'P (%)': rec['P'],
                    'K (%)': rec['K'],
                    'Similarity Score': f"{rec['Similarity']:.3f}",
                    'N Gap': rec['Target_N'] - rec['N'],
                    'P Gap': rec['Target_P'] - rec['P'],
                    'K Gap': rec['Target_K'] - rec['K']
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
            
            # Gap analysis
            st.subheader("🎯 Gap Analysis")
            best_match = recommendations[0]
            st.markdown(f"**Best Match: {best_match['Fertilizer']}**")
            
            gap_col1, gap_col2, gap_col3 = st.columns(3)
            with gap_col1:
                n_gap = best_match['Target_N'] - best_match['N']
                st.metric("Nitrogen Gap", f"{n_gap:.1f}", delta="kg/ha")
            with gap_col2:
                p_gap = best_match['Target_P'] - best_match['P']
                st.metric("Phosphorus Gap", f"{p_gap:.1f}", delta="kg/ha")
            with gap_col3:
                k_gap = best_match['Target_K'] - best_match['K']
                st.metric("Potassium Gap", f"{k_gap:.1f}", delta="kg/ha")
        
        # Additional information
        st.markdown("---")
        st.markdown("### ℹ️ Additional Information")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.markdown("**💡 How it works:**")
            st.markdown("""
            - The system compares your soil NPK values with crop requirements
            - It finds the best matching fertilizer from our database
            - Recommendations are based on similarity scores
            - Higher scores indicate better matches
            """)
        
        with info_col2:
            st.markdown("**📋 Available Fertilizers:**")
            st.markdown("""
            - Urea (46-0-0)
            - DAP (18-46-0)
            - MOP (0-0-60)
            - Various NPK formulations
            """)
    
    else:
        st.error(f"No data available for {selected_crop}")

if __name__ == "__main__":
    main() 