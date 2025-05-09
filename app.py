# import streamlit as st
# import torch
# from transformers import GPTNeoForCausalLM, GPT2Tokenizer
# import time
# import os

# def apply_custom_css():
#     st.markdown("""
#     <style>
#     /* Main container styling */
#     .main {
#         background-color: #f0f4f8; /* soft blue-gray */
#         padding-bottom: 80px;
#     }
    
#     /* Header styling */
#     .stTitle {
#         font-size: 26px !important;
#         margin-bottom: 20px !important;
#         color: #2e3a59 !important;
#     }
    
#     /* Chat container */
#     .chat-container {
#         display: flex;
#         flex-direction: column;
#         height: calc(100vh - 210px);
#         overflow-y: auto;
#         padding-bottom: 20px;
#     }
    
#     /* Message styling */
#     .chat-message {
#         padding: 1.5rem;
#         border-radius: 0;
#         margin-bottom: 0;
#         display: flex;
#         width: 100%;
#     }
    
#     .chat-message.user {
#         background-color: #e3f2fd; /* soft light blue */
#     }
    
#     .chat-message.bot {
#         background-color: #ffffff;
#     }
    
#     .chat-message .avatar {
#         width: 36px;
#         height: 36px;
#         border-radius: 4px;
#         margin-right: 16px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 18px;
#     }
    
#     .chat-message .user-avatar {
#         background-color: #4dabf7; /* medium soft blue */
#         color: white;
#     }
    
#     .chat-message .bot-avatar {
#         background-color: #38d9a9; /* soft teal green */
#         color: white;
#     }
    
#     .chat-message .message-content {
#         flex-grow: 1;
#         max-width: 800px;
#         margin: 0 auto;
#         font-size: 16px;
#         line-height: 1.6;
#     }
    
#     /* Footer input area */
#     .input-container {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         right: 0;
#         background-color: #f8fafc; /* off white */
#         padding: 16px;
#         z-index: 1000;
#         border-top: 1px solid #e5e7eb;
#     }
    
#     .stTextInput > div > div > input {
#         padding: 14px;
#         border-radius: 10px;
#         border: 1px solid #cbd5e1;
#         font-size: 16px;
#         background-color: #ffffff;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.05);
#     }
    
#     .stButton > button {
#         border-radius: 10px;
#         padding: 12px 20px;
#         background-color: #4dabf7;
#         color: white;
#         border: none;
#         transition: all 0.2s ease;
#         font-size: 16px;
#     }
    
#     .stButton > button:hover {
#         background-color: #339af0;
#         transform: translateY(-1px);
#         box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
#     }
    
#     /* Hide the Streamlit footer and hamburger menu */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
    
#     /* Sidebar styling */
#     .css-1d391kg {
#         background-color: #e7f5ff;
#     }
    
#     /* Custom separator */
#     .separator {
#         height: 1px;
#         background-color: #dee2e6;
#         margin: 15px 0;
#         width: 100%;
#     }
    
#     /* Loading animation */
#     .thinking {
#         display: flex;
#         align-items: center;
#         margin-top: 10px;
#     }
    
#     .dot {
#         display: inline-block;
#         width: 8px;
#         height: 8px;
#         border-radius: 50%;
#         background-color: #4dabf7;
#         margin-right: 4px;
#         animation: bounce 1.4s infinite ease-in-out both;
#     }
    
#     .dot:nth-child(1) { animation-delay: -0.32s; }
#     .dot:nth-child(2) { animation-delay: -0.16s; }
    
#     @keyframes bounce {
#         0%, 80%, 100% { transform: scale(0); }
#         40% { transform: scale(1.0); }
#     }
    
#     /* Form look cleaner */
#     .stForm {
#         background-color: transparent !important;
#         border: none !important;
#         padding: 0 !important;
#     }
    
#     .stForm > div {
#         padding: 0 !important;
#         border-width: 0 !important;
#     }
    
#     /* Adjust sidebar width */
#     .css-1d391kg {
#         width: 300px !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)


# # Initialize session state variables
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# if 'model_loaded' not in st.session_state:
#     st.session_state.model_loaded = False

# if 'model' not in st.session_state:
#     st.session_state.model = None

# if 'tokenizer' not in st.session_state:
#     st.session_state.tokenizer = None

# if 'form_submitted' not in st.session_state:
#     st.session_state.form_submitted = False

# if 'temp_input' not in st.session_state:
#     st.session_state.temp_input = ""

# def display_chat_message(role, content, avatar_symbol):
#     """Display a chat message with appropriate styling based on the role."""
#     avatar_class = "user-avatar" if role == "user" else "bot-avatar"
#     message_class = "user" if role == "user" else "bot"
    
