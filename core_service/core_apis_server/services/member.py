import logging
from fastapi import Request
from sqlalchemy.orm import Session

from core_service.core_apis_server.models.models import Member, Team, Organization
from core_service.core_apis_server.services.base import BaseService
from core_service.core_apis_server.exceptions import Err, ConflictException, NotFoundException
from core_service.core_apis_server.schemas.member import MemberCreate
from core_service.core_apis_server.utils import get_current_timestamp

LOG = logging.getLogger(__name__)


class MemberService(BaseService):

    def __init__(self, db_session: Session, token: str = None,
                 request: Request = None, **kwargs):
        super().__init__(db_session, token, request, **kwargs)

    def _get_model_type(self):
        return Member

    def _update_org_members_count(self, organization_id: str):
        org = self._session.query(Organization).filter(
            Organization.id == organization_id
        ).first()
        if org:
            org.members_count = self._session.query(Member).join(Team).filter(
                Team.organization_id == organization_id,
                Team.deleted_at      == 0,
                Member.deleted_at    == 0,
            ).count()
            self._session.commit()

    async def add_member(self, team_id: str,
                          payload: MemberCreate) -> Member:
        team = self._session.query(Team).filter(
            Team.id         == team_id,
            Team.deleted_at == 0,
        ).first()
        if not team:
            raise NotFoundException(Err.OC0012, [team_id])

        existing = self._session.query(Member).filter(
            Member.team_id      == team_id,
            Member.auth_user_id == payload.auth_user_id,
            Member.deleted_at   == 0,
        ).first()
        if existing:
            raise ConflictException(Err.OC0017)

        member = Member(
            team_id      = team_id,
            auth_user_id = payload.auth_user_id,
        )
        result = self.save(member)

        self._update_org_members_count(team.organization_id)

        return result

    async def list_members_by_team(self, team_id: str,
                                    skip: int = 0,
                                    limit: int = 20):
        query = self._session.query(Member).filter(
            Member.team_id    == team_id,
            Member.deleted_at == 0,
        )
        total   = query.count()
        members = query.offset(skip).limit(limit).all()
        return members, total

    async def remove_member(self, member_id: str):
        member = self.get_by_id(member_id)
        team   = self._session.query(Team).filter(
            Team.id == member.team_id
        ).first()
        self.soft_delete(member_id)
        if team:
            self._update_org_members_count(team.organization_id)