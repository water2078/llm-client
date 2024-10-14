import time
from typing import Optional
import uuid

from open_webui.apps.webui.internal.db import Base, get_db
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text

####################
# Usage DB Schema
####################


class Usage(Base):
    __tablename__ = "Usage"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    model = Column(Text)
    token_count = Column(BigInteger)
    created_at = Column(BigInteger)


class UsageModel(BaseModel):
    id: str
    user_id: str
    model: str
    token_count: int
    created_at: int
    model_config = ConfigDict(from_attributes=True)

####################
# Forms
####################


# class UserRoleUpdateForm(BaseModel):
#     id: str
#     role: str


# class UserUpdateForm(BaseModel):
#     name: str
#     email: str
#     profile_image_url: str
#     password: Optional[str] = None


class UsageTable:
    def insert_new_usage(
        self,
        user_id: str,
        model: str,
        token_count: int,
    ) -> Optional[UsageModel]:
        try:
            with get_db() as db:
                usage = UsageModel(
                    **{
                        "id":  str(uuid.uuid4()),
                        "user_id": user_id,
                        "model": model,
                        "token_count": token_count,
                        "created_at": int(time.time()),
                    }
                )
                result = Usage(**usage.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return usage
                else:
                    return None
        except Exception as e:
            print(e)
            return None

    def get_usages_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> list[UsageModel]:
        with get_db() as db:
            usages = (
                db.query(Usage)
                .filter_by(user_id=user_id)
                .order_by(Usage.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [UsageModel.model_validate(useage) for useage in usages]

    def get_usages(self, skip: int = 0, limit: int = 100) -> list[UsageModel]:
        with get_db() as db:
            usages = (
                db.query(Usage).order_by("created_at").offset(skip).limit(limit).all()
            )
            return [UsageModel.model_validate(useage) for useage in usages]


Usages = UsageTable()