#     st.markdown(f"""
#     <div class="chat-message {message_class}">
#         <div class="message-content">
#             <div class="avatar {avatar_class}">{avatar_symbol}</div>
#             <div>{content}</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# def load_model():
#     """Load the pre-trained model and tokenizer."""
#     try:
#         with st.spinner("Loading the AI model. This may take a moment..."):
#             # Path to your saved model - update this to your model's path
#             model_path = r"career_GPT_advisor_chatbot_125m_model"  
            
#             # For testing without the actual model, we can check if the path exists
#             if not os.path.exists(model_path):
#                 st.warning(f"Model path not found: {model_path}. Using a mock model for demonstration.")
#                 # Create a mock model and tokenizer for demonstration
#                 tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125m")
                
#                 # This is just for demonstration - in production you'd use your actual model
#                 try:
#                     model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125m")
#                 except Exception as e:
#                     st.error(f"Error loading demo model: {str(e)}")
#                     # Create a very basic mock model (this won't actually generate text, but allows the app to run)
#                     from transformers import AutoConfig
#                     config = AutoConfig.from_pretrained("EleutherAI/gpt-neo-125m")
#                     model = GPTNeoForCausalLM(config)
#             else:
#                 # Load your fine-tuned model
#                 tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125m")
#                 model = GPTNeoForCausalLM.from_pretrained(model_path)
            
#             # Check if GPU is available
#             device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#             model = model.to(device)
            
#             # Save to session state
#             st.session_state.model = model
#             st.session_state.tokenizer = tokenizer
#             st.session_state.device = device
            
#             return True
#     except Exception as e:
#         st.error(f"Error loading model: {str(e)}")
#         return False

# def mock_generate_response(prompt):
#     """A mock response generator that doesn't require the actual model."""
#     career_responses = {
#         "coding": "Based on your interest in coding, you might want to consider careers like Software Development, Web Development, Mobile App Development, or Data Science. These fields offer great growth potential and allow you to create impactful applications and solutions. To get started, I recommend learning programming languages like Python or JavaScript, and building small projects to develop your skills.",
#         "data": "For someone interested in data science, I recommend focusing on these key skills: statistical analysis, programming (Python/R), machine learning algorithms, data visualization, and SQL for database management. Many employers also value domain knowledge in fields like finance, healthcare, or marketing. Consider getting certifications from platforms like Coursera or edX to showcase your skills.",
#         "marketing": "Transitioning from marketing to product management is quite common! Your marketing background gives you valuable insights into customer needs. To make this switch, start by learning about product development processes, user experience design, and basic technical concepts. Try to get involved in product-related projects at your current job, and consider taking specialized courses in product management from platforms like Product School or General Assembly.",
#         "healthcare": "A career in healthcare typically requires specific education depending on the role. For doctors, you'll need a medical degree (MD) which takes about 8+ years of education after high school. Nursing requires a BSN (4 years) or ADN (2 years). Other options include: Physical Therapy (DPT degree), Healthcare Administration (bachelor's or master's), or Medical Technology (bachelor's degree). Many healthcare professions also require licensing exams and continuing education."
#     }
    
#     # Check for keywords in the prompt
#     response = "I can provide personalized career advice based on your interests and skills. What specific career path or industry are you interested in exploring?"
    
#     for keyword, reply in career_responses.items():
#         if keyword in prompt.lower():
#             response = reply
#             break
    
#     # Add some delay to simulate thinking
#     time.sleep(1.5)
#     return response

# def generate_response(user_input):
#     """Generate a response using the loaded model or a mock response for demonstration."""
#     try:
#         if not os.path.exists(r"career_GPT_advisor_chatbot_125m_model"):  # If model path doesn't exist
#             # Use mock response generator for demo purposes
#             return mock_generate_response(user_input)
        
#         model = st.session_state.model
#         tokenizer = st.session_state.tokenizer
#         device = st.session_state.device
        
#         # Tokenize input
#         inputs = tokenizer(user_input, return_tensors="pt").to(device)
        
#         # Generate text
#         outputs = model.generate(
#             inputs['input_ids'],
#             max_length=200,
#             num_beams=5,
#             no_repeat_ngram_size=2,
#             temperature=0.5,
#             top_p=0.9,
#             pad_token_id=tokenizer.eos_token_id
#         )
        
#         # Decode output
#         response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
#         # If the response includes the original prompt, remove it
#         if response.startswith(user_input):
#             response = response[len(user_input):].strip()
            
#         return response
#     except Exception as e:
#         return f"Sorry, I encountered an error: {str(e)}"

# # Callback function for form submission
# def handle_submit():
#     # Get the text from the input box
#     user_text = st.session_state.user_input
    
