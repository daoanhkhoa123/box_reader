# import logging
# from datetime import date
# from typing import Iterable, List, Optional

# from sqlalchemy import func
# from sqlalchemy.orm import Session

# from src.domain.entities import News
# from src.domain.repositories import BaseNewsRepository
# from src.infrastructure.database.models import NewsModel

# logger = logging.getLogger(__name__)


# class NewsRepository(BaseNewsRepository):
#     def __init__(self, session: Session):
#         self.session = session
#         self.logger = logger.getChild(self.__class__.__name__)

#         self.logger.debug("Initialized with session=%s", session)

#     # ---------- WRITE ----------

#     def save(self, news: News) -> News:
#         self.logger.debug(
#             "Saving news url=%s source=%s published_date=%s",
#             news.url,
#             news.source,
#             news.published_date,
#         )

#         model = NewsModel.from_entity(news)
#         self.session.add(model)
#         self.session.flush()

#         self.logger.info(
#             "Saved news id=%s url=%s",
#             model.id,
#             model.url,
#         )

#         return model.to_entity()

#     def save_many(self, news_iterable: Iterable[News]) -> List[News]:
#         models = [NewsModel.from_entity(n) for n in news_iterable]

#         if not models:
#             self.logger.debug("save_many called with empty iterable")
#             return []

#         self.logger.debug("Saving %d news items", len(models))

#         self.session.add_all(models)
#         self.session.flush()

#         self.logger.info("Saved %d news items", len(models))
#         return [m.to_entity() for m in models]

#     # ---------- READ ----------

#     def exists_by_url(self, url: str) -> bool:
#         exists = (
#             self.session.query(NewsModel.id)
#             .filter(NewsModel.url == url)
#             .first()
#             is not None
#         )

#         self.logger.debug("exists_by_url url=%s exists=%s", url, exists)
#         return exists

#     def get_latest(self, limit: int = 10) -> List[News]:
#         self.logger.debug("Fetching latest news limit=%d", limit)

#         models = (
#             self.session.query(NewsModel)
#             .order_by(NewsModel.published_date.desc())
#             .limit(limit)
#             .all()
#         )

#         self.logger.info("Fetched %d latest news items", len(models))
#         return [m.to_entity() for m in models]

#     def get_latest_date_by_source(self, source: str) -> Optional[date]:
#         latest_date = (
#             self.session.query(func.max(NewsModel.published_date))
#             .filter(NewsModel.source == source)
#             .scalar()
#         )

#         self.logger.debug(
#             "Latest published_date for source=%s is %s",
#             source,
#             latest_date,
#         )
#         return latest_date

#     def get_not_summarized(self) -> List[News]:
#         models = (
#             self.session.query(NewsModel)
#             .filter(NewsModel.summarized.is_(False))
#             .all()
#         )

#         self.logger.info(
#             "Fetched %d not-summarized news items",
#             len(models),
#         )
#         return [m.to_entity() for m in models]

#     # ---------- DOMAIN RULE ----------

#     def is_duplicate_or_outdated(
#         self,
#         *,
#         url: str,
#         published_date: date,
#         source: str,
#     ) -> bool:
#         if self.exists_by_url(url):
#             self.logger.debug("Duplicate news detected url=%s", url)
#             return True

#         latest_date = self.get_latest_date_by_source(source)
#         if latest_date is None:
#             self.logger.debug(
#                 "No existing news for source=%s, treating as new",
#                 source,
#             )
#             return False

#         outdated = published_date <= latest_date
#         self.logger.debug(
#             "Outdated check url=%s published_date=%s latest_date=%s result=%s",
#             url,
#             published_date,
#             latest_date,
#             outdated,
#         )

#         return outdated

#     def mark_many_as_summarized(self, news_ids: List[int]) -> int:
#         if not news_ids:
#             self.logger.debug("mark_many_as_summarized called with empty list")
#             return 0

#         updated = (
#             self.session.query(NewsModel)
#             .filter(
#                 NewsModel.id.in_(news_ids),
#                 NewsModel.summarized.is_(False),
#             )
#             .update(
#                 {NewsModel.summarized: True},
#                 synchronize_session=False,
#             )
#         )

#         self.logger.warning(
#             "Marked %d news items as summarized ids=%s",
#             updated,
#             news_ids,
#         )
#         return updated
