import os
from openai import AsyncOpenAI
import re

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_text_file(filename: str, fallback: str = "") -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception:
        return fallback

SYSTEM_PROMPT = load_text_file("utils/assistant_prompt.txt", "Ти — AI-помічник.")
KNOWLEDGE_CONTEXT = load_text_file("utils/assistant_knowledge.txt", "")

async def ask_openai(prompt: str, history: str = "", extra_knowledge: str = "") -> dict:
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if KNOWLEDGE_CONTEXT:
            messages.append({"role": "system", "content": f"Корисна інформація:\n{KNOWLEDGE_CONTEXT}"})

        if extra_knowledge:
            messages.append({"role": "system", "content": f"Додаткова інформація:\n{extra_knowledge}"})

        if history:
            for line in history.splitlines():
                if line.startswith("👤"):
                    messages.append({"role": "user", "content": line[2:].strip()})
                elif line.startswith("🤖"):
                    messages.append({"role": "assistant", "content": line[2:].strip()})

        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )

        reply_raw = response.choices[0].message.content.strip()
        reply = reply_raw.lower()

        not_confident = "[ask_owner]" in reply
        extra_tag = None
        match = re.search(r"\[(\w+)\]", reply)
        if match and match.group(1).lower() not in ["ask_owner"]:
            extra_tag = match.group(1).upper()

        reply_clean = re.sub(r"\[[^\]]+\]", "", reply_raw).strip()

        return {
            "text": reply_clean,
            "not_confident": not_confident,
            "extra_tag": extra_tag
        }

    except Exception as e:
        return {
            "text": f"⚠️ Помилка AI: {e}",
            "not_confident": True,
            "extra_tag": None
        }
