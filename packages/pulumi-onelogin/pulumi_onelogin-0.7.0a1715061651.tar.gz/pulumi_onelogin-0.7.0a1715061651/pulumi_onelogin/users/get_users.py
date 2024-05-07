# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetUsersResult',
    'AwaitableGetUsersResult',
    'get_users',
    'get_users_output',
]

@pulumi.output_type
class GetUsersResult:
    """
    A collection of values returned by getUsers.
    """
    def __init__(__self__, activated_at=None, comment=None, company=None, created_at=None, department=None, directory_id=None, distinguished_name=None, email=None, external_id=None, filters=None, firstname=None, group_id=None, id=None, invalid_login_attempts=None, invitation_sent_at=None, last_login=None, lastname=None, locked_until=None, manager_ad_id=None, manager_user_id=None, member_of=None, password=None, password_algorithm=None, password_changed_at=None, password_confirmation=None, phone=None, preferred_locale_code=None, role_ids=None, salt=None, samaccountname=None, state=None, status=None, title=None, trusted_idp_id=None, updated_at=None, username=None, userprincipalname=None):
        if activated_at and not isinstance(activated_at, str):
            raise TypeError("Expected argument 'activated_at' to be a str")
        pulumi.set(__self__, "activated_at", activated_at)
        if comment and not isinstance(comment, str):
            raise TypeError("Expected argument 'comment' to be a str")
        pulumi.set(__self__, "comment", comment)
        if company and not isinstance(company, str):
            raise TypeError("Expected argument 'company' to be a str")
        pulumi.set(__self__, "company", company)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if department and not isinstance(department, str):
            raise TypeError("Expected argument 'department' to be a str")
        pulumi.set(__self__, "department", department)
        if directory_id and not isinstance(directory_id, int):
            raise TypeError("Expected argument 'directory_id' to be a int")
        pulumi.set(__self__, "directory_id", directory_id)
        if distinguished_name and not isinstance(distinguished_name, str):
            raise TypeError("Expected argument 'distinguished_name' to be a str")
        pulumi.set(__self__, "distinguished_name", distinguished_name)
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        pulumi.set(__self__, "email", email)
        if external_id and not isinstance(external_id, str):
            raise TypeError("Expected argument 'external_id' to be a str")
        pulumi.set(__self__, "external_id", external_id)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if firstname and not isinstance(firstname, str):
            raise TypeError("Expected argument 'firstname' to be a str")
        pulumi.set(__self__, "firstname", firstname)
        if group_id and not isinstance(group_id, int):
            raise TypeError("Expected argument 'group_id' to be a int")
        pulumi.set(__self__, "group_id", group_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if invalid_login_attempts and not isinstance(invalid_login_attempts, int):
            raise TypeError("Expected argument 'invalid_login_attempts' to be a int")
        pulumi.set(__self__, "invalid_login_attempts", invalid_login_attempts)
        if invitation_sent_at and not isinstance(invitation_sent_at, str):
            raise TypeError("Expected argument 'invitation_sent_at' to be a str")
        pulumi.set(__self__, "invitation_sent_at", invitation_sent_at)
        if last_login and not isinstance(last_login, str):
            raise TypeError("Expected argument 'last_login' to be a str")
        pulumi.set(__self__, "last_login", last_login)
        if lastname and not isinstance(lastname, str):
            raise TypeError("Expected argument 'lastname' to be a str")
        pulumi.set(__self__, "lastname", lastname)
        if locked_until and not isinstance(locked_until, str):
            raise TypeError("Expected argument 'locked_until' to be a str")
        pulumi.set(__self__, "locked_until", locked_until)
        if manager_ad_id and not isinstance(manager_ad_id, str):
            raise TypeError("Expected argument 'manager_ad_id' to be a str")
        pulumi.set(__self__, "manager_ad_id", manager_ad_id)
        if manager_user_id and not isinstance(manager_user_id, str):
            raise TypeError("Expected argument 'manager_user_id' to be a str")
        pulumi.set(__self__, "manager_user_id", manager_user_id)
        if member_of and not isinstance(member_of, str):
            raise TypeError("Expected argument 'member_of' to be a str")
        pulumi.set(__self__, "member_of", member_of)
        if password and not isinstance(password, str):
            raise TypeError("Expected argument 'password' to be a str")
        pulumi.set(__self__, "password", password)
        if password_algorithm and not isinstance(password_algorithm, str):
            raise TypeError("Expected argument 'password_algorithm' to be a str")
        pulumi.set(__self__, "password_algorithm", password_algorithm)
        if password_changed_at and not isinstance(password_changed_at, str):
            raise TypeError("Expected argument 'password_changed_at' to be a str")
        pulumi.set(__self__, "password_changed_at", password_changed_at)
        if password_confirmation and not isinstance(password_confirmation, str):
            raise TypeError("Expected argument 'password_confirmation' to be a str")
        pulumi.set(__self__, "password_confirmation", password_confirmation)
        if phone and not isinstance(phone, str):
            raise TypeError("Expected argument 'phone' to be a str")
        pulumi.set(__self__, "phone", phone)
        if preferred_locale_code and not isinstance(preferred_locale_code, str):
            raise TypeError("Expected argument 'preferred_locale_code' to be a str")
        pulumi.set(__self__, "preferred_locale_code", preferred_locale_code)
        if role_ids and not isinstance(role_ids, list):
            raise TypeError("Expected argument 'role_ids' to be a list")
        pulumi.set(__self__, "role_ids", role_ids)
        if salt and not isinstance(salt, str):
            raise TypeError("Expected argument 'salt' to be a str")
        pulumi.set(__self__, "salt", salt)
        if samaccountname and not isinstance(samaccountname, str):
            raise TypeError("Expected argument 'samaccountname' to be a str")
        pulumi.set(__self__, "samaccountname", samaccountname)
        if state and not isinstance(state, int):
            raise TypeError("Expected argument 'state' to be a int")
        pulumi.set(__self__, "state", state)
        if status and not isinstance(status, int):
            raise TypeError("Expected argument 'status' to be a int")
        pulumi.set(__self__, "status", status)
        if title and not isinstance(title, str):
            raise TypeError("Expected argument 'title' to be a str")
        pulumi.set(__self__, "title", title)
        if trusted_idp_id and not isinstance(trusted_idp_id, int):
            raise TypeError("Expected argument 'trusted_idp_id' to be a int")
        pulumi.set(__self__, "trusted_idp_id", trusted_idp_id)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)
        if username and not isinstance(username, str):
            raise TypeError("Expected argument 'username' to be a str")
        pulumi.set(__self__, "username", username)
        if userprincipalname and not isinstance(userprincipalname, str):
            raise TypeError("Expected argument 'userprincipalname' to be a str")
        pulumi.set(__self__, "userprincipalname", userprincipalname)

    @property
    @pulumi.getter(name="activatedAt")
    def activated_at(self) -> str:
        return pulumi.get(self, "activated_at")

    @property
    @pulumi.getter
    def comment(self) -> str:
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def company(self) -> str:
        return pulumi.get(self, "company")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def department(self) -> str:
        return pulumi.get(self, "department")

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> int:
        return pulumi.get(self, "directory_id")

    @property
    @pulumi.getter(name="distinguishedName")
    def distinguished_name(self) -> str:
        return pulumi.get(self, "distinguished_name")

    @property
    @pulumi.getter
    def email(self) -> str:
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> str:
        return pulumi.get(self, "external_id")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetUsersFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def firstname(self) -> str:
        return pulumi.get(self, "firstname")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> int:
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="invalidLoginAttempts")
    def invalid_login_attempts(self) -> int:
        return pulumi.get(self, "invalid_login_attempts")

    @property
    @pulumi.getter(name="invitationSentAt")
    def invitation_sent_at(self) -> str:
        return pulumi.get(self, "invitation_sent_at")

    @property
    @pulumi.getter(name="lastLogin")
    def last_login(self) -> str:
        return pulumi.get(self, "last_login")

    @property
    @pulumi.getter
    def lastname(self) -> str:
        return pulumi.get(self, "lastname")

    @property
    @pulumi.getter(name="lockedUntil")
    def locked_until(self) -> str:
        return pulumi.get(self, "locked_until")

    @property
    @pulumi.getter(name="managerAdId")
    def manager_ad_id(self) -> str:
        return pulumi.get(self, "manager_ad_id")

    @property
    @pulumi.getter(name="managerUserId")
    def manager_user_id(self) -> str:
        return pulumi.get(self, "manager_user_id")

    @property
    @pulumi.getter(name="memberOf")
    def member_of(self) -> str:
        return pulumi.get(self, "member_of")

    @property
    @pulumi.getter
    def password(self) -> str:
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="passwordAlgorithm")
    def password_algorithm(self) -> str:
        return pulumi.get(self, "password_algorithm")

    @property
    @pulumi.getter(name="passwordChangedAt")
    def password_changed_at(self) -> str:
        return pulumi.get(self, "password_changed_at")

    @property
    @pulumi.getter(name="passwordConfirmation")
    def password_confirmation(self) -> str:
        return pulumi.get(self, "password_confirmation")

    @property
    @pulumi.getter
    def phone(self) -> str:
        return pulumi.get(self, "phone")

    @property
    @pulumi.getter(name="preferredLocaleCode")
    def preferred_locale_code(self) -> str:
        return pulumi.get(self, "preferred_locale_code")

    @property
    @pulumi.getter(name="roleIds")
    def role_ids(self) -> Sequence[int]:
        return pulumi.get(self, "role_ids")

    @property
    @pulumi.getter
    def salt(self) -> str:
        return pulumi.get(self, "salt")

    @property
    @pulumi.getter
    def samaccountname(self) -> str:
        return pulumi.get(self, "samaccountname")

    @property
    @pulumi.getter
    def state(self) -> int:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def status(self) -> int:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter(name="trustedIdpId")
    def trusted_idp_id(self) -> int:
        return pulumi.get(self, "trusted_idp_id")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter
    def username(self) -> str:
        return pulumi.get(self, "username")

    @property
    @pulumi.getter
    def userprincipalname(self) -> str:
        return pulumi.get(self, "userprincipalname")