#     # Check if the input is not empty
#     if user_text.strip():
#         # Store the user input in temp_input before processing
#         st.session_state.temp_input = user_text
        
#         # Set a flag to indicate form was submitted
#         st.session_state.form_submitted = True

# # Function to set example question
# def set_example_question(question):
#     st.session_state.temp_input = question
#     st.session_state.form_submitted = True

# # Attempt to load the model automatically at startup
# if not st.session_state.model_loaded:
#     with st.spinner("Loading AI brain..."):
#         model_loaded = load_model()
#         if model_loaded:
#             st.session_state.model_loaded = True
#         else:
#             st.warning("Initial model loading failed. You can try loading it manually from the sidebar.")

# # Create a sidebar with information and example questions
# with st.sidebar:
#     st.title("Career Advisor AI")
    
#     st.markdown("### About")
#     st.markdown("""
#     This AI assistant provides personalized career advice based on your interests, skills, and goals.
    
#     Whether you're starting your career journey, looking to make a change, or exploring new opportunities, I'm here to help!
#     """)
    
#     # Model status indicator
#     if st.session_state.model_loaded:
#         st.success("AI model is loaded and ready!")
#     else:
#         if st.button("Load AI Model"):
#             with st.spinner("Loading AI brain..."):
#                 model_loaded = load_model()
#                 if model_loaded:
#                     st.session_state.model_loaded = True
#                     st.success("Model loaded successfully!")
#                 else:
#                     st.error("Failed to load model. Check console for details.")
    
#     st.markdown("### Example Questions")
#     st.caption("Click on any question to try it:")
    
#     example_questions = [
#         "What career paths are good for someone who enjoys coding?",
#         "What skills should I develop for a career in data science?",
#         "How can I transition from marketing to product management?",
#         "What education do I need for a career in healthcare?"
#     ]
    
#     for question in example_questions:
#         if st.button(question):
#             set_example_question(question)
    
#     st.markdown("### Tips")
#     st.markdown("""
#     For best results:
#     - Be specific about your interests and goals
#     - Mention your current skills and experience level
#     - Ask about specific industries you're curious about
#     - Inquire about skills needed for particular careers
#     """)

# # Main content area
# st.title(" Career Advisor AI")

# # Chat history container
# chat_container = st.container()
# chat_container.markdown('<div class="chat-container">', unsafe_allow_html=True)

# # Display chat history
# with chat_container:
#     # Add a welcome message if this is the first message
#     if len(st.session_state.chat_history) == 0:
#         display_chat_message(
#             "assistant", 
#             "Hello! I'm your Career Advisor AI. I can help you explore career paths, identify skills to develop, and navigate your professional journey. What would you like to know about?",
#             "🤖"
#         )
    
#     # Display all messages in the chat history
#     for message in st.session_state.chat_history:
#         display_chat_message(
#             message["role"], 
#             message["content"],
#             "👤" if message["role"] == "user" else "🤖"
#         )

# chat_container.markdown('</div>', unsafe_allow_html=True)

# # Input area fixed at the bottom
# st.markdown('<div class="input-container">', unsafe_allow_html=True)
# with st.form(key="chat_form", clear_on_submit=True):
#     col1, col2 = st.columns([6, 1])
    
#     with col1:
#         user_input = st.text_input("", 
#                                   key="user_input", 
#                                   placeholder="Ask me about career advice...",
#                                   label_visibility="collapsed")
    
#     with col2:
#         submit_button = st.form_submit_button("Send", on_click=handle_submit)
        
# st.markdown('</div>', unsafe_allow_html=True)

# # Process the submission
# if st.session_state.form_submitted:
#     # Get the user input from temp storage
#     user_text = st.session_state.temp_input
    
#     # Add user message to chat history
#     st.session_state.chat_history.append({"role": "user", "content": user_text})
    
#     # Check if model is loaded
#     if not st.session_state.model_loaded:
#         if load_model():
#             st.session_state.model_loaded = True
#         else:
#             st.session_state.chat_history.append({
#                 "role": "assistant", 
#                 "content": "I need to load my AI brain first. Please click 'Load AI Model' in the sidebar."
#             })
#             st.session_state.form_submitted = False
#             st.rerun()  # Using st.rerun() instead of experimental_rerun
    
#     # Generate response with a thinking animation
#     with st.spinner("Thinking..."):
#         if st.session_state.model_loaded:
#             response = generate_response(user_text)
#         else:
#             response = "Please load the model first by clicking the 'Load AI Model' button in the sidebar."
    
#     # Add assistant response to chat history
#     st.session_state.chat_history.append({"role": "assistant", "content": response})
    
#     # Reset the form_submitted flag
#     st.session_state.form_submitted = False
    
#     # Clear the temporary input
#     st.session_state.temp_input = ""
    
