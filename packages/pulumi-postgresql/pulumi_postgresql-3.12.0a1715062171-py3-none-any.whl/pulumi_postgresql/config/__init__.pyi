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

awsRdsIamAuth: Optional[bool]
"""
Use rds_iam instead of password authentication (see:
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
"""

awsRdsIamProfile: Optional[str]
"""
AWS profile to use for IAM auth
"""

awsRdsIamRegion: Optional[str]
"""
AWS region to use for IAM auth
"""

azureIdentityAuth: Optional[bool]
"""
Use MS Azure identity OAuth token (see:
https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication)
"""

azureTenantId: Optional[str]

clientcert: Optional[str]
"""
SSL client certificate if required by the database.
"""

connectTimeout: int
"""
Maximum wait for connection, in seconds. Zero or not specified means wait indefinitely.
"""

database: Optional[str]
"""
The name of the database to connect to in order to conenct to (defaults to `postgres`).
"""

databaseUsername: Optional[str]
"""
Database username associated to the connected user (for user name maps)
"""

expectedVersion: Optional[str]
"""
Specify the expected version of PostgreSQL.
"""

host: Optional[str]
"""
Name of PostgreSQL server address to connect to
"""

maxConnections: Optional[int]
"""
Maximum number of connections to establish to the database. Zero means unlimited.
"""

password: Optional[str]
"""
Password to be used if the PostgreSQL server demands password authentication
"""

port: Optional[int]
"""
The PostgreSQL port number to connect to at the server host, or socket file name extension for Unix-domain connections
"""

scheme: Optional[str]

sslMode: Optional[str]

sslmode: Optional[str]
"""
This option determines whether or with what priority a secure SSL TCP/IP connection will be negotiated with the
PostgreSQL server
"""

sslrootcert: Optional[str]
"""
The SSL server root certificate file path. The file must contain PEM encoded data.
"""

superuser: Optional[bool]
"""
Specify if the user to connect as is a Postgres superuser or not.If not, some feature might be disabled (e.g.:
Refreshing state password from Postgres)
"""

username: Optional[str]
"""
PostgreSQL user name to connect as
"""

