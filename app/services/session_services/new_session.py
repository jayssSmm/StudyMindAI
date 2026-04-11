from app.services.llm_services import groq_provider
from app.services.db_services import session_table

def create_new_session(user_id,prompt):
    session_id = session_table.add_session(user_id,(groq_provider.session_title(prompt)))
    return session_id