from backend.utils.functions import upload_questions_to_supabase


upload_questions_to_supabase(file_path='./Data/final_dataset/final_dataset.csv', table_name="Questions")