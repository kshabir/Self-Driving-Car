try:
    import streamlit as st
    import json
    import time
    import os
    import pandas as pd
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
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    # Add Sidebar Logo
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
    
    # Path to results files
    RESULTS_FILE = "zero_shot_results.json"
    FINE_TUNE_RESULTS_FILE = "fine_tuning_results.json"
    
    # Action Handling
    if "action" not in st.session_state:
        st.info("👈 Select an option from the sidebar to proceed.")
    
    elif st.session_state["action"] == "zero_shot":
        st.markdown("## 🚀 Zero-Shot Inference")
        if st.button("🔄 Generate Zero-Shot Results", key="zero_shot_generate"):
            if os.path.exists(RESULTS_FILE):
                with open(RESULTS_FILE, "r") as f:
                    results = json.load(f)
                
                st.write("### 🔍 Key Performance Metrics")
                st.metric("F1 Score (Micro)", results.get("f1_micro", "N/A"))
                st.metric("Precision (Micro)", results.get("precision_micro", "N/A"))
                st.metric("Recall (Micro)", results.get("recall_micro", "N/A"))
                
                if "confusion_matrix" in results:
                    st.write("### 🏆 Confusion Matrix")
                    cm_df = pd.DataFrame(results["confusion_matrix"])
                    st.dataframe(cm_df)
            else:
                st.warning("⚠️ No Zero-Shot results found. Run the model first.")
    
    elif st.session_state["action"] == "model_inference":
        st.markdown("## 📊 Fine-Tuned Model Inference Results")
        
        if os.path.exists(FINE_TUNE_RESULTS_FILE):
            with open(FINE_TUNE_RESULTS_FILE, "r") as f:
                fine_tune_results = json.load(f)
            
            available_ratios = [entry["ratio"] for entry in fine_tune_results]
            
            # Store selected ratios to prevent reset
            if "selected_ratio" not in st.session_state:
                st.session_state["selected_ratio"] = available_ratios[0] if available_ratios else None
            if "selected_ratios" not in st.session_state:
                st.session_state["selected_ratios"] = []
            
            # Single ratio selection
            selected_ratio = st.selectbox("Select a Training Ratio:", available_ratios, index=available_ratios.index(st.session_state["selected_ratio"]) if st.session_state["selected_ratio"] in available_ratios else 0)
            st.session_state["selected_ratio"] = selected_ratio
            
            single_result = next((r for r in fine_tune_results if r["ratio"] == selected_ratio), None)
            if single_result:
                st.metric("F1 Score (Micro)", single_result["f1_micro"])
                st.metric("Precision (Micro)", single_result["precision_micro"])
                st.metric("Recall (Micro)", single_result["recall_micro"])
                if "confusion_matrix" in single_result:
                    st.write(f"### 🏆 Confusion Matrix for {selected_ratio}")
                    cm_df = pd.DataFrame(single_result["confusion_matrix"])
                    st.dataframe(cm_df)
            
            # Multi-ratio selection for comparison
            selected_ratios = st.multiselect("Compare Multiple Ratios:", available_ratios, default=st.session_state["selected_ratios"])
            st.session_state["selected_ratios"] = selected_ratios
            
            if selected_ratios:
                comparison_results = [r for r in fine_tune_results if r["ratio"] in selected_ratios]
                comparison_df = pd.DataFrame(comparison_results)
                st.write("### 📊 Fine-Tuned Model Comparison")
                st.dataframe(comparison_df)
                
                # Display confusion matrices for each selected ratio
                for ratio in selected_ratios:
                    cm_result = next((r for r in fine_tune_results if r["ratio"] == ratio), None)
                    if cm_result and "confusion_matrix" in cm_result:
                        st.write(f"### 🏆 Confusion Matrix for {ratio}")
                        cm_df = pd.DataFrame(cm_result["confusion_matrix"])
                        st.dataframe(cm_df)
        else:
            st.warning("⚠️ No fine-tuned model inference results found. Run the model first.")
    
    elif st.session_state["action"] == "result_comparison":
        st.markdown("## 📊 Result Comparison")
        st.write("Compare and analyze results from different inference approaches.")

    # Fine-Tuning Section
    if "action" in st.session_state and st.session_state["action"] == "fine_tuning":
        st.markdown("## 🛠 Fine-Tuning Model")
        
        # Model Selection
        model_type = st.radio("Select BackBone:", ("ViT", "ResNet"))
        
        # Pretrained Model Selection Based on Model Type
        if model_type == "ViT":
            pretrained_model = st.selectbox("Select Pre-trained Model:", ["resnet_tiny", "resnet_small", "resnet_large"])
        else:
            pretrained_model = st.selectbox("Select Pre-trained Model:", ["vit_tiny", "vit_small", "vit_large"])
        
        # Fixed dataset
        dataset = st.radio("Select Dataset:", ("PTB-XL", "Other"))
        
        # Hyperparameter Inputs
        learning_rate = st.number_input("Learning Rate:", min_value=0.00001, max_value=0.01, value=0.001, step=0.00001, format="%f")
        batch_size = st.number_input("Batch Size:", min_value=8, max_value=64, value=16, step=8)
        epochs = st.number_input("Epochs:", min_value=10, max_value=100, value=50, step=10)
        
        # Ratio Selection (Multiple Options)
        ratio_options = [25, 50, 75]
        selected_ratios = st.multiselect("Select Training Data Ratios (%):", ratio_options, default=ratio_options)
        
        if st.button("Start Fine-Tuning", key="start_fine_tuning"):
            st.markdown("### ⏳ Fine-Tuning in Progress...")
            
            progress_bar = st.progress(0)
            
            for i in range(100):
                time.sleep(3)  # Simulating training time (~5 minutes total)
                progress_bar.progress(i + 1)
            
            # Simulated Fine-Tuning Completion Message
            st.success("✅ Fine-Tuning Completed Successfully!")
            
            # Display Selected Configurations
            st.markdown("### 📌 Fine-Tuning Configuration")
            config_data = {
                "Backbone": model_type,
                "Pre-trained Model": pretrained_model,
                "Dataset": dataset,
                "Learning Rate": learning_rate,
                "Batch Size": batch_size,
                "Epochs": epochs,
                "Selected Ratios": selected_ratios
            }
            st.json(config_data)


except ModuleNotFoundError as e:
    st.error("Error: The 'streamlit' module is not installed. Please install it using 'pip install streamlit' and try again.")
