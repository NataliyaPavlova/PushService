from admin_api.src.services.batch_service import BatchService
from admin_api.src.services.stats_service import StatsService
from admin_api.src.db.repository.batch_repository import BatchRepository
from admin_api.src.db.repository.stats_repository import StatsRepository


async def get_batch_service_callback(sessions):
    async for session in sessions:
        batch_repository = BatchRepository(session)
        batch_service = BatchService(batch_repository)
        return batch_service


async def get_stats_service_callback(sessions):
    async for session in sessions:
        stats_repository = StatsRepository(session)
        stats_service = StatsService(stats_repository)
        return stats_service