#     # Rerun to update the chat display
#     st.rerun()  # Using st.rerun() instead of experimental_rerun


# import streamlit as st
# import torch
# from transformers import GPTNeoForCausalLM, GPT2Tokenizer
# import time
# import os

# def apply_custom_css():
#     st.markdown("""
#     <style>
#     /* Main container styling */
#     .main {
#         background-color: #f8f9fa;
#         max-width: 1200px;
#         margin: 0 auto;
#         padding: 1rem;
#     }
    
#     /* Header styling */
#     .header-container {
#         text-align: center;
#         margin-bottom: 2rem;
#         padding: 1rem;
#         background-color: #ffffff;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#     }
    
#     .header-title {
#         font-size: 24px;
#         font-weight: 600;
#         color: #4361ee;
#         margin-bottom: 0.5rem;
#     }
    
#     .header-subtitle {
#         font-size: 16px;
#         color: #4f4f4f;
#     }
    
#     /* Chat container */
#     .chat-container {
#         display: flex;
#         flex-direction: column;
#         height: calc(100vh - 280px);
#         overflow-y: auto;
#         margin-bottom: 1rem;
#         padding: 1rem;
#         background-color: #ffffff;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#     }
    
#     /* Message styling */
#     .chat-message {
#         padding: 1rem;
#         border-radius: 8px;
#         margin-bottom: 1rem;
#         display: flex;
#         width: 100%;
#     }
    
#     .chat-message.user {
#         background-color: #e9ecef;
#         border-left: 4px solid #4361ee;
#     }
    
#     .chat-message.bot {
#         background-color: #f1f3f5;
#         border-left: 4px solid #3a0ca3;
#     }
    
#     .chat-message .avatar {
#         width: 32px;
#         height: 32px;
#         border-radius: 4px;
#         margin-right: 12px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 14px;
#         font-weight: bold;
#     }
    
#     .chat-message .user-avatar {
#         background-color: #4361ee;
#         color: white;
#     }
    
#     .chat-message .bot-avatar {
#         background-color: #3a0ca3;
#         color: white;
#     }
    
#     .chat-message .message-content {
#         flex-grow: 1;
#         line-height: 1.5;
#     }
    
#     /* Input area */
#     .input-container {
#         background-color: #ffffff;
#         padding: 1rem;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#         margin-top: 1rem;
#     }
    
#     .stTextInput > div > div > input {
#         border-radius: 8px;
#         border: 1px solid #dee2e6;
#         padding: 0.75rem;
#         font-size: 16px;
#     }
    
#     .stButton > button {
#         background-color: #4361ee;
#         color: white;
#         border-radius: 8px;
#         border: none;
#         padding: 0.75rem 1.5rem;
#         font-size: 16px;
#         font-weight: 500;
#         transition: all 0.2s;
#     }
    
#     .stButton > button:hover {
#         background-color: #3a0ca3;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#     }
    
#     /* Sidebar */
#     .css-1d391kg, .css-1vq4p4l {
#         background-color: #f8f9fa;
#     }
    
#     .sidebar-content {
#         background-color: #ffffff;
#         padding: 1.5rem;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#         margin-bottom: 1rem;
#     }
    
#     .sidebar-title {
#         font-size: 20px;
#         font-weight: 600;
#         color: #4361ee;
#         margin-bottom: 1rem;
#     }
    
#     /* Example questions */
#     .example-question {
#         background-color: #e9ecef;
#         color: #212529;
#         border-radius: 8px;
#         padding: 0.75rem;
#         margin-bottom: 0.5rem;
#         cursor: pointer;
#         transition: all 0.2s;
#         border-left: 3px solid #4361ee;
#     }
    
#     .example-question:hover {
#         background-color: #dee2e6;
#         transform: translateY(-2px);
#     }
    
#     /* Hide Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
    
#     /* Tab-like interface */
#     .tab-container {
#         display: flex;
#         background-color: #ffffff;
#         border-radius: 10px 10px 0 0;
#         overflow: hidden;
#         margin-bottom: 0;
#         box-shadow: 0 -4px 6px rgba(0,0,0,0.02);
#     }
    
#     .tab {
#         padding: 0.75rem 1.5rem;
#         background-color: #f1f3f5;
#         border-right: 1px solid #dee2e6;
#         font-weight: 500;
#         color: #4f4f4f;
#     }
    
#     .tab.active {
#         background-color: #ffffff;
#         color: #4361ee;
#         border-bottom: 3px solid #4361ee;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize session state variables
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# if 'model_loaded' not in st.session_state:
#     st.session_state.model_loaded = False

# if 'model' not in st.session_state:
#     st.session_state.model = None

