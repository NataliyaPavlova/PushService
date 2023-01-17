from core.db_clickhouse.repository.abstract_repository import AbstractRepositoryClickHouse


class StatsRepository(AbstractRepositoryClickHouse):
    # model = 'notification.Log'

    async def get_statuses_by_pushes_in_campaign(self, campaign_id: int) -> tuple:
        stat = []
        pushes = set()
        async for row in self.client.iterate(
            "SELECT push_id, event, number_of_events FROM notification.Log WHERE campaign_id={campaign_id}",
                params={'campaign_id': campaign_id}):
            stat.append({'push_id': row[0], 'event': row[1], 'count': row[2]})
            pushes.add(row[0])
        return stat, pushes

    async def get_user_distribution_by_pushes(self, campaign_id: int) -> list[dict]:
        stat = []
        async for row in self.client.iterate(
            "SELECT push_id, count(*) as cnt FROM notification.Log WHERE campaign_id={campaign_id} AND event='opened' GROUP BY push_id",
                params={'campaign_id': campaign_id}):
            stat.append({'push_id': row['push_id'], 'count': row['cnt']})
        return stat

    async def insert(self, data: str) -> None:
        sql = (f'INSERT INTO notification.Log '
               f'(push_tokens, created_at, completed_at, event, number_of_events, notification_id, campaign_id, cohort_id, push_id) VALUES {data}')
        await self.client.execute(sql)
