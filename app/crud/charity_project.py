from datetime import datetime
from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.core import format_timedelta
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject

DATE_TEMPLATE = '{days} days, {time}'


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            charity_project_name: int,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, str, str]]:
        charity_projects = await session.execute(
            select(CharityProject.name,
                   (extract('epoch', CharityProject.close_date) -
                    extract(
                        'epoch', CharityProject.create_date)
                    ).label('duration'),
                   CharityProject.description).where(
                CharityProject.fully_invested == True  # noqa
            ).group_by(
                (extract('epoch', CharityProject.close_date) -
                 extract('epoch', CharityProject.create_date))
            )
        )

        charity_projects = charity_projects.all()
        charity_projects_converted = []
        for charity_project in charity_projects:
            charity_project = dict(charity_project)
            charity_project['duration'] = format_timedelta(
                datetime.fromtimestamp(charity_project['duration']) -
                datetime.fromtimestamp(0)
            )
            charity_projects_converted.append(charity_project)

        return charity_projects_converted


charity_project_crud = CRUDCharityProject(CharityProject)
