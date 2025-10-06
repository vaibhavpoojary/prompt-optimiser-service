# import streamlit as st
# from optimizer_service import optimize_prompt
# from runner_service import run_prompt
# from evaluation_service import evaluate_outputs

# # UI Layout
# st.set_page_config(page_title="Prompt Optimizer (Bedrock Claude)", layout="wide")
# st.title("Prompt Optimizer")

# # Initialize session state variables
# if "optimized_prompt_area" not in st.session_state:
#     st.session_state.optimized_prompt_area = ""
# if "original_output" not in st.session_state:
#     st.session_state.original_output = ""
# if "optimized_output" not in st.session_state:
#     st.session_state.optimized_output = ""
# if "evaluation" not in st.session_state:
#     st.session_state.evaluation = {}

# # =========================================================================
# # 1. Model Configuration in Sidebar
# # =========================================================================
# st.sidebar.header("⚙️ Model Configuration")
# temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5, 0.01)
# top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9, 0.01)
# top_k = st.sidebar.slider("Top K", 0, 100, 50, 1)
# max_tokens = st.sidebar.number_input("Max Tokens", 1, 2048, 512, 1)
# st.sidebar.markdown("---")
# st.sidebar.caption(f"Params: T={temperature}, P={top_p}, K={top_k}, Max={max_tokens}")

# # =========================================================================
# # 2. Input Columns
# # =========================================================================
# input_col1, input_col2 = st.columns(2)

# with input_col1:
#     st.subheader("✍️ Original Prompt Input")
#     raw_prompt = st.text_area(
#         "Enter your raw prompt here:",
#         height=350,
#         placeholder="Explain the topic of Generative AI clearly and concisely...",
#         label_visibility="collapsed",
#         key="prompt_input"  # Changed key to "prompt_input"
#     )

# with input_col2:
#     st.subheader("✨ Optimized Prompt Output")
#     optimized_placeholder = st.empty()
#     optimized_placeholder.text_area(
#         "Optimized Prompt will appear here:",
#         value=st.session_state.optimized_prompt_area,
#         height=350,
#         disabled=True,
#         label_visibility="collapsed",
#         key="optimized_prompt_output"  # Key remains the same
#     )

# # =========================================================================
# # 3. Main Button Action
# # =========================================================================
# if st.button("Optimize & Evaluate Prompts", use_container_width=True):
#     if not raw_prompt.strip():
#         st.warning("Please enter a prompt first.")
#         st.stop()

#     try:
#         with st.spinner("Optimizing prompt..."):
#             optimized_prompt = optimize_prompt(
#                 raw_prompt, 
#                 temperature=temperature,
#                 top_p=top_p,
#                 top_k=top_k,
#                 max_tokens=max_tokens
#             )

#         # Update placeholder text (works with disabled text_area)
#         st.session_state.optimized_prompt_area = optimized_prompt
#         optimized_placeholder.text_area(
#             "Optimized Prompt will appear here:",
#             value=st.session_state.optimized_prompt_area,
#             height=350,
#             disabled=True,
#             label_visibility="collapsed"
#         )

#         with st.spinner("Running original prompt..."):
#             original_output = run_prompt(raw_prompt, temperature, top_p, top_k, max_tokens)

#         with st.spinner("Running optimized prompt..."):
#             optimized_output = run_prompt(optimized_prompt, temperature, top_p, top_k, max_tokens)

#         with st.spinner("Evaluating results..."):
#             evaluation = evaluate_outputs(original_output, optimized_output)

#     except Exception as e:
#         st.error(f"Error: {e}")
#         st.stop()

#     # Store outputs in session state
#     st.session_state.original_output = original_output
#     st.session_state.optimized_output = optimized_output
#     st.session_state.evaluation = evaluation
#     st.rerun()

# # =========================================================================
# # 4. Results Section
# # =========================================================================
# if "optimized_prompt_area" in st.session_state and st.session_state.optimized_prompt_area not in ["", "Press 'Optimize & Evaluate Prompts' to see the optimized prompt here."]:
#     st.markdown("---")
#     st.header("Results Comparison")

#     res_col1, res_col2, res_col3 = st.columns([1, 1, 0.7])

#     with res_col1:
#         st.subheader("🟢 Original Output")
#         st.write(st.session_state.original_output)

#     with res_col2:
#         st.subheader("🟠 Optimized Output")
#         st.write(st.session_state.optimized_output)

#     with res_col3:
#         st.subheader("📊 Evaluation")
#         evaluation = st.session_state.evaluation
#         if "error" not in evaluation:
#             st.metric("Clarity", evaluation.get("clarity", 0))
#             st.metric("Accuracy", evaluation.get("accuracy", 0))
#             st.metric("Completeness", evaluation.get("completeness", 0))
#             st.metric("Conciseness", evaluation.get("conciseness", 0))
#             st.markdown("**Verdict:**")
#             st.write(evaluation.get("verdict", ""))
#         else:
#             st.json(evaluation)




import streamlit as st
from optimizer_service import optimize_prompt
from runner_service import run_prompt
from evaluation_service import evaluate_outputs

# Helper function to safely retrieve and convert score to percentage for progress bar
def get_score_percentage(evaluation_dict, key):
    """Converts a score (assumed to be out of 10) to a 0.0 to 1.0 range for st.progress."""
    score = evaluation_dict.get(key)
    if score is None:
        return 0.0
    try:
        # Clamp value between 0 and 1
        return max(0.0, min(1.0, float(score) / 10.0))
    except (ValueError, TypeError):
        return 0.0 

