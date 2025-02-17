try:
    import streamlit as st
    from streamlit_extras.app_logo import add_logo
    
    # Streamlit UI Layout
    st.set_page_config(page_title="ECG Classification", layout="wide")
    
    # Background images based on section selection
    background_images = {
        "zero_shot": "https://source.unsplash.com/1600x900/?artificial-intelligence",
        "fine_tuning": "https://source.unsplash.com/1600x900/?machine-learning",
        "model_inference": "https://source.unsplash.com/1600x900/?data-science",
        "result_comparison": "https://source.unsplash.com/1600x900/?analytics"
    }
    
    selected_bg = background_images.get(st.session_state.get("action", "zero_shot"), background_images["zero_shot"])
    
    # Dynamic Background Styling
    page_bg_img = f'''
    <style>
    body {{
        background-image: url("{selected_bg}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .stButton > button {{
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        box-shadow: 0 9px #999;
    }}
    .stButton > button:hover {{
        background-color: #45a049;
    }}
    .stButton > button:active {{
        background-color: #3e8e41;
        box-shadow: 0 5px #666;
        transform: translateY(4px);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    try:
    import streamlit as st
    from streamlit_extras.app_logo import add_logo
    
    # Streamlit UI Layout
    st.set_page_config(page_title="ECG Classification", layout="wide")
    
    # Background images based on section selection
    background_images = {
        "zero_shot": "https://source.unsplash.com/1600x900/?artificial-intelligence",
        "fine_tuning": "https://source.unsplash.com/1600x900/?machine-learning",
        "model_inference": "https://source.unsplash.com/1600x900/?data-science",
        "result_comparison": "https://source.unsplash.com/1600x900/?analytics"
    }
    
    selected_bg = background_images.get(st.session_state.get("action", "zero_shot"), background_images["zero_shot"])
    
    # Dynamic Background Styling
    page_bg_img = f'''
    <style>
    body {{
        background-image: url("{selected_bg}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .stButton > button {{
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        box-shadow: 0 9px #999;
    }}
    .stButton > button:hover {{
        background-color: #45a049;
    }}
    .stButton > button:active {{
        background-color: #3e8e41;
        box-shadow: 0 5px #666;
        transform: translateY(4px);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    # Add a Sidebar Logo (Optional: Replace with your logo URL)
    add_logo("https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg")
    
    # Sidebar Sections with Styling
    st.sidebar.markdown("## 🔬 Zero-Shot Section")
    if st.sidebar.button("🚀 Zero-Shot Inference", key="zero_shot_btn"):
        st.session_state["action"] = "zero_shot"
    
    st.sidebar.markdown("## 🎯 Fine-Tuning Section")
    if st.sidebar.button("🛠 Fine-Tuning", key="fine_tune_btn"):
        st.session_state["action"] = "fine_tuning"
    
    st.sidebar.markdown("## 📈 Model Inference Section")
    if st.sidebar.button("📊 Model Inference", key="model_inf_btn"):
        st.session_state["action"] = "model_inference"
    
    st.sidebar.markdown("## 📊 Result Comparison Section")
    if st.sidebar.button("📊 Result Comparison", key="result_comp_btn"):
        st.session_state["action"] = "result_comparison"
    
    # Main Page Title
    st.markdown("# 📡 ECG Classification - AI Model Interface")
    st.markdown("---")
    
    # Action Handling
    if "action" not in st.session_state:
        st.info("👈 Select an option from the sidebar to proceed.")
    elif st.session_state["action"] == "zero_shot":
        st.markdown("## 🚀 Zero-Shot Inference")
        st.write("This section will handle Zero-Shot Inference based on a pre-trained model.")
        if st.button("🔄 Generate Results", key="zero_shot_results"):
            st.success("✅ Running result generation for Zero-Shot Inference...")
    elif st.session_state["action"] == "fine_tuning":
        st.markdown("## 🎯 Fine-Tuning")
        st.write("This section allows users to fine-tune the model with different data ratios.")
        selected_ratios = st.multiselect("Select Training Data Ratios for Fine-Tuning:", ["25%", "50%", "75%"], default=["25%", "50%", "75%"])
        if st.button("🔄 Start Fine-Tuning", key="fine_tune_results"):
            st.success(f"✅ Fine-tuning models with {', '.join(selected_ratios)} data ratios...")
    elif st.session_state["action"] == "model_inference":
        st.markdown("## 📊 Model Inference")
        st.write("Perform model inference using the fine-tuned model.")
        if st.button("🔄 Generate Results", key="model_inf_results"):
            st.success("✅ Running result generation for Model Inference...")
    elif st.session_state["action"] == "result_comparison":
        st.markdown("## 📊 Result Comparison")
        st.write("Compare and analyze results from different inference approaches.")
    
except ModuleNotFoundError as e:
    st.error("Error: The 'streamlit' module is not installed. Please install it using 'pip install streamlit' and try again.")

    # Add a Sidebar Logo (Optional: Replace with your logo URL)
    add_logo("https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg")
    
    # Sidebar Sections with Styling
    st.sidebar.markdown("## 🔬 Zero-Shot Section")
    if st.sidebar.button("🚀 Zero-Shot Inference", key="zero_shot_btn"):
        st.session_state["action"] = "zero_shot"
    
    st.sidebar.markdown("## 🎯 Fine-Tuning Section")
    if st.sidebar.button("🛠 Fine-Tuning", key="fine_tune_btn"):
        st.session_state["action"] = "fine_tuning"
    if st.sidebar.button("📊 Model Inference - Different Ratios", key="model_inf_btn"):
        st.session_state["action"] = "model_inference"
    
    st.sidebar.markdown("## 📈 Result Comparison Section")
    if st.sidebar.button("📊 Result Comparison", key="result_comp_btn"):
        st.session_state["action"] = "result_comparison"
    
    # Main Page Title
    st.markdown("# 📡 ECG Classification - AI Model Interface")
    st.markdown("---")
    
    # Action Handling
    if "action" not in st.session_state:
        st.info("👈 Select an option from the sidebar to proceed.")
    elif st.session_state["action"] == "zero_shot":
        st.markdown("## 🚀 Zero-Shot Inference")
        st.write("This section will handle Zero-Shot Inference based on a pre-trained model.")
        if st.button("🔄 Generate Results", key="zero_shot_results"):
            st.success("✅ Running result generation for Zero-Shot Inference...")
    elif st.session_state["action"] == "fine_tuning":
        st.markdown("## 🎯 Fine-Tuning")
        st.write("This section is for model fine-tuning with custom datasets.")
    elif st.session_state["action"] == "model_inference":
        st.markdown("## 📊 Model Inference - Different Ratios")
        st.write("Perform model inference based on varying dataset ratios.")
        if st.button("🔄 Generate Results", key="model_inf_results"):
            st.success("✅ Running result generation for Model Inference...")
    elif st.session_state["action"] == "result_comparison":
        st.markdown("## 📈 Result Comparison")
        st.write("Compare and analyze results from different inference approaches.")
    
except ModuleNotFoundError as e:
    st.error("Error: The 'streamlit' module is not installed. Please install it using 'pip install streamlit' and try again.")