# if 'tokenizer' not in st.session_state:
#     st.session_state.tokenizer = None

# if 'form_submitted' not in st.session_state:
#     st.session_state.form_submitted = False

# if 'temp_input' not in st.session_state:
#     st.session_state.temp_input = ""

# def display_chat_message(role, content):
#     """Display a chat message with appropriate styling based on the role."""
#     avatar_class = "user-avatar" if role == "user" else "bot-avatar"
#     message_class = "user" if role == "user" else "bot"
#     avatar_letter = "U" if role == "user" else "A"
    
#     st.markdown(f"""
#     <div class="chat-message {message_class}">
#         <div class="avatar {avatar_class}">{avatar_letter}</div>
#         <div class="message-content">{content}</div>
#     </div>
#     """, unsafe_allow_html=True)

# def load_model():
#     """Load the pre-trained model and tokenizer."""
#     try:
#         with st.spinner("Loading AI model..."):
#             # Path to your saved model
#             model_path = r"career_GPT_advisor_chatbot_125m_model"  
            
#             # Check if model path exists
#             if not os.path.exists(model_path):
#                 # Create a mock model and tokenizer for demonstration
#                 tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125m")
                
#                 try:
#                     model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125m")
#                 except Exception as e:
#                     from transformers import AutoConfig
#                     config = AutoConfig.from_pretrained("EleutherAI/gpt-neo-125m")
#                     model = GPTNeoForCausalLM(config)
#             else:
#                 # Load your fine-tuned model
#                 tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125m")
#                 model = GPTNeoForCausalLM.from_pretrained(model_path)
            
#             # Check if GPU is available
#             device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#             model = model.to(device)
            
#             # Save to session state
#             st.session_state.model = model
#             st.session_state.tokenizer = tokenizer
#             st.session_state.device = device
            
#             return True
#     except Exception as e:
#         st.error(f"Error loading model: {str(e)}")
#         return False

# def mock_generate_response(prompt):
#     """A mock response generator that doesn't require the actual model."""
#     career_responses = {
#         "coding": "Based on your interest in coding, you might consider careers in Software Development, Web Development, Mobile Apps, or Data Science. These fields offer growth potential and let you create impactful solutions. To start, learn Python or JavaScript and build small projects to develop your skills.",
#         "data": "For a data science career, focus on these key skills: statistical analysis, programming (Python/R), machine learning, data visualization, and SQL. Domain knowledge in fields like finance or healthcare is also valuable. Consider certifications from Coursera or edX to showcase your expertise.",
#         "marketing": "Transitioning from marketing to product management leverages your customer insights. Learn product development processes, UX design, and basic technical concepts. Get involved in product-related projects at your current job, and take specialized courses from Product School or General Assembly.",
#         "healthcare": "Healthcare careers require specific education: doctors need an MD (8+ years), nurses need a BSN (4 years) or ADN (2 years). Other options include Physical Therapy (DPT), Healthcare Administration (bachelor's/master's), or Medical Technology. Most require licensing exams and continuing education."
#     }
    
#     # Check for keywords in the prompt
#     response = "I can provide career advice based on your interests and skills. What career path or industry interests you?"
    
#     for keyword, reply in career_responses.items():
#         if keyword in prompt.lower():
#             response = reply
#             break
    
#     # Add some delay to simulate thinking
#     time.sleep(1)
#     return response

# def generate_response(user_input):
#     """Generate a response using the loaded model or a mock response."""
#     try:
#         if not os.path.exists(r"career_GPT_advisor_chatbot_125m_model"):
#             # Use mock response generator for demo purposes
#             return mock_generate_response(user_input)
        
#         model = st.session_state.model
#         tokenizer = st.session_state.tokenizer
#         device = st.session_state.device
        
#         # Tokenize input
#         inputs = tokenizer(user_input, return_tensors="pt").to(device)
        
#         # Generate text
#         outputs = model.generate(
#             inputs['input_ids'],
#             max_length=200,
#             num_beams=5,
#             no_repeat_ngram_size=2,
#             temperature=0.7,
#             top_p=0.9,
#             pad_token_id=tokenizer.eos_token_id
#         )
        
#         # Decode output
#         response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
#         # If the response includes the original prompt, remove it
#         if response.startswith(user_input):
#             response = response[len(user_input):].strip()
            
#         return response
#     except Exception as e:
#         return f"Sorry, I encountered an error: {str(e)}"

# # Callback function for form submission
# def handle_submit():
#     # Get the text from the input box
#     user_text = st.session_state.user_input
    
#     # Check if the input is not empty
#     if user_text.strip():
#         # Store the user input in temp_input before processing
#         st.session_state.temp_input = user_text
        
#         # Set a flag to indicate form was submitted
#         st.session_state.form_submitted = True

