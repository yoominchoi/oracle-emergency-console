# oracle-emergency-console
Oracle Summer 2024 Internship (Full Stack app development)
AI-Powered Public Safety app: Emergency Console Communication Tool for Government & Organizations

Youtube Link: https://www.youtube.com/watch?v=Kr4Z4bmoPXA

Hello everyone! I’m Yoomin Choi, a Developer Advocate Intern in the Oracle Database Developers Relations Team. I'm currently a 3rd year Computer Science student at Georgia Tech.

Today, I am going to present a working demo application for AI-Powered Public Safety app: Emergency Console Communication Tool for Government & Organizations. This app is designed to assist emergency response teams and safety managers in handling critical situations effectively. It leverages cutting-edge technologies including RAG (Retrieval-Augmented Generation), Vector Search, OCI AI Llama inference models, and Generative AI.

For the full stack development, I used Python for the backend, Streamlit for the frontend framework, Oracle 23ai Database for data storage and processing, and Jupyter Notebook for interacting with the Generative AI models.

This app facilitates interactions between admin users, such as 911 operators or safety managers, and general users involved in emergency situations. The goal is to enable rapid, informed decision-making to ensure the safety and well-being of all individuals.

Here's the entity relationship diagram of our database. The primary tables are USERS, INCIDENTS, and INCIDENT_DETAILS. The USERS table includes attributes like id, name, and user_type, which specifies whether the user is an admin or a general user. Admin users manage emergency situations, while general users provide on-the-ground information.

The INCIDENTS table logs each emergency event, and the INCIDENT_DETAILS table captures specifics like the shooter’s location, description, and alerts sent from admin to general users. General users are those affected by or witnessing the emergency.

For Jupyter Notebook (vectorization.ipynb) file:
We utilized RAG and Vector Search functionalities of the Oracle Database with OCI AI Llama Inference models to generate reports. This system is built with privacy in mind, using internal data without sharing it externally.

RAG involves retrieving relevant shooter descriptions and augmenting prompts for the AI model to generate coherent summaries. The model is privately hosted on OCI, ensuring data security.

Using Oracle Database and its AI capabilities offers several advantages for our public safety app:

1. **Easy and fast Integration**:
    - The integration ensures that both admin and general users have access to the most current and accurate information.
    - Oracle Database allows easy integration of data operations, ensuring that updates, such as new alerts or shooter descriptions, are reflected across the application in real-time.
2. **Scalability and Performance**:
    - Oracle Database scales effortlessly with the app’s needs, providing high performance even as the number of incidents and user interactions grow.
    - Advanced features like Vector Search enhance the ability to handle complex queries and large datasets efficiently, crucial for processing detailed incident reports.
3. **Security**:
    - Ensuring data privacy by not sharing internal data externally is critical for maintaining trust and confidentiality in emergency situations.
    - Oracle’s robust security measures protect sensitive data, such as emergency reports and user details, from unauthorized access.
4. **Ease of Use with AI**:
    - Oracle's AI integration capabilities, such as using Generative AI and Llama Inference models, simplify incorporating AI features into our app.
    - The combination of RAG and Oracle AI services enables intelligent features like automated report generation, which helps in quickly summarizing detailed shooter descriptions, enhancing the app’s functionality and user experience.

Using Oracle Database and AI makes it easy to manage and update data smoothly, ensuring all users have the most current information. This demonstrates the robust capabilities of Oracle DB in handling dynamic data efficiently while enhancing the app's performance and usability with AI integration.