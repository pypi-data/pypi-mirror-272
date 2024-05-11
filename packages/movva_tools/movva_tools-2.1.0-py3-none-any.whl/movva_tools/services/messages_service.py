from movva_tools.exceptions import ObjectDoesNotExistException
from movva_tools.models.messages_models import RapidProMessages
from movva_tools.models.contacts_models import RapidProContacts, RapidProContactURN
from movva_tools.services.base_service import BaseService


class MessageService(BaseService):
    def __init__(
        self,
        _user=None, _host=None, _port=None, _db_name=None, _password=None,
        db_connection=None
    ) -> None:

        super().__init__(
            _user=_user, _password=_password,
            _host=_host, _port=_port,
            _db_name=_db_name,
            db_connection=db_connection
        )
        self.event_loop = None

        # model table entities
        self.Message = RapidProMessages
        self.Contact = RapidProContacts
        self.ContactURN = RapidProContactURN

    def fetch_message_by_id(self, message_id):
        message = self.db_connection.session.query(self.Message).filter_by(
            id=message_id
        ).first()

        if message:
            return message
        else:
            raise ObjectDoesNotExistException(dababase_object=self.Message)

    def fetch_messages_by_channel_and_org(self, channel_id, org_id, direction, status=None):
        if status:
            messages = self.db_connection.session.query(self.Message).filter_by(
                status=status,
                direction=direction,
                channel_id=channel_id,
                org_id=org_id
            ).all()
        else:
            messages = self.db_connection.session.query(self.Message).filter_by(
                channel_id=channel_id,
                direction=direction,
                org_id=org_id
            ).all()

        return messages if messages else []

    async def create(
        self, session, text, direction, status, visibility, msg_type, created_on, modified_on,
        sent_on, queued_on, channel_id, contact_id, contact_urn_id, org_id, topup_id,
        failed_reason, flow_id, next_attempt, external_id, attachments=None, msg_count=1,
        error_count=0, high_priority=False, contact_ids=[]
    ):
        async with session as async_session:
            message = self.Message(
                text=text,
                direction=direction,
                status=status,
                visibility=visibility,
                msg_type=msg_type,
                created_on=created_on,
                modified_on=modified_on,
                sent_on=sent_on,
                queued_on=queued_on,
                channel_id=channel_id,
                contact_id=contact_id,
                contact_urn_id=contact_urn_id,
                org_id=org_id,
                topup_id=topup_id,
                failed_reason=failed_reason,
                flow_id=flow_id,
                next_attempt=next_attempt,
                external_id=external_id,
                attachments=attachments,
                msg_count=msg_count,
                error_count=error_count,
                high_priority=high_priority,
                contact_ids=contact_ids
            )
            await async_session.add(message)
        await async_session.commit()

