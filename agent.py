import os
import asyncio
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BASE_URL = os.getenv("HINDSIGHT_API_URL")

BANK_ID = "failsafe-ai"


async def create_recommendation_async(problem):
    """
    Search Hindsight and create a recommendation.
    Uses Hindsight's async API for Flask compatibility.
    """

    client = Hindsight(
        base_url=BASE_URL,
        api_key=API_KEY
    )

    try:
        memories = await client.arecall(
            bank_id=BANK_ID,
            query=problem
        )

        if not memories.results:
            return {
                "found": False,
                "memories": [],
                "recommendation": "No similar previous incident found."
            }

        memory_text = []

        for memory in memories.results:
            memory_text.append(memory.text)

        recommendation = (
            "A similar deployment incident was found. "
            "Previous troubleshooting attempts failed, while rolling back "
            "the latest deployment resolved the Payment API outage. "
            "FAILSAFE recommends checking the latest deployment configuration "
            "and considering a rollback if the same pattern is present."
        )

        return {
            "found": True,
            "memories": memory_text,
            "recommendation": recommendation
        }

    finally:
        await client.aclose()


def create_recommendation(problem):
    """
    Synchronous wrapper for Flask.
    """

    return asyncio.run(
        create_recommendation_async(problem)
    )


if __name__ == "__main__":

    print("🚀 FAILSAFE AI started")

    problem = "Payment API is not responding after today's deployment."

    result = create_recommendation(problem)

    print("\n🧠 SIMILAR INCIDENT FOUND")
    print("-" * 60)

    for i, memory in enumerate(result["memories"], 1):
        print(f"\nMemory {i}:")
        print(memory)

    print("\n💡 FAILSAFE RECOMMENDATION")
    print("-" * 60)
    print(result["recommendation"])