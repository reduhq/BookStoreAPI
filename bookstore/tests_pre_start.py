import asyncio
import logging

from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log

from bookstore.db.session import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        async with AsyncSessionLocal() as db:
        # Try to create session to check if DB is awake
            n = await db.execute("SELECT 1")
            logger.info(f"The test service was completed successfully: {n}")
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info("Initializing test service")
    await init()
    logger.info("Test service finished initializing")


if __name__ == "__main__":
    asyncio.run(main())