# # Function to set example question
# def set_example_question(question):
#     st.session_state.temp_input = question
#     st.session_state.form_submitted = True

# # Apply custom CSS
# apply_custom_css()

# # Attempt to load the model automatically at startup
# if not st.session_state.model_loaded:
#     model_loaded = load_model()
#     if model_loaded:
#         st.session_state.model_loaded = True

# # Create a sidebar with information
# with st.sidebar:
#     st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
#     st.markdown('<div class="sidebar-title">Career Advisor AI</div>', unsafe_allow_html=True)
    
#     st.markdown("### About")
#     st.markdown("""
#     This AI assistant provides personalized career advice based on your interests, skills, and goals.
#     """)
    
#     # Model status indicator
#     if st.session_state.model_loaded:
#         st.success("AI model is ready")
#     else:
#         if st.button("Load AI Model"):
#             with st.spinner("Loading AI model..."):
#                 model_loaded = load_model()
#                 if model_loaded:
#                     st.session_state.model_loaded = True
#                     st.success("Model loaded successfully")
#                 else:
#                     st.error("Failed to load model")
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
#     st.markdown("### Example Questions")
    
#     example_questions = [
#         "What career paths are good for someone who enjoys coding?",
#         "What skills should I develop for a career in data science?",
#         "How can I transition from marketing to product management?",
#         "What education do I need for a career in healthcare?"
#     ]
    
#     for question in example_questions:
#         st.markdown(f"""
#         <div class="example-question" onclick="
#             document.querySelector('.stTextInput input').value = '{question}';
#             document.querySelector('.stButton button').click();
#         ">{question}</div>
#         """, unsafe_allow_html=True)
        
#         # Hidden button for JavaScript interaction
#         if st.button(question, key=f"btn_{hash(question)}", help=question):
#             set_example_question(question)
#     st.markdown('</div>', unsafe_allow_html=True)

# # Main content area
# # Header with title and subtitle
# st.markdown("""
# <div class="header-container">
#     <div class="header-title">Career Advisor AI</div>
#     <div class="header-subtitle">How can I help with your career today?</div>
# </div>
# """, unsafe_allow_html=True)

# # Tab-like interface
# st.markdown("""
# <div class="tab-container">
#     <div class="tab active">Chat</div>
# </div>
# """, unsafe_allow_html=True)

# # Chat history container
# chat_container = st.container()
# chat_container.markdown('<div class="chat-container">', unsafe_allow_html=True)

# # Display chat history
# with chat_container:
#     # Add a welcome message if this is the first message
#     if len(st.session_state.chat_history) == 0:
#         display_chat_message(
#             "assistant", 
#             "Hello! I'm your Career Advisor. How can I help you today?"
#         )
    
#     # Display all messages in the chat history
#     for message in st.session_state.chat_history:
#         display_chat_message(
#             message["role"], 
#             message["content"]
#         )

# chat_container.markdown('</div>', unsafe_allow_html=True)

# # Input area
# st.markdown('<div class="input-container">', unsafe_allow_html=True)
# with st.form(key="chat_form", clear_on_submit=True):
#     col1, col2 = st.columns([6, 1])
    
#     with col1:
#         user_input = st.text_input("", 
#                                   key="user_input", 
#                                   placeholder="Ask about career advice...",
#                                   label_visibility="collapsed")
    
#     with col2:
#         submit_button = st.form_submit_button("Send", on_click=handle_submit)
        
# st.markdown('</div>', unsafe_allow_html=True)

# # Process the submission
# if st.session_state.form_submitted:
#     # Get the user input from temp storage
#     user_text = st.session_state.temp_input
    
#     # Add user message to chat history
#     st.session_state.chat_history.append({"role": "user", "content": user_text})
    
#     # Check if model is loaded
#     if not st.session_state.model_loaded:
#         if load_model():
#             st.session_state.model_loaded = True
#         else:
#             st.session_state.chat_history.append({
#                 "role": "assistant", 
#                 "content": "Please click 'Load AI Model' in the sidebar."
#             })
#             st.session_state.form_submitted = False
#             st.rerun()
    
#     # Generate response
#     with st.spinner("Thinking..."):
#         if st.session_state.model_loaded:
#             response = generate_response(user_text)
#         else:
#             response = "Please load the model first using the 'Load AI Model' button."
    
#     # Add assistant response to chat history
#     st.session_state.chat_history.append({"role": "assistant", "content": response})
    
#     # Reset the form_submitted flag
#     st.session_state.form_submitted = False
    
#     # Clear the temporary input
#     st.session_state.temp_input = ""
    
#     # Rerun to update the chat display
#     st.rerun()


import streamlit as st
import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import time
import os

