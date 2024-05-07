# Generated by ariadne-codegen
# Source: ../shared/schema.gql

from enum import Enum


class AuthRole(str, Enum):
    AUTHENTICATED = "AUTHENTICATED"
    ADMIN = "ADMIN"
    USER = "USER"


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class ToolHashType(str, Enum):
    public = "public"
    shared = "shared"
