try:
    import streamlit as st
    import json
    import os
    import pandas as pd
    import time
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
    st.markdown(f"""
        <style>
        body {{
            background-image: url("{selected_bg}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Add Sidebar Logo
    add_logo("https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg")

    # Sidebar Sections
    sections = {
        "🚀 Zero-Shot Inference": "zero_shot",
        "🛠 Fine-Tuning": "fine_tuning",
        "📊 Model Inference": "model_inference",
        "📊 Result Comparison": "result_comparison"
    }

    for label, action in sections.items():
        if st.sidebar.button(label):
            st.session_state["action"] = action

    # File Paths
    RESULTS_FILE = "zero_shot_results.json"
    FINE_TUNE_RESULTS_FILE = "fine_tuning_results.json"

    # Utility Functions
    def load_results(file_path):
        """Load JSON results from a file."""
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return None

    def format_value(value):
        """Format numeric values to 2 decimal places."""
        return f"{value:.2f}" if isinstance(value, (int, float)) else "N/A"

    def display_metrics(results):
        """Display model evaluation metrics."""
        st.metric("F1 Score (Micro)", format_value(results.get("f1_micro")))
        st.metric("Precision (Micro)", format_value(results.get("precision_micro")))
        st.metric("Recall (Micro)", format_value(results.get("recall_micro")))

    def display_confusion_matrix(results, ratio=None):
        """Display confusion matrix if available."""
        if "confusion_matrix" in results:
            title = f"🏆 Confusion Matrix for {ratio}" if ratio else "🏆 Confusion Matrix"
            st.write(f"### {title}")
            cm_df = pd.DataFrame(results["confusion_matrix"])
            st.dataframe(cm_df)

    def select_ratios(results):
        """Handle both single and multiple ratio selection for fine-tuned models."""
        available_ratios = [entry["ratio"] for entry in results]

        # Single ratio selection
        if "selected_ratio" not in st.session_state:
            st.session_state["selected_ratio"] = available_ratios[0]
        selected_ratio = st.selectbox("Select a Training Ratio:", available_ratios, 
                                      index=available_ratios.index(st.session_state["selected_ratio"]))
        st.session_state["selected_ratio"] = selected_ratio

        # Multiple ratio selection
        if "selected_ratios" not in st.session_state:
            st.session_state["selected_ratios"] = []
        selected_ratios = st.multiselect("Compare Multiple Ratios:", available_ratios, 
                                         default=st.session_state["selected_ratios"])
        st.session_state["selected_ratios"] = selected_ratios

        return selected_ratio, selected_ratios

    # Main Content
    st.markdown("# 📡 ECG Classification - AI Model Interface")
    st.markdown("---")

    if "action" not in st.session_state:
        st.info("👈 Select an option from the sidebar to proceed.")

    elif st.session_state["action"] == "zero_shot":
        st.markdown("## 🚀 Zero-Shot Inference")
        if st.button("🔄 Generate Zero-Shot Results"):
            results = load_results(RESULTS_FILE)
            if results:
                display_metrics(results)
                display_confusion_matrix(results)
            else:
                st.warning("⚠️ No Zero-Shot results found. Run the model first.")

    elif st.session_state["action"] == "model_inference":
        st.markdown("## 📊 Fine-Tuned Model Inference Results")
        # Load results
        fine_tune_results = load_results(FINE_TUNE_RESULTS_FILE)

        if fine_tune_results:
            all_ratios = [r["ratio"] for r in fine_tune_results]

            # ✅ Create a layout with two columns for selection dropdowns at the top
            col1_sel, col2_sel = st.columns([1, 1])

            # ✅ Left-most (Single Ratio Selection)
            with col1_sel:
                selected_ratio = st.selectbox("🎯 Select Single Ratio", all_ratios)

            # ✅ Right-most (Multiple Ratio Selection)
            with col2_sel:
                selected_ratios = st.multiselect("📊 Select Multiple Ratios", all_ratios, default=all_ratios)

            # ✅ Two-column layout for results
            col1, col2 = st.columns(2)

            with col1:
                # ✅ Single Ratio Results
                st.markdown(f"### 🎯 Results for {selected_ratio}")
                single_result = next((r for r in fine_tune_results if r["ratio"] == selected_ratio), None)

                if single_result:
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("📏 F1 Score (Micro)", format_value(single_result["f1_micro"]))
                    with metric_col2:
                        st.metric("🎯 Precision (Micro)", format_value(single_result["precision_micro"]))
                    with metric_col3:
                        st.metric("🔄 Recall (Micro)", format_value(single_result["recall_micro"]))

                    st.markdown("#### 🏆 Confusion Matrix")
                    display_confusion_matrix(single_result, selected_ratio)
                else:
                    st.warning(f"⚠️ No results found for ratio {selected_ratio}.")

            with col2:
                # ✅ Multi-Ratio Comparison
                if selected_ratios:
                    st.markdown("### 📊 Multi-Ratio Comparison")

                    # Prepare DataFrame
                    comparison_results = [
                        {
                            "Ratio": r["ratio"],
                            "F1 Score": format_value(r["f1_micro"]),
                            "Precision": format_value(r["precision_micro"]),
                            "Recall": format_value(r["recall_micro"])
                        }
                        for r in fine_tune_results if r["ratio"] in selected_ratios
                    ]
                    df = pd.DataFrame(comparison_results)
                    st.dataframe(df, use_container_width=True)

                    # ✅ Display Confusion Matrices for Each Selected Ratio in Expanders
                    for ratio in selected_ratios:
                        cm_result = next((r for r in fine_tune_results if r["ratio"] == ratio), None)
                        if cm_result:
                            with st.expander(f"🏆 Confusion Matrix for {ratio}"):
                                display_confusion_matrix(cm_result, ratio)
                else:
                    st.info("ℹ️ No multi-ratio results available.")


    elif st.session_state["action"] == "result_comparison":
        st.markdown("## 📊 Result Comparison")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🚀 Zero-Shot Results")
            zero_shot_results = load_results(RESULTS_FILE)
            if zero_shot_results:
                display_metrics(zero_shot_results)
                display_confusion_matrix(zero_shot_results)
            else:
                st.warning("⚠️ No Zero-Shot results found.")

        with col2:
            st.markdown("### 🛠 Fine-Tuning Results")
            fine_tune_results = load_results(FINE_TUNE_RESULTS_FILE)
            if fine_tune_results:
                # ✅ Only Show Multi-Ratio Comparison (Removed Single Ratio Selection)
                selected_ratios = st.multiselect("Compare Multiple Ratios:", 
                                                [entry["ratio"] for entry in fine_tune_results], 
                                                default=st.session_state.get("selected_ratios", []))
                st.session_state["selected_ratios"] = selected_ratios

                if selected_ratios:
                    st.markdown("---")  # Divider for clarity
                    st.markdown("## 📊 Multi-Ratio Comparison")

                    # Prepare Dataframe for Comparison
                    comparison_results = [
                        {
                            "Ratio": r["ratio"],
                            "F1 Score": format_value(r["f1_micro"]),
                            "Precision": format_value(r["precision_micro"]),
                            "Recall": format_value(r["recall_micro"])
                        }
                        for r in fine_tune_results if r["ratio"] in selected_ratios
                    ]
                    st.dataframe(pd.DataFrame(comparison_results), use_container_width=True)

                    # ✅ Display Confusion Matrices for Each Selected Ratio in Expanders
                    for ratio in selected_ratios:
                        cm_result = next((r for r in fine_tune_results if r["ratio"] == ratio), None)
                        if cm_result:
                            with st.expander(f"🏆 Confusion Matrix for {ratio}"):
                                display_confusion_matrix(cm_result, ratio)

    # Fine-Tuning Section
    elif st.session_state.get("action") == "fine_tuning":
        st.markdown("## 🛠 Fine-Tuning Model")

        model_type = st.radio("Select BackBone:", ("ViT", "ResNet"))
        pretrained_model = st.selectbox("Select Pre-trained Model:", ["resnet_tiny", "resnet_small", "resnet_large"] if model_type == "ResNet" else ["vit_tiny", "vit_small", "vit_large"])
        dataset = st.radio("Select Dataset:", ("PTB-XL", "Other"))
        
        learning_rate = st.number_input("Learning Rate:", min_value=0.00001, max_value=0.01, value=0.001, step=0.00001, format="%.5f")
        batch_size = st.number_input("Batch Size:", min_value=8, max_value=64, value=16, step=8)
        epochs = st.number_input("Epochs:", min_value=10, max_value=100, value=50, step=10)
        
        ratio_options = [25, 50, 75]
        selected_ratios = st.multiselect("Select Training Data Ratios (%):", ratio_options, default=ratio_options)

        if st.button("Start Fine-Tuning", key="start_fine_tuning"):
            st.markdown("### ⏳ Fine-Tuning in Progress...")
            progress_bar = st.progress(0)
            
            for i in range(100):
                time.sleep(0.1)  # Simulating training time
                progress_bar.progress(i + 1)
            
            st.success("✅ Fine-Tuning Completed Successfully!")

            st.json({
                "Backbone": model_type,
                "Pre-trained Model": pretrained_model,
                "Dataset": dataset,
                "Learning Rate": format_value(learning_rate),
                "Batch Size": batch_size,
                "Epochs": epochs,
                "Selected Ratios": selected_ratios
            })
except ModuleNotFoundError:
    st.error("Error: Missing required module. Install dependencies and try again.")