def apply_custom_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Header styling */
    .header-title {
        text-align: center;
        font-size: 28px;
        font-weight: 600;
        color: #000000; 
        margin-bottom: 1rem;
    }
    
    /* Message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 9px;
        margin-bottom: 1rem;
        display: flex;
        width: 100%;
    }
    
    .chat-message.user {
        background-color: #e9ecef;
        border-left: 4px solid #4361ee;
    }
    
    .chat-message.bot {
        background-color: #f2fafc;
        border-left: 4px solid #3a0ca3;
    }
    
.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 700;
    color: #ffffff; /* White text */
    border: 3px solid #ffffff; /* White border */
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chat-message .avatar:hover {
    transform: scale(1.08);
    box-shadow: 0 6px 12px rgba(0,0,0,0.25);
}

.chat-message .user-avatar {
    background: linear-gradient(135deg, #FFA726, #FB8C00);
}

.chat-message .bot-avatar {
    background: linear-gradient(135deg, #F57C00, #EF6C00);
}


    
    .chat-message .message-content {
        flex-grow: 1;
        line-height: 1.5;
    }
    
    /* Input area */
    .input-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    
   
    .stButton > button {
        background-color: #FF8C00; /* Saffron color */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #D17A00; /* Darker saffron */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1vq4p4l {
        background-color: #f8f9fa;
    }
    
    .sidebar-title {
        font-size: 20px;
        font-weight: 600;
        color: #000000; /* Saffron color */
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab-like interface */
    .tab-container {
        display: flex;
        background-color: #ffffff;
        border-radius: 10px 10px 0 0;
        overflow: hidden;
        margin-bottom: 0;
        box-shadow: 0 -4px 6px rgba(0,0,0,0.02);
    }
    
    .tab {
        padding: 0.75rem 1.5rem;
        background-color: #f1f3f5;
        border-right: 1px solid #dee2e6;
        font-weight: 500;
        color: #4f4f4f;
    }
    
    .tab.active {
        background-color: #ffffff;
        color: #4361ee;
        border-bottom: 3px solid #4361ee;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

if 'model' not in st.session_state:
    st.session_state.model = None

if 'tokenizer' not in st.session_state:
    st.session_state.tokenizer = None

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if 'temp_input' not in st.session_state:
    st.session_state.temp_input = ""

def display_chat_message(role, content):
    """Display a chat message with appropriate styling based on the role."""
    avatar_class = "user-avatar" if role == "user" else "bot-avatar"
    message_class = "user" if role == "user" else "bot"
    avatar_letter = "U" if role == "user" else "A"
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="avatar {avatar_class}">{avatar_letter}</div>
        <div class="message-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def load_model():
    """Load the pre-trained model and tokenizer."""
    try:
        with st.spinner("Loading AI model..."):
            # Path to your saved model
            model_path = r"career_GPT_advisor_chatbot_125m_model"  
            
            # Check if model path exists
            if not os.path.exists(model_path):
                # Create a mock model and tokenizer for demonstration
                tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125m")
                
                try:
                    model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125m")
                except Exception as e:
                    from transformers import AutoConfig
                    config = AutoConfig.from_pretrained("EleutherAI/gpt-neo-125m")
                    model = GPTNeoForCausalLM(config)
            else:
                # Load your fine-tuned model
                tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125m")
                model = GPTNeoForCausalLM.from_pretrained(model_path)
            
            # Check if GPU is available
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = model.to(device)
            
            # Save to session state
            st.session_state.model = model
            st.session_state.tokenizer = tokenizer
            st.session_state.device = device
            
            return True
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return False

def mock_generate_response(prompt):
    """A mock response generator that doesn't require the actual model."""
    career_responses = {
        "coding": "Based on your interest in coding, you might consider careers in Software Development, Web Development, Mobile Apps, or Data Science. These fields offer growth potential and let you create impactful solutions. To start, learn Python or JavaScript and build small projects to develop your skills.",
        "data": "For a data science career, focus on these key skills: statistical analysis, programming (Python/R), machine learning, data visualization, and SQL. Domain knowledge in fields like finance or healthcare is also valuable. Consider certifications from Coursera or edX to showcase your expertise.",
        "marketing": "Transitioning from marketing to product management leverages your customer insights. Learn product development processes, UX design, and basic technical concepts. Get involved in product-related projects at your current job, and take specialized courses from Product School or General Assembly.",
        "healthcare": "Healthcare careers require specific education: doctors need an MD (8+ years), nurses need a BSN (4 years) or ADN (2 years). Other options include Physical Therapy (DPT), Healthcare Administration (bachelor's/master's), or Medical Technology. Most require licensing exams and continuing education."
    }
    
    # Check for keywords in the prompt
    response = "I can provide career advice based on your interests and skills. What career path or industry interests you?"
    
    for keyword, reply in career_responses.items():
        if keyword in prompt.lower():
            response = reply
            break
    
    # Add some delay to simulate thinking
    time.sleep(1)
    return response

def generate_response(user_input):
    """Generate a response using the loaded model or a mock response."""
    try:
        if not os.path.exists(r"career_GPT_advisor_chatbot_125m_model"):
            # Use mock response generator for demo purposes
            return mock_generate_response(user_input)
        
        model = st.session_state.model
        tokenizer = st.session_state.tokenizer
        device = st.session_state.device
        
        # Tokenize input
        inputs = tokenizer(user_input, return_tensors="pt").to(device)
        
        # Generate text - limit max_length to 200 characters
        outputs = model.generate(
            inputs['input_ids'],
            max_length=70,  # Lower max_length to approximately 200 characters
            num_beams=5,
            no_repeat_ngram_size=2,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
        
        # Decode output
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # If the response includes the original prompt, remove it
        if response.startswith(user_input):
            response = response[len(user_input):].strip()
            
        return response
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Callback function for form submission
def handle_submit():
    # Get the text from the input box
    user_text = st.session_state.user_input
    
    # Check if the input is not empty
    if user_text.strip():
        # Store the user input in temp_input before processing
        st.session_state.temp_input = user_text
        
        # Set a flag to indicate form was submitted
        st.session_state.form_submitted = True

# Function to set example question
def set_example_question(question):
    st.session_state.temp_input = question
    st.session_state.form_submitted = True

# Apply custom CSS
apply_custom_css()

# Attempt to load the model automatically at startup
if not st.session_state.model_loaded:
    model_loaded = load_model()
    if model_loaded:
        st.session_state.model_loaded = True

# Create a sidebar with information
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Career Orbit AI</div>', unsafe_allow_html=True)
    
    st.markdown("### About")
    st.markdown("""
    This AI assistant provides personalized career advice based on your interests, skills, and goals.
    """)
    
    # Model status indicator
    if st.session_state.model_loaded:
        st.success("AI model is ready")
    else:
        if st.button("Load AI Model"):
            with st.spinner("Loading AI model..."):
                model_loaded = load_model()
                if model_loaded:
                    st.session_state.model_loaded = True
                    st.success("Model loaded successfully")
                else:
                    st.error("Failed to load model")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### Example Questions")
    
    example_questions = [
        "What career paths are good for someone who enjoys coding?",
        "What skills should I develop for a career in data science?",
        "How can I transition from marketing to product management?",
        "What education do I need for a career in healthcare?"
    ]
    
    for question in example_questions:
        st.markdown(f"""
        <div class="example-question" onclick="
            document.querySelector('.stTextInput input').value = '{question}';
            document.querySelector('.stButton button').click();
        ">{question}</div>
        """, unsafe_allow_html=True)
        
        # Hidden button for JavaScript interaction
        if st.button(question, key=f"btn_{hash(question)}", help=question):
            set_example_question(question)
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area
# Simple title
st.markdown("""
<div class="header-title">̾Ｃａｒｅｅｒ Ｏｒｂｉｔ ＡＩ</div>
""", unsafe_allow_html=True)

# Chat history container
chat_container = st.container()
chat_container.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
with chat_container:
    # Add a welcome message if this is the first message
    if len(st.session_state.chat_history) == 0:
        display_chat_message(
            "assistant", 
            "How can I help with your career today?"
        )
    
    # Display all messages in the chat history
    for message in st.session_state.chat_history:
        display_chat_message(
            message["role"], 
            message["content"]
        )

chat_container.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input("", 
                                  key="user_input", 
                                  placeholder="Ask about career advice...",
                                  label_visibility="collapsed")
    
    with col2:
        submit_button = st.form_submit_button("Send", on_click=handle_submit)
        
st.markdown('</div>', unsafe_allow_html=True)

# Process the submission
if st.session_state.form_submitted:
    # Get the user input from temp storage
    user_text = st.session_state.temp_input
    
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_text})
    
    # Check if model is loaded
    if not st.session_state.model_loaded:
        if load_model():
            st.session_state.model_loaded = True
        else:
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": "Please click 'Load AI Model' in the sidebar."
            })
            st.session_state.form_submitted = False
            st.rerun()
    
    # Generate response
    with st.spinner("Thinking..."):
        if st.session_state.model_loaded:
            response = generate_response(user_text)
        else:
            response = "Please load the model first using the 'Load AI Model' button."
    
    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Reset the form_submitted flag
    st.session_state.form_submitted = False
    
    # Clear the temporary input
    st.session_state.temp_input = ""
    
    # Rerun to update the chat display
    st.rerun()