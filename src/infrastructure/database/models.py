# from sqlalchemy import (
#     Column,
#     Date,
#     DateTime,
#     Integer,
#     String,
#     Text,
#     UniqueConstraint,
#     Boolean,
#     func,
# )
# from sqlalchemy.orm import declarative_base

# from src.domain.entities import News

# Base = declarative_base()


# class NewsModel(Base):
#     __tablename__ = "news"

#     id = Column(Integer, primary_key=True)
#     title = Column(String(500), nullable=False)
#     url = Column(Text, nullable=False)
#     published_date = Column(Date, nullable=False)
#     source = Column(String(200), nullable=False)

#     summarized = Column(Boolean, nullable=False, default=False)

#     created_at = Column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         nullable=False,
#     )

#     __table_args__ = (
#         UniqueConstraint("url", name="uq_news_url"),
#     )

#     # ---------- MAPPING ----------

#     def to_entity(self) -> News:
#         return News(
#             id=self.id, # type: ignore
#             title=self.title, # type: ignore
#             url=self.url, # type: ignore
#             published_date=self.published_date, # type: ignore
#             source=self.source, # type: ignore
#             created_at=self.created_at, # type: ignore
#             summarized=bool(self.summarized),
#         )

#     @classmethod
#     def from_entity(cls, entity: News) -> "NewsModel":
#         return cls(
#             title=entity.title,
#             url=entity.url,
#             published_date=entity.published_date,
#             source=entity.source,
#             summarized=entity.summarized,
#         )
