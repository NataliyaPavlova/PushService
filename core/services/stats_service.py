from core.db_clickhouse.models import Log
from core.services.abstract_service import AbstractService


class StatsService(AbstractService):

    async def get_statuses_campaign(self, campaign_id: int) -> list[dict]:
        stat, pushes_set, cohorts_set = await self.stats_repository.get_statuses_by_pushes_in_campaign(
            campaign_id)
        result_stat = []
        events = [item for item in Log.Event]
        event_stat = dict.fromkeys(events, 0)
        push_stat = dict.fromkeys(pushes_set, event_stat)
        for item in stat:
            push_stat[item['push_id']][item['event']] += item['count']
        for push_id, push in push_stat.items():
            total_sendings = push[Log.Event.REMAINING] + push[Log.Event.SUCCESSFUL] \
                             + push[Log.Event.FAILED] + push[Log.Event.ERRORED]
            result_stat.append({
                'push_id': push_id,
                'received': round(push[Log.Event.RECEIVED] / total_sendings, 2) * 100,
                'converted': round(push[Log.Event.CONVERTED] / total_sendings, 2) * 100,
                'total': total_sendings
            })
        return result_stat

    async def insert(self, data: str) -> None:
        await self.stats_repository.insert(data)

    def get_statuses_campaign(self, campaign_id: int) -> list[dict]:
        stat, pushes_set = self.stats_repository.get_statuses_by_pushes_in_campaign(campaign_id)
        result_stat = []
        events = [Log.Event.REMAINING, Log.Event.SUCCESSFUL, Log.Event.FAILED,
                      Log.Event.ERRORED, Log.Event.CONVERTED, Log.Event.RECEIVED]
        event_stat = dict.fromkeys(events, 0)
        push_stat = dict.fromkeys(pushes_set, event_stat)
        for item in stat:
            push_stat[item['push_id']][item['event']] += item['count']
        for push_id, push in push_stat.items():
            total_sendings = push[Log.Event.REMAINING] + push[Log.Event.SUCCESSFUL] \
                             + push[Log.Event.FAILED] + push[Log.Event.ERRORED]
            result_stat.append({
                'push_id': push_id,
                'received': round(push[Log.Event.RECEIVED]/total_sendings, 2),
                'converted': round(push[Log.Event.CONVERTED]/total_sendings, 2)
            })
        return result_stat