# UI Layout
st.set_page_config(page_title="Prompt Optimizer (Bedrock Claude)", layout="wide")
st.title("Prompt Optimizer")

# Initialize session state variables
if "optimized_prompt_area" not in st.session_state:
    st.session_state.optimized_prompt_area = ""
if "original_output" not in st.session_state:
    st.session_state.original_output = ""
if "optimized_output" not in st.session_state:
    st.session_state.optimized_output = ""
if "evaluation" not in st.session_state:
    st.session_state.evaluation = {}

# =========================================================================
# 1. Model Configuration in Sidebar
# =========================================================================
st.sidebar.header("⚙️ Model Configuration")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5, 0.01)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9, 0.01)
top_k = st.sidebar.slider("Top K", 0, 100, 50, 1)
max_tokens = st.sidebar.number_input("Max Tokens", 1, 2048, 512, 1)
st.sidebar.markdown("---")
st.sidebar.caption(f"Params: T={temperature}, P={top_p}, K={top_k}, Max={max_tokens}")

# =========================================================================
# 2. Input Columns
# =========================================================================
input_col1, input_col2 = st.columns(2)

with input_col1:
    st.subheader("Original Prompt")
    raw_prompt = st.text_area(
        "Enter your raw prompt here:",
        height=350,
        placeholder="Explain the topic of Generative AI clearly and concisely...",
        label_visibility="collapsed",
        key="prompt_input" 
    )

with input_col2:
    st.subheader("Optimized Prompt")
    optimized_placeholder = st.empty()
    optimized_placeholder.text_area(
        "Optimized Prompt will appear here:",
        value=st.session_state.optimized_prompt_area,
        height=350,
        disabled=True,
        label_visibility="collapsed"
    )

# =========================================================================
# # 3. Main Button Action
# # =========================================================================
if st.button("Optimize & Evaluate Prompts", use_container_width=True):
    if not raw_prompt.strip():
        st.warning("Please enter a prompt first.")
        st.stop()

    try:
        with st.spinner("Optimizing prompt..."):
            optimized_prompt = optimize_prompt(
                raw_prompt, 
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                max_tokens=max_tokens
            )

        # Update placeholder text (works with disabled text_area)
        st.session_state.optimized_prompt_area = optimized_prompt
        optimized_placeholder.text_area(
            "Optimized Prompt will appear here:",
            value=st.session_state.optimized_prompt_area,
            height=350,
            disabled=True,
            label_visibility="collapsed"
        )

        with st.spinner("Running original prompt..."):
            original_output = run_prompt(raw_prompt, temperature, top_p, top_k, max_tokens)

        with st.spinner("Running optimized prompt..."):
            optimized_output = run_prompt(optimized_prompt, temperature, top_p, top_k, max_tokens)

        with st.spinner("Evaluating results..."):
            evaluation = evaluate_outputs(original_output, optimized_output)

    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

    # Store outputs in session state
    st.session_state.original_output = original_output
    st.session_state.optimized_output = optimized_output
    st.session_state.evaluation = evaluation
    st.rerun()

# =========================================================================
# 4. Results Section (ENHANCED UI)
# =========================================================================
if "optimized_prompt_area" in st.session_state and st.session_state.optimized_prompt_area not in ["", "Press 'Optimize & Evaluate Prompts' to see the optimized prompt here."]:
    st.markdown("---")
    st.header("Results Comparison")

    res_col1, res_col2, res_col3 = st.columns([1, 1, 0.7])

    # --- Original Output (using st.text_area for scrollability) ---
    with res_col1:
        st.subheader("Original Output")
        st.text_area(
            "Original Output:",
            value=st.session_state.original_output,
            height=300, 
            disabled=True,
            label_visibility="collapsed"
        )

    # --- Optimized Output (using st.text_area for scrollability) ---
    with res_col2:
        st.subheader("Optimized Output")
        st.text_area(
            "Optimized Output:",
            value=st.session_state.optimized_output,
            height=300, 
            disabled=True,
            label_visibility="collapsed"
        )

    # --- Enhanced Evaluation UI (Progress Bars) ---
    with res_col3:
        st.subheader("Evaluation")
        evaluation = st.session_state.evaluation
        
        # Define a single function for clean score display using columns and progress bar
        def display_score(key, label):
            score_value = evaluation.get(key)
            
            # Use two local columns for score label and bar
            metric_col_a, metric_col_b = st.columns([0.5, 1])
            
            with metric_col_a:
                st.markdown(f"**{label}**")
            with metric_col_b:
                progress = get_score_percentage(evaluation, key)
                score_text = "N/A"
                if score_value is not None:
                     try:
                        score_text = f"{float(score_value):.1f}"
                     except (ValueError, TypeError):
                        pass
                    
                st.progress(progress, text=score_text)
        
        if "error" not in evaluation:
            st.markdown("##### Score Breakdown (Out of 10)")
            
            display_score("clarity", "Clarity")
            display_score("accuracy", "Accuracy")
            display_score("completeness", "Completeness")
            display_score("conciseness", "Conciseness")
            
            st.markdown("---")
            
            st.markdown("##### Key Verdict")
            st.info(evaluation.get("verdict", "No detailed verdict available."), icon="💡")
            
        else:
            st.error("Evaluation Error")
            st.json(evaluation)

