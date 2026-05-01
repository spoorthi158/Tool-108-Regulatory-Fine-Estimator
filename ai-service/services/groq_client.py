import os
import time
import logging
from groq import Groq

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(prompt: str, temperature: float = 0.3, max_tokens: int = 1000) -> str:
    retries = 3
    timeout = 8  # 8 second timeout so fallback returns within 10 seconds

    for attempt in range(retries):
        try:
            start = time.time()
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout
            )
            elapsed = time.time() - start
            logger.info(f"[GROQ] Response received in {elapsed:.2f}s on attempt {attempt + 1}")
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Groq API error on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)

    return None