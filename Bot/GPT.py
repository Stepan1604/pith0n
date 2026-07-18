from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Prompt
from huggingface_hub import InferenceClient
from ENV.env import LLM_TOKEN, MODEL_PATH, QDRANT_HOST, QDRANT_PORT
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

# Initialize LLM client
api_key = LLM_TOKEN
if not api_key:
    logger.warning("LLM_TOKEN not set - LLM features will not work")

client = InferenceClient(api_key=api_key)

# Initialize embedding model and vector DB
try:
    model_token = SentenceTransformer(MODEL_PATH)
    logger.info(f"Loaded embedding model: {MODEL_PATH}")
except Exception as e:
    logger.error(f"Failed to load embedding model: {e}")
    model_token = None

try:
    client_token = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    logger.info(f"Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
except Exception as e:
    logger.error(f"Failed to connect to Qdrant: {e}")
    client_token = None


async def llm_request(
        session: Session,
        messages: list[dict],
        age: int | None = None,
        model: str = "meta-llama/Llama-2-7b-chat-hf",
) -> str:
    """
    Generate LLM response with RAG and system prompts
    
    Args:
        session: Database session
        messages: Chat messages list
        age: User age for personalization
        model: Model to use for inference
    
    Returns:
        Generated response text
    """
    try:
        # Fetch active system prompts from database
        result = await session.execute(
            select(Prompt)
            .where(Prompt.is_active == True)
            .order_by(Prompt.id)
        )
        prompts = result.scalars().all()

        system_parts: list[str] = []

        # Add all active prompts to system message
        for prompt in prompts:
            system_parts.append(prompt.content)

        # Add age-specific instruction
        if age:
            system_parts.append(
                f"Отвечай так, чтобы было понятно человеку, возрастом {age} лет."
            )

        # RAG: Get relevant context from vector DB
        rag_context = ""
        if model_token and client_token:
            try:
                user_query = messages[-1].get("content", "")
                vector = model_token.encode(user_query).tolist()
                
                result = client_token.query_points(
                    collection_name="Constitution",
                    query=vector,
                    limit=3,
                    search_params=models.SearchParams(hnsw_ef=128, exact=False),
                )
                
                if result.points:
                    rag_context = "\n".join([point.payload.get("text", "") for point in result.points])
                    system_parts.append(
                        f"При ответе на вопрос используй следующую нормативно-правовую информацию:\n{rag_context}"
                    )
            except Exception as e:
                logger.warning(f"RAG query failed: {e}")

        # Combine all system parts
        system_prompt = "\n\n".join(system_parts)
        
        # Prepare messages for API
        api_messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            *messages,
        ]

        # Call LLM API
        chat_response = client.chat.completions.create(
            model=model,
            temperature=0.5,
            top_p=0.9,
            max_tokens=512,
            messages=api_messages,
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        logger.error(f"LLM request failed: {e}")
        return f"Извините, произошла ошибка при генерации ответа: {str(e)}"


async def generate_meal_plan(
        session: Session,
        height: int,
        weight: int,
        age: int,
        sports: bool,
        allergies: str,
        budget: int,
        goal: str,
        preferences: str,
        duration: str = "week",
) -> str:
    """
    Generate personalized meal plan using LLM
    
    Args:
        session: Database session
        height: User height in cm
        weight: User weight in kg
        age: User age
        sports: Whether user does sports
        allergies: User allergies
        budget: Weekly/monthly budget
        goal: Nutrition goal (lose_weight, stay_fit, balanced, family_menu)
        preferences: Food preferences
        duration: Plan duration (week or month)
    
    Returns:
        Generated meal plan
    """
    
    prompt_text = f"""
    Создай план питания на {duration} для человека со следующими параметрами:
    - Возраст: {age} лет
    - Рост: {height} см
    - Вес: {weight} кг
    - Занимается спортом: {'Да' if sports else 'Нет'}
    - Аллергии: {allergies if allergies else 'Нет'}
    - Бюджет: {budget} руб.
    - Цель: {goal}
    - Предпочтения: {preferences}
    
    Составь детальный план питания с учетом всех параметров.
    """
    
    messages = [
        {
            "role": "user",
            "content": prompt_text
        }
    ]
    
    return await llm_request(session, messages, age=age)