class AwaitableGetUsersResult(GetUsersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUsersResult(
            activated_at=self.activated_at,
            comment=self.comment,
            company=self.company,
            created_at=self.created_at,
            department=self.department,
            directory_id=self.directory_id,
            distinguished_name=self.distinguished_name,
            email=self.email,
            external_id=self.external_id,
            filters=self.filters,
            firstname=self.firstname,
            group_id=self.group_id,
            id=self.id,
            invalid_login_attempts=self.invalid_login_attempts,
            invitation_sent_at=self.invitation_sent_at,
            last_login=self.last_login,
            lastname=self.lastname,
            locked_until=self.locked_until,
            manager_ad_id=self.manager_ad_id,
            manager_user_id=self.manager_user_id,
            member_of=self.member_of,
            password=self.password,
            password_algorithm=self.password_algorithm,
            password_changed_at=self.password_changed_at,
            password_confirmation=self.password_confirmation,
            phone=self.phone,
            preferred_locale_code=self.preferred_locale_code,
            role_ids=self.role_ids,
            salt=self.salt,
            samaccountname=self.samaccountname,
            state=self.state,
            status=self.status,
            title=self.title,
            trusted_idp_id=self.trusted_idp_id,
            updated_at=self.updated_at,
            username=self.username,
            userprincipalname=self.userprincipalname)


def get_users(activated_at: Optional[str] = None,
              comment: Optional[str] = None,
              company: Optional[str] = None,
              created_at: Optional[str] = None,
              department: Optional[str] = None,
              directory_id: Optional[int] = None,
              distinguished_name: Optional[str] = None,
              email: Optional[str] = None,
              external_id: Optional[str] = None,
              filters: Optional[Sequence[pulumi.InputType['GetUsersFilterArgs']]] = None,
              firstname: Optional[str] = None,
              group_id: Optional[int] = None,
              invalid_login_attempts: Optional[int] = None,
              invitation_sent_at: Optional[str] = None,
              last_login: Optional[str] = None,
              lastname: Optional[str] = None,
              locked_until: Optional[str] = None,
              manager_ad_id: Optional[str] = None,
              manager_user_id: Optional[str] = None,
              member_of: Optional[str] = None,
              password: Optional[str] = None,
              password_algorithm: Optional[str] = None,
              password_changed_at: Optional[str] = None,
              password_confirmation: Optional[str] = None,
              phone: Optional[str] = None,
              preferred_locale_code: Optional[str] = None,
              role_ids: Optional[Sequence[int]] = None,
              salt: Optional[str] = None,
              samaccountname: Optional[str] = None,
              state: Optional[int] = None,
              status: Optional[int] = None,
              title: Optional[str] = None,
              trusted_idp_id: Optional[int] = None,
              updated_at: Optional[str] = None,
              username: Optional[str] = None,
              userprincipalname: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUsersResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['activatedAt'] = activated_at
    __args__['comment'] = comment
    __args__['company'] = company
    __args__['createdAt'] = created_at
    __args__['department'] = department
    __args__['directoryId'] = directory_id
    __args__['distinguishedName'] = distinguished_name
    __args__['email'] = email
    __args__['externalId'] = external_id
    __args__['filters'] = filters
    __args__['firstname'] = firstname
    __args__['groupId'] = group_id
    __args__['invalidLoginAttempts'] = invalid_login_attempts
    __args__['invitationSentAt'] = invitation_sent_at
    __args__['lastLogin'] = last_login
    __args__['lastname'] = lastname
    __args__['lockedUntil'] = locked_until
    __args__['managerAdId'] = manager_ad_id
    __args__['managerUserId'] = manager_user_id
    __args__['memberOf'] = member_of
    __args__['password'] = password
    __args__['passwordAlgorithm'] = password_algorithm
    __args__['passwordChangedAt'] = password_changed_at
    __args__['passwordConfirmation'] = password_confirmation
    __args__['phone'] = phone
    __args__['preferredLocaleCode'] = preferred_locale_code
    __args__['roleIds'] = role_ids
    __args__['salt'] = salt
    __args__['samaccountname'] = samaccountname
    __args__['state'] = state
    __args__['status'] = status
    __args__['title'] = title
    __args__['trustedIdpId'] = trusted_idp_id
    __args__['updatedAt'] = updated_at
    __args__['username'] = username
    __args__['userprincipalname'] = userprincipalname
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('onelogin:users/getUsers:getUsers', __args__, opts=opts, typ=GetUsersResult).value

    return AwaitableGetUsersResult(
        activated_at=pulumi.get(__ret__, 'activated_at'),
        comment=pulumi.get(__ret__, 'comment'),
        company=pulumi.get(__ret__, 'company'),
        created_at=pulumi.get(__ret__, 'created_at'),
        department=pulumi.get(__ret__, 'department'),
        directory_id=pulumi.get(__ret__, 'directory_id'),
        distinguished_name=pulumi.get(__ret__, 'distinguished_name'),
        email=pulumi.get(__ret__, 'email'),
        external_id=pulumi.get(__ret__, 'external_id'),
        filters=pulumi.get(__ret__, 'filters'),
        firstname=pulumi.get(__ret__, 'firstname'),
        group_id=pulumi.get(__ret__, 'group_id'),
        id=pulumi.get(__ret__, 'id'),
        invalid_login_attempts=pulumi.get(__ret__, 'invalid_login_attempts'),
        invitation_sent_at=pulumi.get(__ret__, 'invitation_sent_at'),
        last_login=pulumi.get(__ret__, 'last_login'),
        lastname=pulumi.get(__ret__, 'lastname'),
        locked_until=pulumi.get(__ret__, 'locked_until'),
        manager_ad_id=pulumi.get(__ret__, 'manager_ad_id'),
        manager_user_id=pulumi.get(__ret__, 'manager_user_id'),
        member_of=pulumi.get(__ret__, 'member_of'),
        password=pulumi.get(__ret__, 'password'),
        password_algorithm=pulumi.get(__ret__, 'password_algorithm'),
        password_changed_at=pulumi.get(__ret__, 'password_changed_at'),
        password_confirmation=pulumi.get(__ret__, 'password_confirmation'),
        phone=pulumi.get(__ret__, 'phone'),
        preferred_locale_code=pulumi.get(__ret__, 'preferred_locale_code'),
        role_ids=pulumi.get(__ret__, 'role_ids'),
        salt=pulumi.get(__ret__, 'salt'),
        samaccountname=pulumi.get(__ret__, 'samaccountname'),
        state=pulumi.get(__ret__, 'state'),
        status=pulumi.get(__ret__, 'status'),
        title=pulumi.get(__ret__, 'title'),
        trusted_idp_id=pulumi.get(__ret__, 'trusted_idp_id'),
        updated_at=pulumi.get(__ret__, 'updated_at'),
        username=pulumi.get(__ret__, 'username'),
        userprincipalname=pulumi.get(__ret__, 'userprincipalname'))


@_utilities.lift_output_func(get_users)
def get_users_output(activated_at: Optional[pulumi.Input[Optional[str]]] = None,
                     comment: Optional[pulumi.Input[Optional[str]]] = None,
                     company: Optional[pulumi.Input[Optional[str]]] = None,
                     created_at: Optional[pulumi.Input[Optional[str]]] = None,
                     department: Optional[pulumi.Input[Optional[str]]] = None,
                     directory_id: Optional[pulumi.Input[Optional[int]]] = None,
                     distinguished_name: Optional[pulumi.Input[Optional[str]]] = None,
                     email: Optional[pulumi.Input[Optional[str]]] = None,
                     external_id: Optional[pulumi.Input[Optional[str]]] = None,
                     filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetUsersFilterArgs']]]]] = None,
                     firstname: Optional[pulumi.Input[Optional[str]]] = None,
                     group_id: Optional[pulumi.Input[Optional[int]]] = None,
                     invalid_login_attempts: Optional[pulumi.Input[Optional[int]]] = None,
                     invitation_sent_at: Optional[pulumi.Input[Optional[str]]] = None,
                     last_login: Optional[pulumi.Input[Optional[str]]] = None,
                     lastname: Optional[pulumi.Input[Optional[str]]] = None,
                     locked_until: Optional[pulumi.Input[Optional[str]]] = None,
                     manager_ad_id: Optional[pulumi.Input[Optional[str]]] = None,
                     manager_user_id: Optional[pulumi.Input[Optional[str]]] = None,
                     member_of: Optional[pulumi.Input[Optional[str]]] = None,
                     password: Optional[pulumi.Input[Optional[str]]] = None,
                     password_algorithm: Optional[pulumi.Input[Optional[str]]] = None,
                     password_changed_at: Optional[pulumi.Input[Optional[str]]] = None,
                     password_confirmation: Optional[pulumi.Input[Optional[str]]] = None,
                     phone: Optional[pulumi.Input[Optional[str]]] = None,
                     preferred_locale_code: Optional[pulumi.Input[Optional[str]]] = None,
                     role_ids: Optional[pulumi.Input[Optional[Sequence[int]]]] = None,
                     salt: Optional[pulumi.Input[Optional[str]]] = None,
                     samaccountname: Optional[pulumi.Input[Optional[str]]] = None,
                     state: Optional[pulumi.Input[Optional[int]]] = None,
                     status: Optional[pulumi.Input[Optional[int]]] = None,
                     title: Optional[pulumi.Input[Optional[str]]] = None,
                     trusted_idp_id: Optional[pulumi.Input[Optional[int]]] = None,
                     updated_at: Optional[pulumi.Input[Optional[str]]] = None,
                     username: Optional[pulumi.Input[Optional[str]]] = None,
                     userprincipalname: Optional[pulumi.Input[Optional[str]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUsersResult]:
    """
    Use this data source to access information about an existing resource.
    """
    ...
