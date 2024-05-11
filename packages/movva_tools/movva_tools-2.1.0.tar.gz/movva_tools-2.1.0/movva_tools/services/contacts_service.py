from movva_tools.services.base_service import BaseService
from movva_tools.models.contacts_models import (
    RapidProContactFields, RapidProContacts,
    RapidProContactGroups, RapidProContactGroupsContacts
)
from movva_tools.exceptions import ObjectDoesNotExistException
from movva_tools.models.contacts_models import RapidProContactURN
from sqlalchemy import or_


class ContactService(BaseService):

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

        # model table entities
        self.Contact = RapidProContacts
        self.ContactFields = RapidProContactFields
        self.ContactGroups = RapidProContactGroups
        self.ContactGroupsContacts = RapidProContactGroupsContacts

    def get_contact_group_by_id(self, id):
        contact_group = self.db_connection.session.query(
            self.ContactGroups
        ).filter_by(
            id=id
        ).first()

        if contact_group:
            return contact_group
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactGroups
            )

    def get_contact_group_by_name(self, name, org_id):
        contact_group = self.db_connection.session.query(
            self.ContactGroups
        ).filter_by(
            name=name,
            org_id=org_id
        ).first()

        if contact_group:
            return contact_group
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactGroups
            )

    def get_contact_groups_contact_by_contact_id(self, contact_id_list: list):
        contacts_groups_contacts = self.db_connection.session.query(
            self.ContactGroupsContacts
        ).filter(
            self.ContactGroupsContacts.contact_id.in_(contact_id_list)
        )

        groups = []
        contact_ids = []
        for contact_group_contact in contacts_groups_contacts:
            groups.append(
                contact_group_contact.contactgroup_id
            )
            contact_ids.append(
                contact_group_contact.contact_id
            )

        return contact_ids, groups

    def get_contacfield_by_label(self, org, label):
        contact_field = self.db_connection.session.query(
            self.ContactFields
        ).filter_by(
            label=label,
            org_id=org.id
        ).first()

        if contact_field:
            return contact_field
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactFields
            )


class ContactURNService(BaseService):

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

        self.ContactURN = RapidProContactURN

    def get_contact_urn_by_contact_id(self, contact_id):

        contact_urn = self.db_connection.session.query(
            self.ContactURN
        ).filter_by(
            contact_id=contact_id
        ).first()

        if not contact_urn:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactURN
            )

        return contact_urn

    def batch_get_contact_urn_by_contact_id(self, contact_id_list: list):

        contact_urns = self.db_connection.session.query(
            self.ContactURN
        ).filter(
            self.ContactURN.contact_id.in_(contact_id_list)
        )

        if not contact_urns:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactURN
            )

        return contact_urns

    def batch_get_contact_urn_by_identity(self, identities_list: list):

        contact_urns = self.db_connection.session.query(
            self.ContactURN
        ).filter(
            or_(
                *[self.ContactURN.identity.like(f'%{identity}%') for identity in identities_list]  # noqa
            )
        )

        if not contact_urns:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactURN
            )

        return contact_urns
