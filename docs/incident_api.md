Create an incident
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents

Overview
Create an incident. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Request
Body Data (required)
Incident payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident data for a create request.

attributes [required]

object

The incident's attributes for a create request.

customer_impact_scope

string

Required if customer_impacted:"true". A summary of the impact customers experienced during the incident.

customer_impacted [required]

boolean

A flag indicating whether the incident caused customer impact.

fields

object

A condensed view of the user-defined fields for which to create initial selections.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

type

enum

Type of the single value field definitions. Allowed enum values: dropdown,textbox

default: dropdown

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

type

enum

Type of the multiple value field definitions. Allowed enum values: multiselect,textarray,metrictag,autocomplete

default: multiselect

value

[string]

The multiple values selected for this field.

incident_type_uuid

string

A unique identifier that represents an incident type. The default incident type will be used if this property is not provided.

initial_cells

[ <oneOf>]

An array of initial timeline cells to be placed at the beginning of the incident timeline.

Option 1

object

Timeline cell data for Markdown timeline cells for a create request.

cell_type [required]

enum

Type of the Markdown timeline cell. Allowed enum values: markdown

default: markdown

content [required]

object

The Markdown timeline cell contents.

content

string

The Markdown content of the cell.

important

boolean

A flag indicating whether the timeline cell is important and should be highlighted.

is_test

boolean

A flag indicating whether the incident is a test incident.

notification_handles

[object]

Notification handles that will be notified of the incident at creation.

display_name

string

The name of the notified handle.

handle

string

The handle used for the notification. This includes an email address, Slack channel, or workflow.

title [required]

string

The title of the incident, which summarizes what happened.

relationships

object

The relationships the incident will have with other resources once created.

commander_user [required]

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

Response
201
400
401
403
404
429
CREATED

Model
Example
Response with an incident.

Collapse All
Field

Type

Description

data [required]

object

Incident data from a response.

attributes

object

The incident's attributes from a response.

archived

date-time

Timestamp of when the incident was archived.

case_id

int64

The incident case id.

created

date-time

Timestamp when the incident was created.

customer_impact_duration

int64

Length of the incident's customer impact in seconds. Equals the difference between customer_impact_start and customer_impact_end.

customer_impact_end

date-time

Timestamp when customers were no longer impacted by the incident.

customer_impact_scope

string

A summary of the impact customers experienced during the incident.

customer_impact_start

date-time

Timestamp when customers began being impacted by the incident.

customer_impacted

boolean

A flag indicating whether the incident caused customer impact.

declared

date-time

Timestamp when the incident was declared.

declared_by

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

declared_by_uuid

string

UUID of the user who declared the incident.

detected

date-time

Timestamp when the incident was detected.

fields

object

A condensed view of the user-defined fields attached to incidents.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

type

enum

Type of the single value field definitions. Allowed enum values: dropdown,textbox

default: dropdown

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

type

enum

Type of the multiple value field definitions. Allowed enum values: multiselect,textarray,metrictag,autocomplete

default: multiselect

value

[string]

The multiple values selected for this field.

incident_type_uuid

string

A unique identifier that represents an incident type.

is_test

boolean

A flag indicating whether the incident is a test incident.

modified

date-time

Timestamp when the incident was last modified.

non_datadog_creator

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

notification_handles

[object]

Notification handles that will be notified of the incident during update.

display_name

string

The name of the notified handle.

handle

string

The handle used for the notification. This includes an email address, Slack channel, or workflow.

public_id

int64

The monotonically increasing integer ID for the incident.

resolved

date-time

Timestamp when the incident's state was last changed from active or stable to resolved or completed.

severity

enum

The incident severity. Allowed enum values: UNKNOWN,SEV-0,SEV-1,SEV-2,SEV-3,SEV-4,SEV-5

state

string

The state incident.

time_to_detect

int64

The amount of time in seconds to detect the incident. Equals the difference between customer_impact_start and detected.

time_to_internal_response

int64

The amount of time in seconds to call incident after detection. Equals the difference of detected and created.

time_to_repair

int64

The amount of time in seconds to resolve customer impact after detecting the issue. Equals the difference between customer_impact_end and detected.

time_to_resolve

int64

The amount of time in seconds to resolve the incident after it was created. Equals the difference between created and resolved.

title [required]

string

The title of the incident, which summarizes what happened.

visibility

string

The incident visibility status.

id [required]

string

The incident's ID.

relationships

object

The incident's relationships from a response.

attachments

object

A relationship reference for attachments.

data [required]

[object]

An array of incident attachments.

id [required]

string

A unique identifier that represents the attachment.

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

commander_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

declared_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

impacts

object

Relationship to impacts.

data [required]

[object]

An array of incident impacts.

id [required]

string

A unique identifier that represents the impact.

type [required]

enum

The incident impacts type. Allowed enum values: incident_impacts

integrations

object

A relationship reference for multiple integration metadata objects.

data [required]

[object]

Integration metadata relationship array

id [required]

string

A unique identifier that represents the integration metadata.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

responders

object

Relationship to incident responders.

data [required]

[object]

An array of incident responders.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident responders type. Allowed enum values: incident_responders

user_defined_fields

object

Relationship to incident user defined fields.

data [required]

[object]

An array of user defined fields.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident user defined fields type. Allowed enum values: user_defined_field

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Attachment data from a response.

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Create an incident returns "CREATED" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_create_attributes import IncidentCreateAttributes
from datadog_api_client.v2.model.incident_create_data import IncidentCreateData
from datadog_api_client.v2.model.incident_create_relationships import IncidentCreateRelationships
from datadog_api_client.v2.model.incident_create_request import IncidentCreateRequest
from datadog_api_client.v2.model.incident_field_attributes_single_value import IncidentFieldAttributesSingleValue
from datadog_api_client.v2.model.incident_field_attributes_single_value_type import (
    IncidentFieldAttributesSingleValueType,
)
from datadog_api_client.v2.model.incident_type import IncidentType
from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser
from datadog_api_client.v2.model.nullable_relationship_to_user_data import NullableRelationshipToUserData
from datadog_api_client.v2.model.users_type import UsersType

# there is a valid "user" in the system
USER_DATA_ID = environ["USER_DATA_ID"]

body = IncidentCreateRequest(
    data=IncidentCreateData(
        type=IncidentType.INCIDENTS,
        attributes=IncidentCreateAttributes(
            title="Example-Incident",
            customer_impacted=False,
            fields=dict(
                state=IncidentFieldAttributesSingleValue(
                    type=IncidentFieldAttributesSingleValueType.DROPDOWN,
                    value="resolved",
                ),
            ),
        ),
        relationships=IncidentCreateRelationships(
            commander_user=NullableRelationshipToUser(
                data=NullableRelationshipToUserData(
                    type=UsersType.USERS,
                    id=USER_DATA_ID,
                ),
            ),
        ),
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident(body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get the details of an incident
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/{incident_id}

Overview
Get the details of an incident by incident_id. This endpoint requires the incident_read permission.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Query Strings
Name

Type

Description

include

array

Specifies which types of related objects should be included in the response.

Response
200
400
401
403
404
429
OK

Model
Example
Response with an incident.

Collapse All
Field

Type

Description

data [required]

object

Incident data from a response.

attributes

object

The incident's attributes from a response.

archived

date-time

Timestamp of when the incident was archived.

case_id

int64

The incident case id.

created

date-time

Timestamp when the incident was created.

customer_impact_duration

int64

Length of the incident's customer impact in seconds. Equals the difference between customer_impact_start and customer_impact_end.

customer_impact_end

date-time

Timestamp when customers were no longer impacted by the incident.

customer_impact_scope

string

A summary of the impact customers experienced during the incident.

customer_impact_start

date-time

Timestamp when customers began being impacted by the incident.

customer_impacted

boolean

A flag indicating whether the incident caused customer impact.

declared

date-time

Timestamp when the incident was declared.

declared_by

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

declared_by_uuid

string

UUID of the user who declared the incident.

detected

date-time

Timestamp when the incident was detected.

fields

object

A condensed view of the user-defined fields attached to incidents.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

type

enum

Type of the single value field definitions. Allowed enum values: dropdown,textbox

default: dropdown

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

type

enum

Type of the multiple value field definitions. Allowed enum values: multiselect,textarray,metrictag,autocomplete

default: multiselect

value

[string]

The multiple values selected for this field.

incident_type_uuid

string

A unique identifier that represents an incident type.

is_test

boolean

A flag indicating whether the incident is a test incident.

modified

date-time

Timestamp when the incident was last modified.

non_datadog_creator

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

notification_handles

[object]

Notification handles that will be notified of the incident during update.

display_name

string

The name of the notified handle.

handle

string

The handle used for the notification. This includes an email address, Slack channel, or workflow.

public_id

int64

The monotonically increasing integer ID for the incident.

resolved

date-time

Timestamp when the incident's state was last changed from active or stable to resolved or completed.

severity

enum

The incident severity. Allowed enum values: UNKNOWN,SEV-0,SEV-1,SEV-2,SEV-3,SEV-4,SEV-5

state

string

The state incident.

time_to_detect

int64

The amount of time in seconds to detect the incident. Equals the difference between customer_impact_start and detected.

time_to_internal_response

int64

The amount of time in seconds to call incident after detection. Equals the difference of detected and created.

time_to_repair

int64

The amount of time in seconds to resolve customer impact after detecting the issue. Equals the difference between customer_impact_end and detected.

time_to_resolve

int64

The amount of time in seconds to resolve the incident after it was created. Equals the difference between created and resolved.

title [required]

string

The title of the incident, which summarizes what happened.

visibility

string

The incident visibility status.

id [required]

string

The incident's ID.

relationships

object

The incident's relationships from a response.

attachments

object

A relationship reference for attachments.

data [required]

[object]

An array of incident attachments.

id [required]

string

A unique identifier that represents the attachment.

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

commander_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

declared_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

impacts

object

Relationship to impacts.

data [required]

[object]

An array of incident impacts.

id [required]

string

A unique identifier that represents the impact.

type [required]

enum

The incident impacts type. Allowed enum values: incident_impacts

integrations

object

A relationship reference for multiple integration metadata objects.

data [required]

[object]

Integration metadata relationship array

id [required]

string

A unique identifier that represents the integration metadata.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

responders

object

Relationship to incident responders.

data [required]

[object]

An array of incident responders.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident responders type. Allowed enum values: incident_responders

user_defined_fields

object

Relationship to incident user defined fields.

data [required]

[object]

An array of user defined fields.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident user defined fields type. Allowed enum values: user_defined_field

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Attachment data from a response.

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get the details of an incident returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["get_incident"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.get_incident(
        incident_id=INCIDENT_DATA_ID,
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Update an existing incident
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

PATCH https://api.datadoghq.com/api/v2/incidents/{incident_id}

Overview
Updates an incident. Provide only the attributes that should be updated as this request is a partial update. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Query Strings
Name

Type

Description

include

array

Specifies which types of related objects should be included in the response.

Request
Body Data (required)
Incident Payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident data for an update request.

attributes

object

The incident's attributes for an update request.

customer_impact_end

date-time

Timestamp when customers were no longer impacted by the incident.

customer_impact_scope

string

A summary of the impact customers experienced during the incident.

customer_impact_start

date-time

Timestamp when customers began being impacted by the incident.

customer_impacted

boolean

A flag indicating whether the incident caused customer impact.

detected

date-time

Timestamp when the incident was detected.

fields

object

A condensed view of the user-defined fields for which to update selections.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

type

enum

Type of the single value field definitions. Allowed enum values: dropdown,textbox

default: dropdown

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

type

enum

Type of the multiple value field definitions. Allowed enum values: multiselect,textarray,metrictag,autocomplete

default: multiselect

value

[string]

The multiple values selected for this field.

notification_handles

[object]

Notification handles that will be notified of the incident during update.

display_name

string

The name of the notified handle.

handle

string

The handle used for the notification. This includes an email address, Slack channel, or workflow.

title

string

The title of the incident, which summarizes what happened.

id [required]

string

The incident's ID.

relationships

object

The incident's relationships for an update request.

commander_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

integrations

object

A relationship reference for multiple integration metadata objects.

data [required]

[object]

Integration metadata relationship array

id [required]

string

A unique identifier that represents the integration metadata.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

postmortem

object

A relationship reference for postmortems.

data [required]

object

The postmortem relationship data.

id [required]

string

A unique identifier that represents the postmortem.

type [required]

enum

Incident postmortem resource type. Allowed enum values: incident_postmortems

default: incident_postmortems

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

Response
200
400
401
403
404
429
OK

Model
Example
Response with an incident.

Collapse All
Field

Type

Description

data [required]

object

Incident data from a response.

attributes

object

The incident's attributes from a response.

archived

date-time

Timestamp of when the incident was archived.

case_id

int64

The incident case id.

created

date-time

Timestamp when the incident was created.

customer_impact_duration

int64

Length of the incident's customer impact in seconds. Equals the difference between customer_impact_start and customer_impact_end.

customer_impact_end

date-time

Timestamp when customers were no longer impacted by the incident.

customer_impact_scope

string

A summary of the impact customers experienced during the incident.

customer_impact_start

date-time

Timestamp when customers began being impacted by the incident.

customer_impacted

boolean

A flag indicating whether the incident caused customer impact.

declared

date-time

Timestamp when the incident was declared.

declared_by

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

declared_by_uuid

string

UUID of the user who declared the incident.

detected

date-time

Timestamp when the incident was detected.

fields

object

A condensed view of the user-defined fields attached to incidents.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

type

enum

Type of the single value field definitions. Allowed enum values: dropdown,textbox

default: dropdown

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

type

enum

Type of the multiple value field definitions. Allowed enum values: multiselect,textarray,metrictag,autocomplete

default: multiselect

value

[string]

The multiple values selected for this field.

incident_type_uuid

string

A unique identifier that represents an incident type.

is_test

boolean

A flag indicating whether the incident is a test incident.

modified

date-time

Timestamp when the incident was last modified.

non_datadog_creator

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

notification_handles

[object]

Notification handles that will be notified of the incident during update.

display_name

string

The name of the notified handle.

handle

string

The handle used for the notification. This includes an email address, Slack channel, or workflow.

public_id

int64

The monotonically increasing integer ID for the incident.

resolved

date-time

Timestamp when the incident's state was last changed from active or stable to resolved or completed.

severity

enum

The incident severity. Allowed enum values: UNKNOWN,SEV-0,SEV-1,SEV-2,SEV-3,SEV-4,SEV-5

state

string

The state incident.

time_to_detect

int64

The amount of time in seconds to detect the incident. Equals the difference between customer_impact_start and detected.

time_to_internal_response

int64

The amount of time in seconds to call incident after detection. Equals the difference of detected and created.

time_to_repair

int64

The amount of time in seconds to resolve customer impact after detecting the issue. Equals the difference between customer_impact_end and detected.

time_to_resolve

int64

The amount of time in seconds to resolve the incident after it was created. Equals the difference between created and resolved.

title [required]

string

The title of the incident, which summarizes what happened.

visibility

string

The incident visibility status.

id [required]

string

The incident's ID.

relationships

object

The incident's relationships from a response.

attachments

object

A relationship reference for attachments.

data [required]

[object]

An array of incident attachments.

id [required]

string

A unique identifier that represents the attachment.

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

commander_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

declared_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

impacts

object

Relationship to impacts.

data [required]

[object]

An array of incident impacts.

id [required]

string

A unique identifier that represents the impact.

type [required]

enum

The incident impacts type. Allowed enum values: incident_impacts

integrations

object

A relationship reference for multiple integration metadata objects.

data [required]

[object]

Integration metadata relationship array

id [required]

string

A unique identifier that represents the integration metadata.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

responders

object

Relationship to incident responders.

data [required]

[object]

An array of incident responders.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident responders type. Allowed enum values: incident_responders

user_defined_fields

object

Relationship to incident user defined fields.

data [required]

[object]

An array of user defined fields.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident user defined fields type. Allowed enum values: user_defined_field

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Attachment data from a response.

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Add commander to an incident returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_type import IncidentType
from datadog_api_client.v2.model.incident_update_data import IncidentUpdateData
from datadog_api_client.v2.model.incident_update_relationships import IncidentUpdateRelationships
from datadog_api_client.v2.model.incident_update_request import IncidentUpdateRequest
from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser
from datadog_api_client.v2.model.nullable_relationship_to_user_data import NullableRelationshipToUserData
from datadog_api_client.v2.model.users_type import UsersType

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# there is a valid "user" in the system
USER_DATA_ID = environ["USER_DATA_ID"]

body = IncidentUpdateRequest(
    data=IncidentUpdateData(
        id=INCIDENT_DATA_ID,
        type=IncidentType.INCIDENTS,
        relationships=IncidentUpdateRelationships(
            commander_user=NullableRelationshipToUser(
                data=NullableRelationshipToUserData(
                    id=USER_DATA_ID,
                    type=UsersType.USERS,
                ),
            ),
        ),
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_incident"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_incident(incident_id=INCIDENT_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Delete an existing incident
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/{incident_id}

Overview
Deletes an existing incident from the users organization. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Response
204
400
401
403
404
429
OK

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete an existing incident returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["delete_incident"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident(
        incident_id=INCIDENT_DATA_ID,
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Create postmortem attachment
v2 (latest)
Note: This endpoint is in public beta and it’s subject to change. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/{incident_id}/attachments/postmortems

Overview
Create a postmortem attachment for an incident.

The endpoint accepts markdown for notebooks created in Confluence or Google Docs. Postmortems created from notebooks need to be formatted using frontend notebook cells, in addition to markdown format.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The ID of the incident

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

Postmortem attachment data

attributes [required]

object

Postmortem attachment attributes

cells

[object]

The cells of the postmortem

attributes

object

Attributes of a postmortem cell

definition

object

Definition of a postmortem cell

content

string

The content of the cell in markdown format

id

string

The unique identifier of the cell

type

enum

The postmortem cell resource type. Allowed enum values: markdown

content

string

The content of the postmortem

postmortem_template_id

string

The ID of the postmortem template

title

string

The title of the postmortem

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

Response
201
400
429
Created

Model
Example
An attachment response containing the attachment data and related objects.

Collapse All
Field

Type

Description

data

object

Attachment data from a response.

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

included

[ <oneOf>]

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Create postmortem attachment returns "Created" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType
from datadog_api_client.v2.model.postmortem_attachment_request import PostmortemAttachmentRequest
from datadog_api_client.v2.model.postmortem_attachment_request_attributes import PostmortemAttachmentRequestAttributes
from datadog_api_client.v2.model.postmortem_attachment_request_data import PostmortemAttachmentRequestData
from datadog_api_client.v2.model.postmortem_cell import PostmortemCell
from datadog_api_client.v2.model.postmortem_cell_attributes import PostmortemCellAttributes
from datadog_api_client.v2.model.postmortem_cell_definition import PostmortemCellDefinition
from datadog_api_client.v2.model.postmortem_cell_type import PostmortemCellType

body = PostmortemAttachmentRequest(
    data=PostmortemAttachmentRequestData(
        attributes=PostmortemAttachmentRequestAttributes(
            cells=[
                PostmortemCell(
                    attributes=PostmortemCellAttributes(
                        definition=PostmortemCellDefinition(
                            content="## Incident Summary\nThis incident was caused by...",
                        ),
                    ),
                    id="cell-1",
                    type=PostmortemCellType.MARKDOWN,
                ),
            ],
            content="# Incident Report - IR-123\n[...]",
            postmortem_template_id="93645509-874e-45c4-adfa-623bfeaead89-123",
            title="Postmortem-IR-123",
        ),
        type=IncidentAttachmentType.INCIDENT_ATTACHMENTS,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_postmortem_attachment"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_postmortem_attachment(
        incident_id="00000000-0000-0000-0000-000000000000", body=body
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Get a list of incidents
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents

Overview
Get all incidents for the user’s organization. This endpoint requires the incident_read permission.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Query Strings
Name

Type

Description

include

array

Specifies which types of related objects should be included in the response.

page[size]

integer

Size for a given page. The maximum allowed value is 100.

page[offset]

integer

Specific offset to use as the beginning of the returned page.

Response
200
400
401
403
404
429
OK

Model
Example
Response with a list of incidents.

Collapse All
Field

Type

Description

data [required]

[object]

An array of incidents.

attributes

object

The incident's attributes from a response.

archived

date-time

Timestamp of when the incident was archived.

case_id

int64

The incident case id.

created

date-time

Timestamp when the incident was created.

customer_impact_duration

int64

Length of the incident's customer impact in seconds. Equals the difference between customer_impact_start and customer_impact_end.

customer_impact_end

date-time

Timestamp when customers were no longer impacted by the incident.

customer_impact_scope

string

A summary of the impact customers experienced during the incident.

customer_impact_start

date-time

Timestamp when customers began being impacted by the incident.

customer_impacted

boolean

A flag indicating whether the incident caused customer impact.

declared

date-time

Timestamp when the incident was declared.

declared_by

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

declared_by_uuid

string

UUID of the user who declared the incident.

detected

date-time

Timestamp when the incident was detected.

fields

object

A condensed view of the user-defined fields attached to incidents.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

type

enum

Type of the single value field definitions. Allowed enum values: dropdown,textbox

default: dropdown

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

type

enum

Type of the multiple value field definitions. Allowed enum values: multiselect,textarray,metrictag,autocomplete

default: multiselect

value

[string]

The multiple values selected for this field.

incident_type_uuid

string

A unique identifier that represents an incident type.

is_test

boolean

A flag indicating whether the incident is a test incident.

modified

date-time

Timestamp when the incident was last modified.

non_datadog_creator

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

notification_handles

[object]

Notification handles that will be notified of the incident during update.

display_name

string

The name of the notified handle.

handle

string

The handle used for the notification. This includes an email address, Slack channel, or workflow.

public_id

int64

The monotonically increasing integer ID for the incident.

resolved

date-time

Timestamp when the incident's state was last changed from active or stable to resolved or completed.

severity

enum

The incident severity. Allowed enum values: UNKNOWN,SEV-0,SEV-1,SEV-2,SEV-3,SEV-4,SEV-5

state

string

The state incident.

time_to_detect

int64

The amount of time in seconds to detect the incident. Equals the difference between customer_impact_start and detected.

time_to_internal_response

int64

The amount of time in seconds to call incident after detection. Equals the difference of detected and created.

time_to_repair

int64

The amount of time in seconds to resolve customer impact after detecting the issue. Equals the difference between customer_impact_end and detected.

time_to_resolve

int64

The amount of time in seconds to resolve the incident after it was created. Equals the difference between created and resolved.

title [required]

string

The title of the incident, which summarizes what happened.

visibility

string

The incident visibility status.

id [required]

string

The incident's ID.

relationships

object

The incident's relationships from a response.

attachments

object

A relationship reference for attachments.

data [required]

[object]

An array of incident attachments.

id [required]

string

A unique identifier that represents the attachment.

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

commander_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

declared_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

impacts

object

Relationship to impacts.

data [required]

[object]

An array of incident impacts.

id [required]

string

A unique identifier that represents the impact.

type [required]

enum

The incident impacts type. Allowed enum values: incident_impacts

integrations

object

A relationship reference for multiple integration metadata objects.

data [required]

[object]

Integration metadata relationship array

id [required]

string

A unique identifier that represents the integration metadata.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

responders

object

Relationship to incident responders.

data [required]

[object]

An array of incident responders.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident responders type. Allowed enum values: incident_responders

user_defined_fields

object

Relationship to incident user defined fields.

data [required]

[object]

An array of user defined fields.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident user defined fields type. Allowed enum values: user_defined_field

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Attachment data from a response.

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

meta

object

The metadata object containing pagination metadata.

pagination

object

Pagination properties.

next_offset

int64

The index of the first element in the next page of results. Equal to page size added to the current offset.

offset

int64

The index of the first element in the results.

size

int64

Maximum size of pages to return.

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get a list of incidents returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["list_incidents"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incidents()

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Search for incidents
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/search

Overview
Search for incidents matching a certain query. This endpoint requires the incident_read permission.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Query Strings
Name

Type

Description

include

enum

Specifies which types of related objects should be included in the response.
Allowed enum values: users, attachments

query [required]

string

Specifies which incidents should be returned. The query can contain any number of incident facets joined by ANDs, along with multiple values for each of those facets joined by ORs. For example: state:active AND severity:(SEV-2 OR SEV-1).

sort

enum

Specifies the order of returned incidents.
Allowed enum values: created, -created

page[size]

integer

Size for a given page. The maximum allowed value is 100.

page[offset]

integer

Specific offset to use as the beginning of the returned page.

Response
200
400
401
403
404
429
OK

Model
Example
Response with incidents and facets.

Collapse All
Field

Type

Description

data [required]

object

Data returned by an incident search.

attributes

object

Attributes returned by an incident search.

facets [required]

object

Facet data for incidents returned by a search query.

commander

[object]

Facet data for incident commander users.

count

int32

Count of the facet value appearing in search results.

email

string

Email of the user.

handle

string

Handle of the user.

name

string

Name of the user.

uuid

string

ID of the user.

created_by

[object]

Facet data for incident creator users.

count

int32

Count of the facet value appearing in search results.

email

string

Email of the user.

handle

string

Handle of the user.

name

string

Name of the user.

uuid

string

ID of the user.

fields

[object]

Facet data for incident property fields.

aggregates

object

Aggregate information for numeric incident data.

max

double

Maximum value of the numeric aggregates.

min

double

Minimum value of the numeric aggregates.

facets [required]

[object]

Facet data for the property field of an incident.

count

int32

Count of the facet value appearing in search results.

name

string

The facet value appearing in search results.

name [required]

string

Name of the incident property field.

impact

[object]

Facet data for incident impact attributes.

count

int32

Count of the facet value appearing in search results.

name

string

The facet value appearing in search results.

last_modified_by

[object]

Facet data for incident last modified by users.

count

int32

Count of the facet value appearing in search results.

email

string

Email of the user.

handle

string

Handle of the user.

name

string

Name of the user.

uuid

string

ID of the user.

postmortem

[object]

Facet data for incident postmortem existence.

count

int32

Count of the facet value appearing in search results.

name

string

The facet value appearing in search results.

responder

[object]

Facet data for incident responder users.

count

int32

Count of the facet value appearing in search results.

email

string

Email of the user.

handle

string

Handle of the user.

name

string

Name of the user.

uuid

string

ID of the user.

severity

[object]

Facet data for incident severity attributes.

count

int32

Count of the facet value appearing in search results.

name

string

The facet value appearing in search results.

state

[object]

Facet data for incident state attributes.

count

int32

Count of the facet value appearing in search results.

name

string

The facet value appearing in search results.

time_to_repair

[object]

Facet data for incident time to repair metrics.

aggregates [required]

object

Aggregate information for numeric incident data.

max

double

Maximum value of the numeric aggregates.

min

double

Minimum value of the numeric aggregates.

name [required]

string

Name of the incident property field.

time_to_resolve

[object]

Facet data for incident time to resolve metrics.

aggregates [required]

object

Aggregate information for numeric incident data.

max

double

Maximum value of the numeric aggregates.

min

double

Minimum value of the numeric aggregates.

name [required]

string

Name of the incident property field.

incidents [required]

[object]

Incidents returned by the search.

data [required]

object

Incident data from a response.

attributes

object

The incident's attributes from a response.

archived

date-time

Timestamp of when the incident was archived.

case_id

int64

The incident case id.

created

date-time

Timestamp when the incident was created.

customer_impact_duration

int64

Length of the incident's customer impact in seconds. Equals the difference between customer_impact_start and customer_impact_end.

customer_impact_end

date-time

Timestamp when customers were no longer impacted by the incident.

customer_impact_scope

string

A summary of the impact customers experienced during the incident.

customer_impact_start

date-time

Timestamp when customers began being impacted by the incident.

customer_impacted

boolean

A flag indicating whether the incident caused customer impact.

declared

date-time

Timestamp when the incident was declared.

declared_by

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

declared_by_uuid

string

UUID of the user who declared the incident.

detected

date-time

Timestamp when the incident was detected.

fields

object

A condensed view of the user-defined fields attached to incidents.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

type

enum

Type of the single value field definitions. Allowed enum values: dropdown,textbox

default: dropdown

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

type

enum

Type of the multiple value field definitions. Allowed enum values: multiselect,textarray,metrictag,autocomplete

default: multiselect

value

[string]

The multiple values selected for this field.

incident_type_uuid

string

A unique identifier that represents an incident type.

is_test

boolean

A flag indicating whether the incident is a test incident.

modified

date-time

Timestamp when the incident was last modified.

non_datadog_creator

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

notification_handles

[object]

Notification handles that will be notified of the incident during update.

display_name

string

The name of the notified handle.

handle

string

The handle used for the notification. This includes an email address, Slack channel, or workflow.

public_id

int64

The monotonically increasing integer ID for the incident.

resolved

date-time

Timestamp when the incident's state was last changed from active or stable to resolved or completed.

severity

enum

The incident severity. Allowed enum values: UNKNOWN,SEV-0,SEV-1,SEV-2,SEV-3,SEV-4,SEV-5

state

string

The state incident.

time_to_detect

int64

The amount of time in seconds to detect the incident. Equals the difference between customer_impact_start and detected.

time_to_internal_response

int64

The amount of time in seconds to call incident after detection. Equals the difference of detected and created.

time_to_repair

int64

The amount of time in seconds to resolve customer impact after detecting the issue. Equals the difference between customer_impact_end and detected.

time_to_resolve

int64

The amount of time in seconds to resolve the incident after it was created. Equals the difference between created and resolved.

title [required]

string

The title of the incident, which summarizes what happened.

visibility

string

The incident visibility status.

id [required]

string

The incident's ID.

relationships

object

The incident's relationships from a response.

attachments

object

A relationship reference for attachments.

data [required]

[object]

An array of incident attachments.

id [required]

string

A unique identifier that represents the attachment.

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

commander_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

declared_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

impacts

object

Relationship to impacts.

data [required]

[object]

An array of incident impacts.

id [required]

string

A unique identifier that represents the impact.

type [required]

enum

The incident impacts type. Allowed enum values: incident_impacts

integrations

object

A relationship reference for multiple integration metadata objects.

data [required]

[object]

Integration metadata relationship array

id [required]

string

A unique identifier that represents the integration metadata.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

responders

object

Relationship to incident responders.

data [required]

[object]

An array of incident responders.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident responders type. Allowed enum values: incident_responders

user_defined_fields

object

Relationship to incident user defined fields.

data [required]

[object]

An array of user defined fields.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident user defined fields type. Allowed enum values: user_defined_field

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

total [required]

int32

Number of incidents returned by the search.

type

enum

Incident search result type. Allowed enum values: incidents_search_results

default: incidents_search_results

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Attachment data from a response.

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

meta

object

The metadata object containing pagination metadata.

pagination

object

Pagination properties.

next_offset

int64

The index of the first element in the next page of results. Equal to page size added to the current offset.

offset

int64

The index of the first element in the results.

size

int64

Maximum size of pages to return.

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Search for incidents returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["search_incidents"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.search_incidents(
        query="state:(active OR stable OR resolved)",
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
List an incident's impacts
v2 (latest)
GET https://api.datadoghq.com/api/v2/incidents/{incident_id}/impacts

Overview
Get all impacts for an incident. This endpoint requires the incident_read permission.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Query Strings
Name

Type

Description

include

array

Specifies which related resources should be included in the response.

Response
200
400
401
403
404
429
OK

Model
Example
Response with a list of incident impacts.

Collapse All
Field

Type

Description

data [required]

[object]

An array of incident impacts.

attributes

object

The incident impact's attributes.

created

date-time

Timestamp when the impact was created.

description [required]

string

Description of the impact.

end_at

date-time

Timestamp when the impact ended.

fields

object

An object mapping impact field names to field values.

impact_type

string

The type of impact.

modified

date-time

Timestamp when the impact was last modified.

start_at [required]

date-time

Timestamp representing when the impact started.

id [required]

string

The incident impact's ID.

relationships

object

The incident impact's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Incident impact resource type. Allowed enum values: incident_impacts

default: incident_impacts

included

[object]

Included related resources that the user requested.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
List an incident's impacts returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["list_incident_impacts"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incident_impacts(
        incident_id=INCIDENT_DATA_ID,
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Create an incident impact
v2 (latest)
POST https://api.datadoghq.com/api/v2/incidents/{incident_id}/impacts

Overview
Create an impact for an incident. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Query Strings
Name

Type

Description

include

array

Specifies which related resources should be included in the response.

Request
Body Data (required)
Incident impact payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident impact data for a create request.

attributes [required]

object

The incident impact's attributes for a create request.

description [required]

string

Description of the impact.

end_at

date-time

Timestamp when the impact ended.

fields

object

An object mapping impact field names to field values.

start_at [required]

date-time

Timestamp when the impact started.

type [required]

enum

Incident impact resource type. Allowed enum values: incident_impacts

default: incident_impacts

Response
201
400
401
403
404
429
CREATED

Model
Example
Response with an incident impact.

Collapse All
Field

Type

Description

data [required]

object

Incident impact data from a response.

attributes

object

The incident impact's attributes.

created

date-time

Timestamp when the impact was created.

description [required]

string

Description of the impact.

end_at

date-time

Timestamp when the impact ended.

fields

object

An object mapping impact field names to field values.

impact_type

string

The type of impact.

modified

date-time

Timestamp when the impact was last modified.

start_at [required]

date-time

Timestamp representing when the impact started.

id [required]

string

The incident impact's ID.

relationships

object

The incident impact's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Incident impact resource type. Allowed enum values: incident_impacts

default: incident_impacts

included

[object]

Included related resources that the user requested.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Create an incident impact returns "CREATED" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_impact_create_attributes import IncidentImpactCreateAttributes
from datadog_api_client.v2.model.incident_impact_create_data import IncidentImpactCreateData
from datadog_api_client.v2.model.incident_impact_create_request import IncidentImpactCreateRequest
from datadog_api_client.v2.model.incident_impact_type import IncidentImpactType
from datetime import datetime
from dateutil.tz import tzutc

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

body = IncidentImpactCreateRequest(
    data=IncidentImpactCreateData(
        type=IncidentImpactType.INCIDENT_IMPACTS,
        attributes=IncidentImpactCreateAttributes(
            start_at=datetime(2025, 9, 12, 13, 50, tzinfo=tzutc()),
            end_at=datetime(2025, 9, 12, 14, 50, tzinfo=tzutc()),
            description="Outage in the us-east-1 region",
        ),
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_impact"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_impact(incident_id=INCIDENT_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Delete an incident impact
v2 (latest)
DELETE https://api.datadoghq.com/api/v2/incidents/{incident_id}/impacts/{impact_id}

Overview
Delete an incident impact. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

impact_id [required]

string

The UUID of the incident impact.

Response
204
401
403
404
429
No Content

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete an incident impact returns "No Content" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# the "incident" has an "incident_impact"
INCIDENT_IMPACT_DATA_ID = environ["INCIDENT_IMPACT_DATA_ID"]
INCIDENT_IMPACT_DATA_RELATIONSHIPS_INCIDENT_DATA_ID = environ["INCIDENT_IMPACT_DATA_RELATIONSHIPS_INCIDENT_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["delete_incident_impact"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident_impact(
        incident_id=INCIDENT_IMPACT_DATA_RELATIONSHIPS_INCIDENT_DATA_ID,
        impact_id=INCIDENT_IMPACT_DATA_ID,
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get a list of an incident's integration metadata
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/integrations

Overview
Get all integration metadata for an incident. This endpoint requires the incident_read permission.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Response
200
400
401
403
404
429
OK

Model
Example
Response with a list of incident integration metadata.

Collapse All
Field

Type

Description

data [required]

[object]

An array of incident integration metadata.

attributes

object

Incident integration metadata's attributes for a create request.

created

date-time

Timestamp when the incident todo was created.

incident_id

string

UUID of the incident this integration metadata is connected to.

integration_type [required]

int32

A number indicating the type of integration this metadata is for. 1 indicates Slack; 8 indicates Jira.

metadata [required]

 <oneOf>

Incident integration metadata's metadata attribute.

Option 1

object

Incident integration metadata for the Slack integration.

channels [required]

[object]

Array of Slack channels in this integration metadata.

channel_id [required]

string

Slack channel ID.

channel_name [required]

string

Name of the Slack channel.

redirect_url [required]

string

URL redirecting to the Slack channel.

team_id

string

Slack team ID.

Option 2

object

Incident integration metadata for the Jira integration.

issues [required]

[object]

Array of Jira issues in this integration metadata.

account [required]

string

URL of issue's Jira account.

issue_key

string

Jira issue's issue key.

issuetype_id

string

Jira issue's issue type.

project_key [required]

string

Jira issue's project keys.

redirect_url

string

URL redirecting to the Jira issue.

Option 3

object

Incident integration metadata for the Microsoft Teams integration.

teams [required]

[object]

Array of Microsoft Teams in this integration metadata.

ms_channel_id [required]

string

Microsoft Teams channel ID.

ms_channel_name [required]

string

Microsoft Teams channel name.

ms_tenant_id [required]

string

Microsoft Teams tenant ID.

redirect_url [required]

string

URL redirecting to the Microsoft Teams channel.

modified

date-time

Timestamp when the incident todo was last modified.

status

int32

A number indicating the status of this integration metadata. 0 indicates unknown; 1 indicates pending; 2 indicates complete; 3 indicates manually created; 4 indicates manually updated; 5 indicates failed.

id [required]

string

The incident integration metadata's ID.

relationships

object

The incident's integration relationships from a response.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

meta

object

The metadata object containing pagination metadata.

pagination

object

Pagination properties.

next_offset

int64

The index of the first element in the next page of results. Equal to page size added to the current offset.

offset

int64

The index of the first element in the results.

size

int64

Maximum size of pages to return.

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get a list of an incident's integration metadata returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["list_incident_integrations"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incident_integrations(
        incident_id=INCIDENT_DATA_ID,
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Create an incident integration metadata
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/integrations

Overview
Create an incident integration metadata. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Request
Body Data (required)
Incident integration metadata payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident integration metadata data for a create request.

attributes [required]

object

Incident integration metadata's attributes for a create request.

incident_id

string

UUID of the incident this integration metadata is connected to.

integration_type [required]

int32

A number indicating the type of integration this metadata is for. 1 indicates Slack; 8 indicates Jira.

metadata [required]

 <oneOf>

Incident integration metadata's metadata attribute.

Option 1

object

Incident integration metadata for the Slack integration.

channels [required]

[object]

Array of Slack channels in this integration metadata.

channel_id [required]

string

Slack channel ID.

channel_name [required]

string

Name of the Slack channel.

redirect_url [required]

string

URL redirecting to the Slack channel.

team_id

string

Slack team ID.

Option 2

object

Incident integration metadata for the Jira integration.

issues [required]

[object]

Array of Jira issues in this integration metadata.

account [required]

string

URL of issue's Jira account.

issue_key

string

Jira issue's issue key.

issuetype_id

string

Jira issue's issue type.

project_key [required]

string

Jira issue's project keys.

redirect_url

string

URL redirecting to the Jira issue.

Option 3

object

Incident integration metadata for the Microsoft Teams integration.

teams [required]

[object]

Array of Microsoft Teams in this integration metadata.

ms_channel_id [required]

string

Microsoft Teams channel ID.

ms_channel_name [required]

string

Microsoft Teams channel name.

ms_tenant_id [required]

string

Microsoft Teams tenant ID.

redirect_url [required]

string

URL redirecting to the Microsoft Teams channel.

status

int32

A number indicating the status of this integration metadata. 0 indicates unknown; 1 indicates pending; 2 indicates complete; 3 indicates manually created; 4 indicates manually updated; 5 indicates failed.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

Response
201
400
401
403
404
429
CREATED

Model
Example
Response with an incident integration metadata.

Collapse All
Field

Type

Description

data [required]

object

Incident integration metadata from a response.

attributes

object

Incident integration metadata's attributes for a create request.

created

date-time

Timestamp when the incident todo was created.

incident_id

string

UUID of the incident this integration metadata is connected to.

integration_type [required]

int32

A number indicating the type of integration this metadata is for. 1 indicates Slack; 8 indicates Jira.

metadata [required]

 <oneOf>

Incident integration metadata's metadata attribute.

Option 1

object

Incident integration metadata for the Slack integration.

channels [required]

[object]

Array of Slack channels in this integration metadata.

channel_id [required]

string

Slack channel ID.

channel_name [required]

string

Name of the Slack channel.

redirect_url [required]

string

URL redirecting to the Slack channel.

team_id

string

Slack team ID.

Option 2

object

Incident integration metadata for the Jira integration.

issues [required]

[object]

Array of Jira issues in this integration metadata.

account [required]

string

URL of issue's Jira account.

issue_key

string

Jira issue's issue key.

issuetype_id

string

Jira issue's issue type.

project_key [required]

string

Jira issue's project keys.

redirect_url

string

URL redirecting to the Jira issue.

Option 3

object

Incident integration metadata for the Microsoft Teams integration.

teams [required]

[object]

Array of Microsoft Teams in this integration metadata.

ms_channel_id [required]

string

Microsoft Teams channel ID.

ms_channel_name [required]

string

Microsoft Teams channel name.

ms_tenant_id [required]

string

Microsoft Teams tenant ID.

redirect_url [required]

string

URL redirecting to the Microsoft Teams channel.

modified

date-time

Timestamp when the incident todo was last modified.

status

int32

A number indicating the status of this integration metadata. 0 indicates unknown; 1 indicates pending; 2 indicates complete; 3 indicates manually created; 4 indicates manually updated; 5 indicates failed.

id [required]

string

The incident integration metadata's ID.

relationships

object

The incident's integration relationships from a response.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Create an incident integration metadata returns "CREATED" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_integration_metadata_attributes import IncidentIntegrationMetadataAttributes
from datadog_api_client.v2.model.incident_integration_metadata_create_data import IncidentIntegrationMetadataCreateData
from datadog_api_client.v2.model.incident_integration_metadata_create_request import (
    IncidentIntegrationMetadataCreateRequest,
)
from datadog_api_client.v2.model.incident_integration_metadata_type import IncidentIntegrationMetadataType
from datadog_api_client.v2.model.slack_integration_metadata import SlackIntegrationMetadata
from datadog_api_client.v2.model.slack_integration_metadata_channel_item import SlackIntegrationMetadataChannelItem

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

body = IncidentIntegrationMetadataCreateRequest(
    data=IncidentIntegrationMetadataCreateData(
        attributes=IncidentIntegrationMetadataAttributes(
            incident_id=INCIDENT_DATA_ID,
            integration_type=1,
            metadata=SlackIntegrationMetadata(
                channels=[
                    SlackIntegrationMetadataChannelItem(
                        channel_id="C0123456789",
                        channel_name="#new-channel",
                        team_id="T01234567",
                        redirect_url="https://slack.com/app_redirect?channel=C0123456789&team=T01234567",
                    ),
                ],
            ),
        ),
        type=IncidentIntegrationMetadataType.INCIDENT_INTEGRATIONS,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_integration"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_integration(incident_id=INCIDENT_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get incident integration metadata details
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}

Overview
Get incident integration metadata details.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

integration_metadata_id [required]

string

The UUID of the incident integration metadata.

Response
200
400
401
403
404
429
OK

Model
Example
Response with an incident integration metadata.

Collapse All
Field

Type

Description

data [required]

object

Incident integration metadata from a response.

attributes

object

Incident integration metadata's attributes for a create request.

created

date-time

Timestamp when the incident todo was created.

incident_id

string

UUID of the incident this integration metadata is connected to.

integration_type [required]

int32

A number indicating the type of integration this metadata is for. 1 indicates Slack; 8 indicates Jira.

metadata [required]

 <oneOf>

Incident integration metadata's metadata attribute.

Option 1

object

Incident integration metadata for the Slack integration.

channels [required]

[object]

Array of Slack channels in this integration metadata.

channel_id [required]

string

Slack channel ID.

channel_name [required]

string

Name of the Slack channel.

redirect_url [required]

string

URL redirecting to the Slack channel.

team_id

string

Slack team ID.

Option 2

object

Incident integration metadata for the Jira integration.

issues [required]

[object]

Array of Jira issues in this integration metadata.

account [required]

string

URL of issue's Jira account.

issue_key

string

Jira issue's issue key.

issuetype_id

string

Jira issue's issue type.

project_key [required]

string

Jira issue's project keys.

redirect_url

string

URL redirecting to the Jira issue.

Option 3

object

Incident integration metadata for the Microsoft Teams integration.

teams [required]

[object]

Array of Microsoft Teams in this integration metadata.

ms_channel_id [required]

string

Microsoft Teams channel ID.

ms_channel_name [required]

string

Microsoft Teams channel name.

ms_tenant_id [required]

string

Microsoft Teams tenant ID.

redirect_url [required]

string

URL redirecting to the Microsoft Teams channel.

modified

date-time

Timestamp when the incident todo was last modified.

status

int32

A number indicating the status of this integration metadata. 0 indicates unknown; 1 indicates pending; 2 indicates complete; 3 indicates manually created; 4 indicates manually updated; 5 indicates failed.

id [required]

string

The incident integration metadata's ID.

relationships

object

The incident's integration relationships from a response.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get incident integration metadata details returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# the "incident" has an "incident_integration_metadata"
INCIDENT_INTEGRATION_METADATA_DATA_ID = environ["INCIDENT_INTEGRATION_METADATA_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["get_incident_integration"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.get_incident_integration(
        incident_id=INCIDENT_DATA_ID,
        integration_metadata_id=INCIDENT_INTEGRATION_METADATA_DATA_ID,
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Update an existing incident integration metadata
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

PATCH https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}

Overview
Update an existing incident integration metadata.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

integration_metadata_id [required]

string

The UUID of the incident integration metadata.

Request
Body Data (required)
Incident integration metadata payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident integration metadata data for a patch request.

attributes [required]

object

Incident integration metadata's attributes for a create request.

incident_id

string

UUID of the incident this integration metadata is connected to.

integration_type [required]

int32

A number indicating the type of integration this metadata is for. 1 indicates Slack; 8 indicates Jira.

metadata [required]

 <oneOf>

Incident integration metadata's metadata attribute.

Option 1

object

Incident integration metadata for the Slack integration.

channels [required]

[object]

Array of Slack channels in this integration metadata.

channel_id [required]

string

Slack channel ID.

channel_name [required]

string

Name of the Slack channel.

redirect_url [required]

string

URL redirecting to the Slack channel.

team_id

string

Slack team ID.

Option 2

object

Incident integration metadata for the Jira integration.

issues [required]

[object]

Array of Jira issues in this integration metadata.

account [required]

string

URL of issue's Jira account.

issue_key

string

Jira issue's issue key.

issuetype_id

string

Jira issue's issue type.

project_key [required]

string

Jira issue's project keys.

redirect_url

string

URL redirecting to the Jira issue.

Option 3

object

Incident integration metadata for the Microsoft Teams integration.

teams [required]

[object]

Array of Microsoft Teams in this integration metadata.

ms_channel_id [required]

string

Microsoft Teams channel ID.

ms_channel_name [required]

string

Microsoft Teams channel name.

ms_tenant_id [required]

string

Microsoft Teams tenant ID.

redirect_url [required]

string

URL redirecting to the Microsoft Teams channel.

status

int32

A number indicating the status of this integration metadata. 0 indicates unknown; 1 indicates pending; 2 indicates complete; 3 indicates manually created; 4 indicates manually updated; 5 indicates failed.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

Response
200
400
401
403
404
429
OK

Model
Example
Response with an incident integration metadata.

Collapse All
Field

Type

Description

data [required]

object

Incident integration metadata from a response.

attributes

object

Incident integration metadata's attributes for a create request.

created

date-time

Timestamp when the incident todo was created.

incident_id

string

UUID of the incident this integration metadata is connected to.

integration_type [required]

int32

A number indicating the type of integration this metadata is for. 1 indicates Slack; 8 indicates Jira.

metadata [required]

 <oneOf>

Incident integration metadata's metadata attribute.

Option 1

object

Incident integration metadata for the Slack integration.

channels [required]

[object]

Array of Slack channels in this integration metadata.

channel_id [required]

string

Slack channel ID.

channel_name [required]

string

Name of the Slack channel.

redirect_url [required]

string

URL redirecting to the Slack channel.

team_id

string

Slack team ID.

Option 2

object

Incident integration metadata for the Jira integration.

issues [required]

[object]

Array of Jira issues in this integration metadata.

account [required]

string

URL of issue's Jira account.

issue_key

string

Jira issue's issue key.

issuetype_id

string

Jira issue's issue type.

project_key [required]

string

Jira issue's project keys.

redirect_url

string

URL redirecting to the Jira issue.

Option 3

object

Incident integration metadata for the Microsoft Teams integration.

teams [required]

[object]

Array of Microsoft Teams in this integration metadata.

ms_channel_id [required]

string

Microsoft Teams channel ID.

ms_channel_name [required]

string

Microsoft Teams channel name.

ms_tenant_id [required]

string

Microsoft Teams tenant ID.

redirect_url [required]

string

URL redirecting to the Microsoft Teams channel.

modified

date-time

Timestamp when the incident todo was last modified.

status

int32

A number indicating the status of this integration metadata. 0 indicates unknown; 1 indicates pending; 2 indicates complete; 3 indicates manually created; 4 indicates manually updated; 5 indicates failed.

id [required]

string

The incident integration metadata's ID.

relationships

object

The incident's integration relationships from a response.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Update an existing incident integration metadata returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_integration_metadata_attributes import IncidentIntegrationMetadataAttributes
from datadog_api_client.v2.model.incident_integration_metadata_patch_data import IncidentIntegrationMetadataPatchData
from datadog_api_client.v2.model.incident_integration_metadata_patch_request import (
    IncidentIntegrationMetadataPatchRequest,
)
from datadog_api_client.v2.model.incident_integration_metadata_type import IncidentIntegrationMetadataType
from datadog_api_client.v2.model.slack_integration_metadata import SlackIntegrationMetadata
from datadog_api_client.v2.model.slack_integration_metadata_channel_item import SlackIntegrationMetadataChannelItem

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# the "incident" has an "incident_integration_metadata"
INCIDENT_INTEGRATION_METADATA_DATA_ID = environ["INCIDENT_INTEGRATION_METADATA_DATA_ID"]

body = IncidentIntegrationMetadataPatchRequest(
    data=IncidentIntegrationMetadataPatchData(
        attributes=IncidentIntegrationMetadataAttributes(
            incident_id=INCIDENT_DATA_ID,
            integration_type=1,
            metadata=SlackIntegrationMetadata(
                channels=[
                    SlackIntegrationMetadataChannelItem(
                        channel_id="C0123456789",
                        channel_name="#updated-channel-name",
                        team_id="T01234567",
                        redirect_url="https://slack.com/app_redirect?channel=C0123456789&team=T01234567",
                    ),
                ],
            ),
        ),
        type=IncidentIntegrationMetadataType.INCIDENT_INTEGRATIONS,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_incident_integration"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_incident_integration(
        incident_id=INCIDENT_DATA_ID, integration_metadata_id=INCIDENT_INTEGRATION_METADATA_DATA_ID, body=body
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Delete an incident integration metadata
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}

Overview
Delete an incident integration metadata.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

integration_metadata_id [required]

string

The UUID of the incident integration metadata.

Response
204
400
401
403
404
429
OK

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete an incident integration metadata returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# the "incident" has an "incident_integration_metadata"
INCIDENT_INTEGRATION_METADATA_DATA_ID = environ["INCIDENT_INTEGRATION_METADATA_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["delete_incident_integration"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident_integration(
        incident_id=INCIDENT_DATA_ID,
        integration_metadata_id=INCIDENT_INTEGRATION_METADATA_DATA_ID,
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get a list of an incident's todos
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/todos

Overview
Get all todos for an incident. This endpoint requires the incident_read permission.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Response
200
400
401
403
404
429
OK

Model
Example
Response with a list of incident todos.

Collapse All
Field

Type

Description

data [required]

[object]

An array of incident todos.

attributes

object

Incident todo's attributes.

assignees [required]

[ <oneOf>]

Array of todo assignees.

Option 1

string

Assignee's @-handle.

Option 2

object

Anonymous assignee entity.

icon [required]

string

URL for assignee's icon.

id [required]

string

Anonymous assignee's ID.

name [required]

string

Assignee's name.

source [required]

enum

The source of the anonymous assignee. Allowed enum values: slack,microsoft_teams

default: slack

completed

string

Timestamp when the todo was completed.

content [required]

string

The follow-up task's content.

created

date-time

Timestamp when the incident todo was created.

due_date

string

Timestamp when the todo should be completed by.

incident_id

string

UUID of the incident this todo is connected to.

modified

date-time

Timestamp when the incident todo was last modified.

id [required]

string

The incident todo's ID.

relationships

object

The incident's relationships from a response.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Todo resource type. Allowed enum values: incident_todos

default: incident_todos

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

meta

object

The metadata object containing pagination metadata.

pagination

object

Pagination properties.

next_offset

int64

The index of the first element in the next page of results. Equal to page size added to the current offset.

offset

int64

The index of the first element in the results.

size

int64

Maximum size of pages to return.

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get a list of an incident's todos returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["list_incident_todos"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incident_todos(
        incident_id=INCIDENT_DATA_ID,
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Create an incident todo
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/todos

Overview
Create an incident todo. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Request
Body Data (required)
Incident todo payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident todo data for a create request.

attributes [required]

object

Incident todo's attributes.

assignees [required]

[ <oneOf>]

Array of todo assignees.

Option 1

string

Assignee's @-handle.

Option 2

object

Anonymous assignee entity.

icon [required]

string

URL for assignee's icon.

id [required]

string

Anonymous assignee's ID.

name [required]

string

Assignee's name.

source [required]

enum

The source of the anonymous assignee. Allowed enum values: slack,microsoft_teams

default: slack

completed

string

Timestamp when the todo was completed.

content [required]

string

The follow-up task's content.

due_date

string

Timestamp when the todo should be completed by.

incident_id

string

UUID of the incident this todo is connected to.

type [required]

enum

Todo resource type. Allowed enum values: incident_todos

default: incident_todos

Response
201
400
401
403
404
429
CREATED

Model
Example
Response with an incident todo.

Collapse All
Field

Type

Description

data [required]

object

Incident todo response data.

attributes

object

Incident todo's attributes.

assignees [required]

[ <oneOf>]

Array of todo assignees.

Option 1

string

Assignee's @-handle.

Option 2

object

Anonymous assignee entity.

icon [required]

string

URL for assignee's icon.

id [required]

string

Anonymous assignee's ID.

name [required]

string

Assignee's name.

source [required]

enum

The source of the anonymous assignee. Allowed enum values: slack,microsoft_teams

default: slack

completed

string

Timestamp when the todo was completed.

content [required]

string

The follow-up task's content.

created

date-time

Timestamp when the incident todo was created.

due_date

string

Timestamp when the todo should be completed by.

incident_id

string

UUID of the incident this todo is connected to.

modified

date-time

Timestamp when the incident todo was last modified.

id [required]

string

The incident todo's ID.

relationships

object

The incident's relationships from a response.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Todo resource type. Allowed enum values: incident_todos

default: incident_todos

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Create an incident todo returns "CREATED" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_todo_assignee_array import IncidentTodoAssigneeArray
from datadog_api_client.v2.model.incident_todo_attributes import IncidentTodoAttributes
from datadog_api_client.v2.model.incident_todo_create_data import IncidentTodoCreateData
from datadog_api_client.v2.model.incident_todo_create_request import IncidentTodoCreateRequest
from datadog_api_client.v2.model.incident_todo_type import IncidentTodoType

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

body = IncidentTodoCreateRequest(
    data=IncidentTodoCreateData(
        attributes=IncidentTodoAttributes(
            assignees=IncidentTodoAssigneeArray(
                [
                    "@test.user@test.com",
                ]
            ),
            content="Restore lost data.",
        ),
        type=IncidentTodoType.INCIDENT_TODOS,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_todo"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_todo(incident_id=INCIDENT_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get incident todo details
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/todos/{todo_id}

Overview
Get incident todo details. This endpoint requires the incident_read permission.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

todo_id [required]

string

The UUID of the incident todo.

Response
200
400
401
403
404
429
OK

Model
Example
Response with an incident todo.

Collapse All
Field

Type

Description

data [required]

object

Incident todo response data.

attributes

object

Incident todo's attributes.

assignees [required]

[ <oneOf>]

Array of todo assignees.

Option 1

string

Assignee's @-handle.

Option 2

object

Anonymous assignee entity.

icon [required]

string

URL for assignee's icon.

id [required]

string

Anonymous assignee's ID.

name [required]

string

Assignee's name.

source [required]

enum

The source of the anonymous assignee. Allowed enum values: slack,microsoft_teams

default: slack

completed

string

Timestamp when the todo was completed.

content [required]

string

The follow-up task's content.

created

date-time

Timestamp when the incident todo was created.

due_date

string

Timestamp when the todo should be completed by.

incident_id

string

UUID of the incident this todo is connected to.

modified

date-time

Timestamp when the incident todo was last modified.

id [required]

string

The incident todo's ID.

relationships

object

The incident's relationships from a response.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Todo resource type. Allowed enum values: incident_todos

default: incident_todos

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get incident todo details returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# the "incident" has an "incident_todo"
INCIDENT_TODO_DATA_ID = environ["INCIDENT_TODO_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["get_incident_todo"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.get_incident_todo(
        incident_id=INCIDENT_DATA_ID,
        todo_id=INCIDENT_TODO_DATA_ID,
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Update an incident todo
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

PATCH https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/todos/{todo_id}

Overview
Update an incident todo. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

todo_id [required]

string

The UUID of the incident todo.

Request
Body Data (required)
Incident todo payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident todo data for a patch request.

attributes [required]

object

Incident todo's attributes.

assignees [required]

[ <oneOf>]

Array of todo assignees.

Option 1

string

Assignee's @-handle.

Option 2

object

Anonymous assignee entity.

icon [required]

string

URL for assignee's icon.

id [required]

string

Anonymous assignee's ID.

name [required]

string

Assignee's name.

source [required]

enum

The source of the anonymous assignee. Allowed enum values: slack,microsoft_teams

default: slack

completed

string

Timestamp when the todo was completed.

content [required]

string

The follow-up task's content.

due_date

string

Timestamp when the todo should be completed by.

incident_id

string

UUID of the incident this todo is connected to.

type [required]

enum

Todo resource type. Allowed enum values: incident_todos

default: incident_todos

Response
200
400
401
403
404
429
OK

Model
Example
Response with an incident todo.

Collapse All
Field

Type

Description

data [required]

object

Incident todo response data.

attributes

object

Incident todo's attributes.

assignees [required]

[ <oneOf>]

Array of todo assignees.

Option 1

string

Assignee's @-handle.

Option 2

object

Anonymous assignee entity.

icon [required]

string

URL for assignee's icon.

id [required]

string

Anonymous assignee's ID.

name [required]

string

Assignee's name.

source [required]

enum

The source of the anonymous assignee. Allowed enum values: slack,microsoft_teams

default: slack

completed

string

Timestamp when the todo was completed.

content [required]

string

The follow-up task's content.

created

date-time

Timestamp when the incident todo was created.

due_date

string

Timestamp when the todo should be completed by.

incident_id

string

UUID of the incident this todo is connected to.

modified

date-time

Timestamp when the incident todo was last modified.

id [required]

string

The incident todo's ID.

relationships

object

The incident's relationships from a response.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Todo resource type. Allowed enum values: incident_todos

default: incident_todos

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Update an incident todo returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_todo_assignee_array import IncidentTodoAssigneeArray
from datadog_api_client.v2.model.incident_todo_attributes import IncidentTodoAttributes
from datadog_api_client.v2.model.incident_todo_patch_data import IncidentTodoPatchData
from datadog_api_client.v2.model.incident_todo_patch_request import IncidentTodoPatchRequest
from datadog_api_client.v2.model.incident_todo_type import IncidentTodoType

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# the "incident" has an "incident_todo"
INCIDENT_TODO_DATA_ID = environ["INCIDENT_TODO_DATA_ID"]

body = IncidentTodoPatchRequest(
    data=IncidentTodoPatchData(
        attributes=IncidentTodoAttributes(
            assignees=IncidentTodoAssigneeArray(
                [
                    "@test.user@test.com",
                ]
            ),
            content="Restore lost data.",
            completed="2023-03-06T22:00:00.000000+00:00",
            due_date="2023-07-10T05:00:00.000000+00:00",
        ),
        type=IncidentTodoType.INCIDENT_TODOS,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_incident_todo"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_incident_todo(incident_id=INCIDENT_DATA_ID, todo_id=INCIDENT_TODO_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Delete an incident todo
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/{incident_id}/relationships/todos/{todo_id}

Overview
Delete an incident todo. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

todo_id [required]

string

The UUID of the incident todo.

Response
204
400
401
403
404
429
OK

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete an incident todo returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# the "incident" has an "incident_todo"
INCIDENT_TODO_DATA_ID = environ["INCIDENT_TODO_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["delete_incident_todo"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident_todo(
        incident_id=INCIDENT_DATA_ID,
        todo_id=INCIDENT_TODO_DATA_ID,
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Create an incident type
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/config/types

Overview
Create an incident type. This endpoint requires the incident_settings_write permission.

OAuth apps require the incident_settings_write authorization scope to access this endpoint.

Request
Body Data (required)
Incident type payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident type data for a create request.

attributes [required]

object

Incident type's attributes.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

name [required]

string

The name of the incident type.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Response
201
400
401
403
404
429
CREATED

Model
Example
Incident type response data.

Collapse All
Field

Type

Description

data [required]

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Create an incident type returns "CREATED" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_type_attributes import IncidentTypeAttributes
from datadog_api_client.v2.model.incident_type_create_data import IncidentTypeCreateData
from datadog_api_client.v2.model.incident_type_create_request import IncidentTypeCreateRequest
from datadog_api_client.v2.model.incident_type_type import IncidentTypeType

body = IncidentTypeCreateRequest(
    data=IncidentTypeCreateData(
        attributes=IncidentTypeAttributes(
            description="Any incidents that harm (or have the potential to) the confidentiality, integrity, or availability of our data.",
            is_default=False,
            name="Security Incident",
        ),
        type=IncidentTypeType.INCIDENT_TYPES,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_type"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_type(body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get a list of incident types
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/types

Overview
Get all incident types. This endpoint requires any of the following permissions:

incident_settings_read
incident_read

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Query Strings
Name

Type

Description

include_deleted

boolean

Include deleted incident types in the response.

Response
200
400
401
403
429
OK

Model
Example
Response with a list of incident types.

Collapse All
Field

Type

Description

data [required]

[object]

An array of incident type objects.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get a list of incident types returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["list_incident_types"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incident_types()

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get incident type details
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/types/{incident_type_id}

Overview
Get incident type details. This endpoint requires the incident_read permission.

OAuth apps require the incident_read authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_type_id [required]

string

The UUID of the incident type.

Response
200
400
401
403
404
429
OK

Model
Example
Incident type response data.

Collapse All
Field

Type

Description

data [required]

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get incident type details returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["get_incident_type"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.get_incident_type(
        incident_type_id="incident_type_id",
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Update an incident type
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

PATCH https://api.datadoghq.com/api/v2/incidents/config/types/{incident_type_id}

Overview
Update an incident type. This endpoint requires the incident_settings_write permission.

OAuth apps require the incident_settings_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_type_id [required]

string

The UUID of the incident type.

Request
Body Data (required)
Incident type payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident type data for a patch request.

attributes [required]

object

Incident type's attributes for updates.

description

string

Text that describes the incident type.

is_default

boolean

When true, this incident type will be used as the default type when an incident type is not specified.

name

string

The name of the incident type.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Response
200
400
401
403
404
429
OK

Model
Example
Incident type response data.

Collapse All
Field

Type

Description

data [required]

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Update an incident type returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_type_patch_data import IncidentTypePatchData
from datadog_api_client.v2.model.incident_type_patch_request import IncidentTypePatchRequest
from datadog_api_client.v2.model.incident_type_type import IncidentTypeType
from datadog_api_client.v2.model.incident_type_update_attributes import IncidentTypeUpdateAttributes

# there is a valid "incident_type" in the system
INCIDENT_TYPE_DATA_ATTRIBUTES_NAME = environ["INCIDENT_TYPE_DATA_ATTRIBUTES_NAME"]
INCIDENT_TYPE_DATA_ID = environ["INCIDENT_TYPE_DATA_ID"]

body = IncidentTypePatchRequest(
    data=IncidentTypePatchData(
        id=INCIDENT_TYPE_DATA_ID,
        attributes=IncidentTypeUpdateAttributes(
            name="Security Incident-updated",
        ),
        type=IncidentTypeType.INCIDENT_TYPES,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_incident_type"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_incident_type(incident_type_id=INCIDENT_TYPE_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Delete an incident type
v2 (latest)
Note: This endpoint is in public beta. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/config/types/{incident_type_id}

Overview
Delete an incident type. This endpoint requires the incident_settings_write permission.

OAuth apps require the incident_settings_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_type_id [required]

string

The UUID of the incident type.

Response
204
400
401
403
404
429
OK

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete an incident type returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident_type" in the system
INCIDENT_TYPE_DATA_ID = environ["INCIDENT_TYPE_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["delete_incident_type"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident_type(
        incident_type_id=INCIDENT_TYPE_DATA_ID,
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
List incident notification templates
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/notification-templates

Overview
Lists all notification templates. Optionally filter by incident type. This endpoint requires the incident_notification_settings_read permission.

Arguments
Query Strings
Name

Type

Description

filter[incident-type]

string

Optional incident type ID filter.

include

string

Comma-separated list of relationships to include. Supported values: created_by_user, last_modified_by_user, incident_type

Response
200
400
401
403
404
429
OK

Model
Example
Response with notification templates.

Collapse All
Field

Type

Description

data [required]

[object]

The NotificationTemplateArray data.

attributes

object

The notification template's attributes.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

created [required]

date-time

Timestamp when the notification template was created.

modified [required]

date-time

Timestamp when the notification template was last modified.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

relationships

object

The notification template's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

included

[ <oneOf>]

Related objects that are included in the response.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

meta

object

Response metadata.

page

object

Pagination metadata.

total_count

int64

Total number of notification templates.

total_filtered_count

int64

Total number of notification templates matching the filter.

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
List incident notification templates returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["list_incident_notification_templates"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incident_notification_templates()

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Create incident notification template
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/config/notification-templates

Overview
Creates a new notification template. This endpoint requires the incident_notification_settings_write permission.

OAuth apps require the incident_notification_settings_write authorization scope to access this endpoint.

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

Notification template data for a create request.

attributes [required]

object

The attributes for creating a notification template.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

relationships

object

The definition of NotificationTemplateCreateDataRelationships object.

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

Response
201
400
401
403
404
429
Created

Model
Example
Response with a notification template.

Collapse All
Field

Type

Description

data [required]

object

Notification template data from a response.

attributes

object

The notification template's attributes.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

created [required]

date-time

Timestamp when the notification template was created.

modified [required]

date-time

Timestamp when the notification template was last modified.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

relationships

object

The notification template's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

included

[ <oneOf>]

Related objects that are included in the response.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Create incident notification template returns "Created" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.create_incident_notification_template_request import (
    CreateIncidentNotificationTemplateRequest,
)
from datadog_api_client.v2.model.incident_notification_template_create_attributes import (
    IncidentNotificationTemplateCreateAttributes,
)
from datadog_api_client.v2.model.incident_notification_template_create_data import (
    IncidentNotificationTemplateCreateData,
)
from datadog_api_client.v2.model.incident_notification_template_create_data_relationships import (
    IncidentNotificationTemplateCreateDataRelationships,
)
from datadog_api_client.v2.model.incident_notification_template_type import IncidentNotificationTemplateType
from datadog_api_client.v2.model.incident_type_type import IncidentTypeType
from datadog_api_client.v2.model.relationship_to_incident_type import RelationshipToIncidentType
from datadog_api_client.v2.model.relationship_to_incident_type_data import RelationshipToIncidentTypeData

# there is a valid "incident_type" in the system
INCIDENT_TYPE_DATA_ID = environ["INCIDENT_TYPE_DATA_ID"]

body = CreateIncidentNotificationTemplateRequest(
    data=IncidentNotificationTemplateCreateData(
        attributes=IncidentNotificationTemplateCreateAttributes(
            category="alert",
            content="An incident has been declared.\n\nTitle: Sample Incident Title\nSeverity: SEV-2\nAffected Services: web-service, database-service\nStatus: active\n\nPlease join the incident channel for updates.",
            name="Example-Incident",
            subject="SEV-2 Incident: Sample Incident Title",
        ),
        relationships=IncidentNotificationTemplateCreateDataRelationships(
            incident_type=RelationshipToIncidentType(
                data=RelationshipToIncidentTypeData(
                    id=INCIDENT_TYPE_DATA_ID,
                    type=IncidentTypeType.INCIDENT_TYPES,
                ),
            ),
        ),
        type=IncidentNotificationTemplateType.NOTIFICATION_TEMPLATES,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_notification_template"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_notification_template(body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get incident notification template
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/notification-templates/{id}

Overview
Retrieves a specific notification template by its ID. This endpoint requires any of the following permissions:

incident_settings_read
incident_write
incident_read

OAuth apps require the incident_read, incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

id [required]

string

The ID of the notification template.

Query Strings
Name

Type

Description

include

string

Comma-separated list of relationships to include. Supported values: created_by_user, last_modified_by_user, incident_type

Response
200
400
401
403
404
429
OK

Model
Example
Response with a notification template.

Collapse All
Field

Type

Description

data [required]

object

Notification template data from a response.

attributes

object

The notification template's attributes.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

created [required]

date-time

Timestamp when the notification template was created.

modified [required]

date-time

Timestamp when the notification template was last modified.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

relationships

object

The notification template's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

included

[ <oneOf>]

Related objects that are included in the response.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get incident notification template returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "notification_template" in the system
NOTIFICATION_TEMPLATE_DATA_ID = environ["NOTIFICATION_TEMPLATE_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["get_incident_notification_template"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.get_incident_notification_template(
        id=NOTIFICATION_TEMPLATE_DATA_ID,
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Update incident notification template
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

PATCH https://api.datadoghq.com/api/v2/incidents/config/notification-templates/{id}

Overview
Updates an existing notification template’s attributes. This endpoint requires the incident_notification_settings_write permission.

OAuth apps require the incident_notification_settings_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

id [required]

string

The ID of the notification template.

Query Strings
Name

Type

Description

include

string

Comma-separated list of relationships to include. Supported values: created_by_user, last_modified_by_user, incident_type

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

Notification template data for an update request.

attributes

object

The attributes to update on a notification template.

category

string

The category of the notification template.

content

string

The content body of the notification template.

name

string

The name of the notification template.

subject

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

Response
200
400
401
403
404
429
OK

Model
Example
Response with a notification template.

Collapse All
Field

Type

Description

data [required]

object

Notification template data from a response.

attributes

object

The notification template's attributes.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

created [required]

date-time

Timestamp when the notification template was created.

modified [required]

date-time

Timestamp when the notification template was last modified.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

relationships

object

The notification template's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

included

[ <oneOf>]

Related objects that are included in the response.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Update incident notification template returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_notification_template_type import IncidentNotificationTemplateType
from datadog_api_client.v2.model.incident_notification_template_update_attributes import (
    IncidentNotificationTemplateUpdateAttributes,
)
from datadog_api_client.v2.model.incident_notification_template_update_data import (
    IncidentNotificationTemplateUpdateData,
)
from datadog_api_client.v2.model.patch_incident_notification_template_request import (
    PatchIncidentNotificationTemplateRequest,
)

# there is a valid "notification_template" in the system
NOTIFICATION_TEMPLATE_DATA_ID = environ["NOTIFICATION_TEMPLATE_DATA_ID"]

body = PatchIncidentNotificationTemplateRequest(
    data=IncidentNotificationTemplateUpdateData(
        attributes=IncidentNotificationTemplateUpdateAttributes(
            category="update",
            content="Incident Status Update:\n\nTitle: Sample Incident Title\nNew Status: resolved\nSeverity: SEV-2\nServices: web-service, database-service\nCommander: John Doe\n\nFor more details, visit the incident page.",
            name="Example-Incident",
            subject="Incident Update: Sample Incident Title - resolved",
        ),
        id=NOTIFICATION_TEMPLATE_DATA_ID,
        type=IncidentNotificationTemplateType.NOTIFICATION_TEMPLATES,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_incident_notification_template"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_incident_notification_template(id=NOTIFICATION_TEMPLATE_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Delete a notification template
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/config/notification-templates/{id}

Overview
Deletes a notification template by its ID. This endpoint requires the incident_notification_settings_write permission.

OAuth apps require the incident_notification_settings_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

id [required]

string

The ID of the notification template.

Query Strings
Name

Type

Description

include

string

Comma-separated list of relationships to include. Supported values: created_by_user, last_modified_by_user, incident_type

Response
204
400
401
403
404
429
No Content

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete a notification template returns "No Content" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from uuid import UUID

configuration = Configuration()
configuration.unstable_operations["delete_incident_notification_template"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident_notification_template(
        id=UUID("00000000-0000-0000-0000-000000000001"),
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
List incident notification rules
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/notification-rules

Overview
Lists all notification rules for the organization. Optionally filter by incident type. This endpoint requires the incident_notification_settings_read permission.

Arguments
Query Strings
Name

Type

Description

include

string

Comma-separated list of resources to include. Supported values: created_by_user, last_modified_by_user, incident_type, notification_template

Response
200
400
401
403
404
429
OK

Model
Example
Response with notification rules.

Collapse All
Field

Type

Description

data [required]

[object]

The NotificationRuleArray data.

attributes

object

The notification rule's attributes.

conditions [required]

[object]

The conditions that trigger this notification rule.

field [required]

string

The incident field to evaluate

values [required]

[string]

The value(s) to compare against. Multiple values are ORed together.

created [required]

date-time

Timestamp when the notification rule was created.

enabled [required]

boolean

Whether the notification rule is enabled.

handles [required]

[string]

The notification handles (targets) for this rule.

modified [required]

date-time

Timestamp when the notification rule was last modified.

renotify_on

[string]

List of incident fields that trigger re-notification when changed.

trigger [required]

string

The trigger event for this notification rule.

visibility [required]

enum

The visibility of the notification rule. Allowed enum values: all,organization,private

id [required]

uuid

The unique identifier of the notification rule.

relationships

object

The notification rule's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

notification_template

object

A relationship reference to a notification template.

data [required]

object

The notification template relationship data.

id [required]

uuid

The unique identifier of the notification template.

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

type [required]

enum

Notification rules resource type. Allowed enum values: incident_notification_rules

included

[ <oneOf>]

Related objects that are included in the response.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Option 3

object

A notification template object for inclusion in other resources.

attributes

object

The notification template's attributes.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

created [required]

date-time

Timestamp when the notification template was created.

modified [required]

date-time

Timestamp when the notification template was last modified.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

relationships

object

The notification template's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

meta

object

Response metadata.

pagination

object

Pagination metadata.

next_offset

int64

The offset for the next page of results.

offset

int64

The current offset in the results.

size

int64

The number of results returned per page.

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
List incident notification rules returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["list_incident_notification_rules"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incident_notification_rules()

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Create an incident notification rule
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/config/notification-rules

Overview
Creates a new notification rule. This endpoint requires the incident_notification_settings_write permission.

OAuth apps require the incident_notification_settings_write authorization scope to access this endpoint.

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

Notification rule data for a create request.

attributes [required]

object

The attributes for creating a notification rule.

conditions [required]

[object]

The conditions that trigger this notification rule.

field [required]

string

The incident field to evaluate

values [required]

[string]

The value(s) to compare against. Multiple values are ORed together.

enabled

boolean

Whether the notification rule is enabled.

handles [required]

[string]

The notification handles (targets) for this rule.

renotify_on

[string]

List of incident fields that trigger re-notification when changed.

trigger [required]

string

The trigger event for this notification rule.

visibility

enum

The visibility of the notification rule. Allowed enum values: all,organization,private

relationships

object

The definition of NotificationRuleCreateDataRelationships object.

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

notification_template

object

A relationship reference to a notification template.

data [required]

object

The notification template relationship data.

id [required]

uuid

The unique identifier of the notification template.

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

type [required]

enum

Notification rules resource type. Allowed enum values: incident_notification_rules

Response
201
400
401
403
404
429
Created

Model
Example
Response with a notification rule.

Collapse All
Field

Type

Description

data [required]

object

Notification rule data from a response.

attributes

object

The notification rule's attributes.

conditions [required]

[object]

The conditions that trigger this notification rule.

field [required]

string

The incident field to evaluate

values [required]

[string]

The value(s) to compare against. Multiple values are ORed together.

created [required]

date-time

Timestamp when the notification rule was created.

enabled [required]

boolean

Whether the notification rule is enabled.

handles [required]

[string]

The notification handles (targets) for this rule.

modified [required]

date-time

Timestamp when the notification rule was last modified.

renotify_on

[string]

List of incident fields that trigger re-notification when changed.

trigger [required]

string

The trigger event for this notification rule.

visibility [required]

enum

The visibility of the notification rule. Allowed enum values: all,organization,private

id [required]

uuid

The unique identifier of the notification rule.

relationships

object

The notification rule's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

notification_template

object

A relationship reference to a notification template.

data [required]

object

The notification template relationship data.

id [required]

uuid

The unique identifier of the notification template.

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

type [required]

enum

Notification rules resource type. Allowed enum values: incident_notification_rules

included

[ <oneOf>]

Related objects that are included in the response.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Option 3

object

A notification template object for inclusion in other resources.

attributes

object

The notification template's attributes.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

created [required]

date-time

Timestamp when the notification template was created.

modified [required]

date-time

Timestamp when the notification template was last modified.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

relationships

object

The notification template's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Create incident notification rule returns "Created" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.create_incident_notification_rule_request import CreateIncidentNotificationRuleRequest
from datadog_api_client.v2.model.incident_notification_rule_conditions_items import (
    IncidentNotificationRuleConditionsItems,
)
from datadog_api_client.v2.model.incident_notification_rule_create_attributes import (
    IncidentNotificationRuleCreateAttributes,
)
from datadog_api_client.v2.model.incident_notification_rule_create_attributes_visibility import (
    IncidentNotificationRuleCreateAttributesVisibility,
)
from datadog_api_client.v2.model.incident_notification_rule_create_data import IncidentNotificationRuleCreateData
from datadog_api_client.v2.model.incident_notification_rule_create_data_relationships import (
    IncidentNotificationRuleCreateDataRelationships,
)
from datadog_api_client.v2.model.incident_notification_rule_type import IncidentNotificationRuleType
from datadog_api_client.v2.model.incident_type_type import IncidentTypeType
from datadog_api_client.v2.model.relationship_to_incident_type import RelationshipToIncidentType
from datadog_api_client.v2.model.relationship_to_incident_type_data import RelationshipToIncidentTypeData

# there is a valid "incident_type" in the system
INCIDENT_TYPE_DATA_ID = environ["INCIDENT_TYPE_DATA_ID"]

body = CreateIncidentNotificationRuleRequest(
    data=IncidentNotificationRuleCreateData(
        attributes=IncidentNotificationRuleCreateAttributes(
            conditions=[
                IncidentNotificationRuleConditionsItems(
                    field="severity",
                    values=[
                        "SEV-1",
                        "SEV-2",
                    ],
                ),
            ],
            handles=[
                "@test-email@company.com",
            ],
            visibility=IncidentNotificationRuleCreateAttributesVisibility.ORGANIZATION,
            trigger="incident_created_trigger",
            enabled=True,
        ),
        relationships=IncidentNotificationRuleCreateDataRelationships(
            incident_type=RelationshipToIncidentType(
                data=RelationshipToIncidentTypeData(
                    id=INCIDENT_TYPE_DATA_ID,
                    type=IncidentTypeType.INCIDENT_TYPES,
                ),
            ),
        ),
        type=IncidentNotificationRuleType.INCIDENT_NOTIFICATION_RULES,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_notification_rule"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_notification_rule(body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get an incident notification rule
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/notification-rules/{id}

Overview
Retrieves a specific notification rule by its ID. This endpoint requires the incident_notification_settings_read permission.

OAuth apps require the incident_notification_settings_read authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

id [required]

string

The ID of the notification rule.

Query Strings
Name

Type

Description

include

string

Comma-separated list of resources to include. Supported values: created_by_user, last_modified_by_user, incident_type, notification_template

Response
200
400
401
403
404
429
OK

Model
Example
Response with a notification rule.

Collapse All
Field

Type

Description

data [required]

object

Notification rule data from a response.

attributes

object

The notification rule's attributes.

conditions [required]

[object]

The conditions that trigger this notification rule.

field [required]

string

The incident field to evaluate

values [required]

[string]

The value(s) to compare against. Multiple values are ORed together.

created [required]

date-time

Timestamp when the notification rule was created.

enabled [required]

boolean

Whether the notification rule is enabled.

handles [required]

[string]

The notification handles (targets) for this rule.

modified [required]

date-time

Timestamp when the notification rule was last modified.

renotify_on

[string]

List of incident fields that trigger re-notification when changed.

trigger [required]

string

The trigger event for this notification rule.

visibility [required]

enum

The visibility of the notification rule. Allowed enum values: all,organization,private

id [required]

uuid

The unique identifier of the notification rule.

relationships

object

The notification rule's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

notification_template

object

A relationship reference to a notification template.

data [required]

object

The notification template relationship data.

id [required]

uuid

The unique identifier of the notification template.

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

type [required]

enum

Notification rules resource type. Allowed enum values: incident_notification_rules

included

[ <oneOf>]

Related objects that are included in the response.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Option 3

object

A notification template object for inclusion in other resources.

attributes

object

The notification template's attributes.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

created [required]

date-time

Timestamp when the notification template was created.

modified [required]

date-time

Timestamp when the notification template was last modified.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

relationships

object

The notification template's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get an incident notification rule returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from uuid import UUID

configuration = Configuration()
configuration.unstable_operations["get_incident_notification_rule"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.get_incident_notification_rule(
        id=UUID("00000000-0000-0000-0000-000000000001"),
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Update an incident notification rule
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

PUT https://api.datadoghq.com/api/v2/incidents/config/notification-rules/{id}

Overview
Updates an existing notification rule with a complete replacement. This endpoint requires the incident_notification_settings_write permission.

OAuth apps require the incident_notification_settings_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

id [required]

string

The ID of the notification rule.

Query Strings
Name

Type

Description

include

string

Comma-separated list of resources to include. Supported values: created_by_user, last_modified_by_user, incident_type, notification_template

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

Notification rule data for an update request.

attributes [required]

object

The attributes for creating a notification rule.

conditions [required]

[object]

The conditions that trigger this notification rule.

field [required]

string

The incident field to evaluate

values [required]

[string]

The value(s) to compare against. Multiple values are ORed together.

enabled

boolean

Whether the notification rule is enabled.

handles [required]

[string]

The notification handles (targets) for this rule.

renotify_on

[string]

List of incident fields that trigger re-notification when changed.

trigger [required]

string

The trigger event for this notification rule.

visibility

enum

The visibility of the notification rule. Allowed enum values: all,organization,private

id [required]

uuid

The unique identifier of the notification rule.

relationships

object

The definition of NotificationRuleCreateDataRelationships object.

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

notification_template

object

A relationship reference to a notification template.

data [required]

object

The notification template relationship data.

id [required]

uuid

The unique identifier of the notification template.

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

type [required]

enum

Notification rules resource type. Allowed enum values: incident_notification_rules

Response
200
400
401
403
404
429
OK

Model
Example
Response with a notification rule.

Collapse All
Field

Type

Description

data [required]

object

Notification rule data from a response.

attributes

object

The notification rule's attributes.

conditions [required]

[object]

The conditions that trigger this notification rule.

field [required]

string

The incident field to evaluate

values [required]

[string]

The value(s) to compare against. Multiple values are ORed together.

created [required]

date-time

Timestamp when the notification rule was created.

enabled [required]

boolean

Whether the notification rule is enabled.

handles [required]

[string]

The notification handles (targets) for this rule.

modified [required]

date-time

Timestamp when the notification rule was last modified.

renotify_on

[string]

List of incident fields that trigger re-notification when changed.

trigger [required]

string

The trigger event for this notification rule.

visibility [required]

enum

The visibility of the notification rule. Allowed enum values: all,organization,private

id [required]

uuid

The unique identifier of the notification rule.

relationships

object

The notification rule's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

notification_template

object

A relationship reference to a notification template.

data [required]

object

The notification template relationship data.

id [required]

uuid

The unique identifier of the notification template.

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

type [required]

enum

Notification rules resource type. Allowed enum values: incident_notification_rules

included

[ <oneOf>]

Related objects that are included in the response.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

created_at

date-time

Creation time of the user.

disabled

boolean

Whether the user is disabled.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

last_login_time

date-time

The last time the user logged in.

mfa_enabled

boolean

If user has MFA enabled.

modified_at

date-time

Time that the user was last modified.

name

string

Name of the user.

service_account

boolean

Whether the user is a service account.

status

string

Status of the user.

title

string

Title of the user.

verified

boolean

Whether the user is verified.

id

string

ID of the user.

relationships

object

Relationships of the user object returned by the API.

org

object

Relationship to an organization.

data [required]

object

Relationship to organization object.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_orgs

object

Relationship to organizations.

data [required]

[object]

Relationships to organization objects.

id [required]

string

ID of the organization.

type [required]

enum

Organizations resource type. Allowed enum values: orgs

default: orgs

other_users

object

Relationship to users.

data [required]

[object]

Relationships to user objects.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

roles

object

Relationship to roles.

data

[object]

An array containing type and the unique identifier of a role.

id

string

The unique identifier of the role.

type

enum

Roles type. Allowed enum values: roles

default: roles

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Option 3

object

A notification template object for inclusion in other resources.

attributes

object

The notification template's attributes.

category [required]

string

The category of the notification template.

content [required]

string

The content body of the notification template.

created [required]

date-time

Timestamp when the notification template was created.

modified [required]

date-time

Timestamp when the notification template was last modified.

name [required]

string

The name of the notification template.

subject [required]

string

The subject line of the notification template.

id [required]

uuid

The unique identifier of the notification template.

relationships

object

The notification template's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Notification templates resource type. Allowed enum values: notification_templates

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Update incident notification rule returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_notification_rule_conditions_items import (
    IncidentNotificationRuleConditionsItems,
)
from datadog_api_client.v2.model.incident_notification_rule_create_attributes import (
    IncidentNotificationRuleCreateAttributes,
)
from datadog_api_client.v2.model.incident_notification_rule_create_attributes_visibility import (
    IncidentNotificationRuleCreateAttributesVisibility,
)
from datadog_api_client.v2.model.incident_notification_rule_create_data_relationships import (
    IncidentNotificationRuleCreateDataRelationships,
)
from datadog_api_client.v2.model.incident_notification_rule_type import IncidentNotificationRuleType
from datadog_api_client.v2.model.incident_notification_rule_update_data import IncidentNotificationRuleUpdateData
from datadog_api_client.v2.model.incident_type_type import IncidentTypeType
from datadog_api_client.v2.model.put_incident_notification_rule_request import PutIncidentNotificationRuleRequest
from datadog_api_client.v2.model.relationship_to_incident_type import RelationshipToIncidentType
from datadog_api_client.v2.model.relationship_to_incident_type_data import RelationshipToIncidentTypeData

# there is a valid "notification_rule" in the system
NOTIFICATION_RULE_DATA_ID = environ["NOTIFICATION_RULE_DATA_ID"]

# there is a valid "incident_type" in the system
INCIDENT_TYPE_DATA_ID = environ["INCIDENT_TYPE_DATA_ID"]

body = PutIncidentNotificationRuleRequest(
    data=IncidentNotificationRuleUpdateData(
        attributes=IncidentNotificationRuleCreateAttributes(
            enabled=False,
            conditions=[
                IncidentNotificationRuleConditionsItems(
                    field="severity",
                    values=[
                        "SEV-1",
                    ],
                ),
            ],
            handles=[
                "@updated-team-email@company.com",
            ],
            visibility=IncidentNotificationRuleCreateAttributesVisibility.PRIVATE,
            trigger="incident_modified_trigger",
        ),
        relationships=IncidentNotificationRuleCreateDataRelationships(
            incident_type=RelationshipToIncidentType(
                data=RelationshipToIncidentTypeData(
                    id=INCIDENT_TYPE_DATA_ID,
                    type=IncidentTypeType.INCIDENT_TYPES,
                ),
            ),
        ),
        id=NOTIFICATION_RULE_DATA_ID,
        type=IncidentNotificationRuleType.INCIDENT_NOTIFICATION_RULES,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_incident_notification_rule"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_incident_notification_rule(id=NOTIFICATION_RULE_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Delete an incident notification rule
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/config/notification-rules/{id}

Overview
Deletes a notification rule by its ID. This endpoint requires the incident_notification_settings_write permission.

OAuth apps require the incident_notification_settings_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

id [required]

string

The ID of the notification rule.

Query Strings
Name

Type

Description

include

string

Comma-separated list of resources to include. Supported values: created_by_user, last_modified_by_user, incident_type, notification_template

Response
204
400
401
403
404
429
No Content

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete an incident notification rule returns "No Content" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from uuid import UUID

configuration = Configuration()
configuration.unstable_operations["delete_incident_notification_rule"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident_notification_rule(
        id=UUID("00000000-0000-0000-0000-000000000001"),
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
List incident attachments
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/{incident_id}/attachments

Overview
List incident attachments. This endpoint requires the incident_read permission.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Query Strings
Name

Type

Description

filter[attachment_type]

string

Filter attachments by type. Supported values are 1 (postmortem) and 2 (link).

include

string

Resource to include in the response. Supported value: last_modified_by_user.

Response
200
400
429
OK

Model
Example
A list of incident attachments.

Collapse All
Field

Type

Description

data [required]

[object]

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

included

[ <oneOf>]

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
List incident attachments returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["list_incident_attachments"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incident_attachments(
        incident_id=INCIDENT_DATA_ID,
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Create incident attachment
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/{incident_id}/attachments

Overview
Create an incident attachment. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

Query Strings
Name

Type

Description

include

string

Resource to include in the response. Supported value: last_modified_by_user.

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data

object

Attachment data for a create request.

attributes

object

The attributes for creating an attachment.

attachment

object

The attachment object for creating an attachment.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

id

string

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

Response
201
400
403
429
Created

Model
Example
An attachment response containing the attachment data and related objects.

Collapse All
Field

Type

Description

data

object

Attachment data from a response.

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

included

[ <oneOf>]

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Create incident attachment returns "Created" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.attachment_data_attributes_attachment_type import (
    AttachmentDataAttributesAttachmentType,
)
from datadog_api_client.v2.model.create_attachment_request import CreateAttachmentRequest
from datadog_api_client.v2.model.create_attachment_request_data import CreateAttachmentRequestData
from datadog_api_client.v2.model.create_attachment_request_data_attributes import CreateAttachmentRequestDataAttributes
from datadog_api_client.v2.model.create_attachment_request_data_attributes_attachment import (
    CreateAttachmentRequestDataAttributesAttachment,
)
from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

body = CreateAttachmentRequest(
    data=CreateAttachmentRequestData(
        attributes=CreateAttachmentRequestDataAttributes(
            attachment=CreateAttachmentRequestDataAttributesAttachment(
                document_url="https://app.datadoghq.com/notebook/ExampleIncident/Example-Incident",
                title="Example-Incident",
            ),
            attachment_type=AttachmentDataAttributesAttachmentType.POSTMORTEM,
        ),
        type=IncidentAttachmentType.INCIDENT_ATTACHMENTS,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_attachment"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_attachment(incident_id=INCIDENT_DATA_ID, body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Delete incident attachment
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/{incident_id}/attachments/{attachment_id}

Overview
This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

attachment_id [required]

string

The ID of the attachment.

Response
204
400
403
404
429
No Content

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete incident attachment returns "No Content" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# there is a valid "incident_attachment" in the system
INCIDENT_ATTACHMENT_DATA_ID = environ["INCIDENT_ATTACHMENT_DATA_ID"]

configuration = Configuration()
configuration.unstable_operations["delete_incident_attachment"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident_attachment(
        incident_id=INCIDENT_DATA_ID,
        attachment_id=INCIDENT_ATTACHMENT_DATA_ID,
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Update incident attachment
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

PATCH https://api.datadoghq.com/api/v2/incidents/{incident_id}/attachments/{attachment_id}

Overview
This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Path Parameters
Name

Type

Description

incident_id [required]

string

The UUID of the incident.

attachment_id [required]

string

The ID of the attachment.

Query Strings
Name

Type

Description

include

string

Resource to include in the response. Supported value: last_modified_by_user.

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data

object

Attachment data for an update request.

attributes

object

The attributes for updating an attachment.

attachment

object

The updated attachment object.

documentUrl

string

The updated URL for the attachment.

title

string

The updated title for the attachment.

id

string

The unique identifier of the attachment.

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

Response
200
400
403
404
429
OK

Model
Example
An attachment response containing the attachment data and related objects.

Collapse All
Field

Type

Description

data

object

Attachment data from a response.

attributes [required]

object

The attachment's attributes.

attachment

object

The attachment object.

documentUrl

string

The URL of the attachment.

title

string

The title of the attachment.

attachment_type

enum

The type of the attachment. Allowed enum values: postmortem,link

modified

date-time

Timestamp when the attachment was last modified.

id [required]

string

The unique identifier of the attachment.

relationships [required]

object

The attachment's resource relationships.

incident

object

Relationship to incident.

data [required]

object

Relationship to incident object.

id [required]

string

A unique identifier that represents the incident.

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

included

[ <oneOf>]

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Code Example
Curl
Go
Java
Python
Ruby
Rust
Typescript
"""
Update incident attachment returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_attachment_type import IncidentAttachmentType
from datadog_api_client.v2.model.patch_attachment_request import PatchAttachmentRequest
from datadog_api_client.v2.model.patch_attachment_request_data import PatchAttachmentRequestData
from datadog_api_client.v2.model.patch_attachment_request_data_attributes import PatchAttachmentRequestDataAttributes
from datadog_api_client.v2.model.patch_attachment_request_data_attributes_attachment import (
    PatchAttachmentRequestDataAttributesAttachment,
)

# there is a valid "incident" in the system
INCIDENT_DATA_ID = environ["INCIDENT_DATA_ID"]

# there is a valid "incident_attachment" in the system
INCIDENT_ATTACHMENT_DATA_ID = environ["INCIDENT_ATTACHMENT_DATA_ID"]

body = PatchAttachmentRequest(
    data=PatchAttachmentRequestData(
        attributes=PatchAttachmentRequestDataAttributes(
            attachment=PatchAttachmentRequestDataAttributesAttachment(
                document_url="https://app.datadoghq.com/notebook/124/Example-Incident",
                title="Example-Incident",
            ),
        ),
        id=INCIDENT_ATTACHMENT_DATA_ID,
        type=IncidentAttachmentType.INCIDENT_ATTACHMENTS,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_incident_attachment"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_incident_attachment(
        incident_id=INCIDENT_DATA_ID, attachment_id=INCIDENT_ATTACHMENT_DATA_ID, body=body
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
Get global incident settings
v2 (latest)
Note: This endpoint is in public beta and is subject to change. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/global/settings

Overview
Retrieve global incident settings for the organization.

Response
200
400
429
OK

Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

Global incident settings attributes

analytics_dashboard_id [required]

string

The analytics dashboard ID

created [required]

date-time

Timestamp when the settings were created

modified [required]

date-time

Timestamp when the settings were last modified

id [required]

string

The unique identifier for the global incident settings

type [required]

enum

Global incident settings resource type Allowed enum values: incidents_global_settings

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get global incident settings returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["get_global_incident_settings"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.get_global_incident_settings()

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Update global incident settings
v2 (latest)
Note: This endpoint is in public beta and is subject to change. If you have any feedback, contact Datadog support.

PATCH https://api.datadoghq.com/api/v2/incidents/config/global/settings

Overview
Update global incident settings for the organization.

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes

object

Global incident settings attributes

analytics_dashboard_id

string

The analytics dashboard ID

type [required]

enum

Global incident settings resource type Allowed enum values: incidents_global_settings

Response
200
400
429
OK

Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

Global incident settings attributes

analytics_dashboard_id [required]

string

The analytics dashboard ID

created [required]

date-time

Timestamp when the settings were created

modified [required]

date-time

Timestamp when the settings were last modified

id [required]

string

The unique identifier for the global incident settings

type [required]

enum

Global incident settings resource type Allowed enum values: incidents_global_settings

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Update global incident settings returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.global_incident_settings_attributes_request import (
    GlobalIncidentSettingsAttributesRequest,
)
from datadog_api_client.v2.model.global_incident_settings_data_request import GlobalIncidentSettingsDataRequest
from datadog_api_client.v2.model.global_incident_settings_request import GlobalIncidentSettingsRequest
from datadog_api_client.v2.model.global_incident_settings_type import GlobalIncidentSettingsType

body = GlobalIncidentSettingsRequest(
    data=GlobalIncidentSettingsDataRequest(
        attributes=GlobalIncidentSettingsAttributesRequest(
            analytics_dashboard_id="abc-123-def",
        ),
        type=GlobalIncidentSettingsType.INCIDENTS_GLOBAL_SETTINGS,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_global_incident_settings"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_global_incident_settings(body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
List global incident handles
v2 (latest)
Note: This endpoint is in public beta and is subject to change. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/global/incident-handles

Overview
Retrieve a list of global incident handles.

Arguments
Query Strings
Name

Type

Description

include

string

Comma-separated list of related resources to include in the response

Response
200
400
429
OK

Model
Example
Collapse All
Field

Type

Description

data [required]

[object]

attributes [required]

object

Incident handle attributes for responses

created_at [required]

date-time

Timestamp when the handle was created

fields [required]

object

Dynamic fields associated with the handle

severity

[string]

Severity levels associated with the handle

modified_at [required]

date-time

Timestamp when the handle was last modified

name [required]

string

The handle name

id [required]

string

The ID of the incident handle

relationships

object

commander_user

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

created_by_user [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

incident_type [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

last_modified_by_user [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

type [required]

enum

Incident handle resource type Allowed enum values: incidents_handles

included

[ <oneOf>]

Included related resources

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
List global incident handles returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["list_global_incident_handles"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_global_incident_handles()

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Create global incident handle
v2 (latest)
Note: This endpoint is in public beta and is subject to change. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/config/global/incident-handles

Overview
Create a new global incident handle.

Arguments
Query Strings
Name

Type

Description

include

string

Comma-separated list of related resources to include in the response

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

Incident handle attributes for requests

fields

object

Dynamic fields associated with the handle

severity

[string]

Severity levels associated with the handle

name [required]

string

The handle name

id

string

The ID of the incident handle (required for PUT requests)

relationships

object

commander_user

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

incident_type [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

type [required]

enum

Incident handle resource type Allowed enum values: incidents_handles

Response
201
400
429
Created

Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

Incident handle attributes for responses

created_at [required]

date-time

Timestamp when the handle was created

fields [required]

object

Dynamic fields associated with the handle

severity

[string]

Severity levels associated with the handle

modified_at [required]

date-time

Timestamp when the handle was last modified

name [required]

string

The handle name

id [required]

string

The ID of the incident handle

relationships

object

commander_user

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

created_by_user [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

incident_type [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

last_modified_by_user [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

type [required]

enum

Incident handle resource type Allowed enum values: incidents_handles

included

[ <oneOf>]

Included related resources

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Create global incident handle returns "Created" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_handle_attributes_fields import IncidentHandleAttributesFields
from datadog_api_client.v2.model.incident_handle_attributes_request import IncidentHandleAttributesRequest
from datadog_api_client.v2.model.incident_handle_data_request import IncidentHandleDataRequest
from datadog_api_client.v2.model.incident_handle_relationship import IncidentHandleRelationship
from datadog_api_client.v2.model.incident_handle_relationship_data import IncidentHandleRelationshipData
from datadog_api_client.v2.model.incident_handle_relationships_request import IncidentHandleRelationshipsRequest
from datadog_api_client.v2.model.incident_handle_request import IncidentHandleRequest
from datadog_api_client.v2.model.incident_handle_type import IncidentHandleType

body = IncidentHandleRequest(
    data=IncidentHandleDataRequest(
        attributes=IncidentHandleAttributesRequest(
            fields=IncidentHandleAttributesFields(
                severity=[
                    "SEV-1",
                ],
            ),
            name="@incident-sev-1",
        ),
        id="b2494081-cdf0-4205-b366-4e1dd4fdf0bf",
        relationships=IncidentHandleRelationshipsRequest(
            commander_user=IncidentHandleRelationship(
                data=IncidentHandleRelationshipData(
                    id="f7b538b1-ed7c-4e84-82de-fdf84a539d40",
                    type="incident_types",
                ),
            ),
            incident_type=IncidentHandleRelationship(
                data=IncidentHandleRelationshipData(
                    id="f7b538b1-ed7c-4e84-82de-fdf84a539d40",
                    type="incident_types",
                ),
            ),
        ),
        type=IncidentHandleType.INCIDENTS_HANDLES,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_global_incident_handle"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_global_incident_handle(body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Update global incident handle
v2 (latest)
Note: This endpoint is in public beta and is subject to change. If you have any feedback, contact Datadog support.

PUT https://api.datadoghq.com/api/v2/incidents/config/global/incident-handles

Overview
Update an existing global incident handle.

Arguments
Query Strings
Name

Type

Description

include

string

Comma-separated list of related resources to include in the response

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

Incident handle attributes for requests

fields

object

Dynamic fields associated with the handle

severity

[string]

Severity levels associated with the handle

name [required]

string

The handle name

id

string

The ID of the incident handle (required for PUT requests)

relationships

object

commander_user

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

incident_type [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

type [required]

enum

Incident handle resource type Allowed enum values: incidents_handles

Response
200
400
429
OK

Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

Incident handle attributes for responses

created_at [required]

date-time

Timestamp when the handle was created

fields [required]

object

Dynamic fields associated with the handle

severity

[string]

Severity levels associated with the handle

modified_at [required]

date-time

Timestamp when the handle was last modified

name [required]

string

The handle name

id [required]

string

The ID of the incident handle

relationships

object

commander_user

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

created_by_user [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

incident_type [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

last_modified_by_user [required]

object

data [required]

object

id [required]

string

The ID of the related resource

type [required]

string

The type of the related resource

type [required]

enum

Incident handle resource type Allowed enum values: incidents_handles

included

[ <oneOf>]

Included related resources

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Update global incident handle returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.incident_handle_attributes_fields import IncidentHandleAttributesFields
from datadog_api_client.v2.model.incident_handle_attributes_request import IncidentHandleAttributesRequest
from datadog_api_client.v2.model.incident_handle_data_request import IncidentHandleDataRequest
from datadog_api_client.v2.model.incident_handle_relationship import IncidentHandleRelationship
from datadog_api_client.v2.model.incident_handle_relationship_data import IncidentHandleRelationshipData
from datadog_api_client.v2.model.incident_handle_relationships_request import IncidentHandleRelationshipsRequest
from datadog_api_client.v2.model.incident_handle_request import IncidentHandleRequest
from datadog_api_client.v2.model.incident_handle_type import IncidentHandleType

body = IncidentHandleRequest(
    data=IncidentHandleDataRequest(
        attributes=IncidentHandleAttributesRequest(
            fields=IncidentHandleAttributesFields(
                severity=[
                    "SEV-1",
                ],
            ),
            name="@incident-sev-1",
        ),
        id="b2494081-cdf0-4205-b366-4e1dd4fdf0bf",
        relationships=IncidentHandleRelationshipsRequest(
            commander_user=IncidentHandleRelationship(
                data=IncidentHandleRelationshipData(
                    id="f7b538b1-ed7c-4e84-82de-fdf84a539d40",
                    type="incident_types",
                ),
            ),
            incident_type=IncidentHandleRelationship(
                data=IncidentHandleRelationshipData(
                    id="f7b538b1-ed7c-4e84-82de-fdf84a539d40",
                    type="incident_types",
                ),
            ),
        ),
        type=IncidentHandleType.INCIDENTS_HANDLES,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_global_incident_handle"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_global_incident_handle(body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Delete global incident handle
v2 (latest)
Note: This endpoint is in public beta and is subject to change. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/config/global/incident-handles

Overview
Delete a global incident handle.

Response
204
400
429
No Content

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete global incident handle returns "No Content" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["delete_global_incident_handle"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_global_incident_handle()
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
List postmortem templates
v2 (latest)
Note: This endpoint is in preview and is subject to change. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/postmortem-templates

Overview
Retrieve a list of all postmortem templates for incidents.

Response
200
400
429
OK

Model
Example
Collapse All
Field

Type

Description

data [required]

[object]

attributes [required]

object

createdAt [required]

date-time

When the template was created

modifiedAt [required]

date-time

When the template was last modified

name [required]

string

The name of the template

id [required]

string

The ID of the template

type [required]

enum

Postmortem template resource type Allowed enum values: postmortem_template

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
List postmortem templates returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["list_incident_postmortem_templates"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.list_incident_postmortem_templates()

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Create postmortem template
v2 (latest)
Note: This endpoint is in preview and is subject to change. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/config/postmortem-templates

Overview
Create a new postmortem template for incidents.

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

name [required]

string

The name of the template

type [required]

enum

Postmortem template resource type Allowed enum values: postmortem_template

Response
201
400
403
429
Created

Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

createdAt [required]

date-time

When the template was created

modifiedAt [required]

date-time

When the template was last modified

name [required]

string

The name of the template

id [required]

string

The ID of the template

type [required]

enum

Postmortem template resource type Allowed enum values: postmortem_template

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Create postmortem template returns "Created" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.postmortem_template_attributes_request import PostmortemTemplateAttributesRequest
from datadog_api_client.v2.model.postmortem_template_data_request import PostmortemTemplateDataRequest
from datadog_api_client.v2.model.postmortem_template_request import PostmortemTemplateRequest
from datadog_api_client.v2.model.postmortem_template_type import PostmortemTemplateType

body = PostmortemTemplateRequest(
    data=PostmortemTemplateDataRequest(
        attributes=PostmortemTemplateAttributesRequest(
            name="Standard Postmortem Template",
        ),
        type=PostmortemTemplateType.POSTMORTEM_TEMPLATE,
    ),
)

configuration = Configuration()
configuration.unstable_operations["create_incident_postmortem_template"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.create_incident_postmortem_template(body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Get postmortem template
v2 (latest)
Note: This endpoint is in preview and is subject to change. If you have any feedback, contact Datadog support.

GET https://api.datadoghq.com/api/v2/incidents/config/postmortem-templates/{template_id}

Overview
Retrieve details of a specific postmortem template.

Arguments
Path Parameters
Name

Type

Description

template_id [required]

string

The ID of the postmortem template

Response
200
400
404
429
OK

Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

createdAt [required]

date-time

When the template was created

modifiedAt [required]

date-time

When the template was last modified

name [required]

string

The name of the template

id [required]

string

The ID of the template

type [required]

enum

Postmortem template resource type Allowed enum values: postmortem_template

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Get postmortem template returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["get_incident_postmortem_template"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.get_incident_postmortem_template(
        template_id="template-456",
    )

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Update postmortem template
v2 (latest)
Note: This endpoint is in preview and is subject to change. If you have any feedback, contact Datadog support.

PATCH https://api.datadoghq.com/api/v2/incidents/config/postmortem-templates/{template_id}

Overview
Update an existing postmortem template.

Arguments
Path Parameters
Name

Type

Description

template_id [required]

string

The ID of the postmortem template

Request
Body Data (required)
Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

name [required]

string

The name of the template

type [required]

enum

Postmortem template resource type Allowed enum values: postmortem_template

Response
200
400
404
429
OK

Model
Example
Collapse All
Field

Type

Description

data [required]

object

attributes [required]

object

createdAt [required]

date-time

When the template was created

modifiedAt [required]

date-time

When the template was last modified

name [required]

string

The name of the template

id [required]

string

The ID of the template

type [required]

enum

Postmortem template resource type Allowed enum values: postmortem_template

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Update postmortem template returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from datadog_api_client.v2.model.postmortem_template_attributes_request import PostmortemTemplateAttributesRequest
from datadog_api_client.v2.model.postmortem_template_data_request import PostmortemTemplateDataRequest
from datadog_api_client.v2.model.postmortem_template_request import PostmortemTemplateRequest
from datadog_api_client.v2.model.postmortem_template_type import PostmortemTemplateType

body = PostmortemTemplateRequest(
    data=PostmortemTemplateDataRequest(
        attributes=PostmortemTemplateAttributesRequest(
            name="Standard Postmortem Template",
        ),
        type=PostmortemTemplateType.POSTMORTEM_TEMPLATE,
    ),
)

configuration = Configuration()
configuration.unstable_operations["update_incident_postmortem_template"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    response = api_instance.update_incident_postmortem_template(template_id="template-456", body=body)

    print(response)
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Delete postmortem template
v2 (latest)
Note: This endpoint is in preview and is subject to change. If you have any feedback, contact Datadog support.

DELETE https://api.datadoghq.com/api/v2/incidents/config/postmortem-templates/{template_id}

Overview
Delete a postmortem template.

Arguments
Path Parameters
Name

Type

Description

template_id [required]

string

The ID of the postmortem template

Response
204
400
404
429
No Content

Code Example
Curl
Python
Ruby
Go
Java
Rust
Typescript
"""
Delete postmortem template returns "No Content" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

configuration = Configuration()
configuration.unstable_operations["delete_incident_postmortem_template"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    api_instance.delete_incident_postmortem_template(
        template_id="template-456",
    )
Instructions
First install the library and its dependencies and then save the example to example.py and run following commands:

DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>" python3 "example.py"
Import an incident
v2 (latest)
Note: This endpoint is in Preview. If you have any feedback, contact Datadog support.

POST https://api.datadoghq.com/api/v2/incidents/import

Overview
Import an incident from an external system. This endpoint allows you to create incidents with historical data such as custom timestamps for detection, declaration, and resolution. Imported incidents do not execute integrations or notification rules. This endpoint requires the incident_write permission.

OAuth apps require the incident_write authorization scope to access this endpoint.

Arguments
Query Strings
Name

Type

Description

include

array

Specifies which related object types to include in the response when importing an incident.

Request
Body Data (required)
Incident import payload.

Model
Example
Collapse All
Field

Type

Description

data [required]

object

Incident data for an import request.

attributes [required]

object

The incident's attributes for an import request.

declared

date-time

Timestamp when the incident was declared.

detected

date-time

Timestamp when the incident was detected.

fields

object

A condensed view of the user-defined fields for which to create initial selections.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

value

[string]

The multiple values selected for this field.

incident_type_uuid

string

A unique identifier that represents the incident type. If not provided, the default incident type is used.

resolved

date-time

Timestamp when the incident was resolved. Can only be set when the state field is set to 'resolved'.

title [required]

string

The title of the incident that summarizes what happened.

visibility

enum

The visibility of the incident. Allowed enum values: organization,private

default: organization

relationships

object

The relationships for an incident import request.

commander_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

declared_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

Response
201
400
401
403
404
429
CREATED

Model
Example
Response with an incident.

Collapse All
Field

Type

Description

data [required]

object

Incident data from an import response.

attributes

object

The incident's attributes from an import response.

archived

date-time

Timestamp when the incident was archived.

case_id

int64

The incident case ID.

created

date-time

Timestamp when the incident was created.

created_by_uuid

string

UUID of the user who created the incident.

creation_idempotency_key

string

A unique key used to ensure idempotent incident creation.

customer_impact_end

date-time

Timestamp when customers were no longer impacted by the incident.

customer_impact_scope

string

A summary of the impact customers experienced during the incident.

customer_impact_start

date-time

Timestamp when customers began to be impacted by the incident.

declared

date-time

Timestamp when the incident was declared.

declared_by_uuid

string

UUID of the user who declared the incident.

detected

date-time

Timestamp when the incident was detected.

fields

object

A condensed view of the user-defined fields attached to incidents.

<any-key>

 <oneOf>

Dynamic fields for which selections can be made, with field names as keys.

Option 1

object

A field with a single value selected.

type

enum

Type of the single value field definitions. Allowed enum values: dropdown,textbox

default: dropdown

value

string

The single value selected for this field.

Option 2

object

A field with potentially multiple values selected.

type

enum

Type of the multiple value field definitions. Allowed enum values: multiselect,textarray,metrictag,autocomplete

default: multiselect

value

[string]

The multiple values selected for this field.

incident_type_uuid

string

A unique identifier that represents an incident type.

is_test

boolean

A flag indicating whether the incident is a test incident.

last_modified_by_uuid

string

UUID of the user who last modified the incident.

modified

date-time

Timestamp when the incident was last modified.

non_datadog_creator

object

Incident's non Datadog creator.

image_48_px

string

Non Datadog creator 48px image.

name

string

Non Datadog creator name.

notification_handles

[object]

Notification handles that are notified of the incident during update.

display_name

string

The name of the notified handle.

handle

string

The handle used for the notification. This includes an email address, Slack channel, or workflow.

public_id

int64

The monotonically increasing integer ID for the incident.

resolved

date-time

Timestamp when the incident's state was last changed from active or stable to resolved or completed.

severity

enum

The incident severity. Allowed enum values: UNKNOWN,SEV-0,SEV-1,SEV-2,SEV-3,SEV-4,SEV-5

state

string

The state of the incident.

title [required]

string

The title of the incident that summarizes what happened.

visibility

string

The incident visibility status.

id [required]

string

The incident's ID.

relationships

object

The incident's relationships from an import response.

attachments

object

A relationship reference for attachments.

data [required]

[object]

An array of incident attachments.

id [required]

string

A unique identifier that represents the attachment.

type [required]

enum

The incident attachment resource type. Allowed enum values: incident_attachments

default: incident_attachments

commander_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

declared_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

impacts

object

Relationship to impacts.

data [required]

[object]

An array of incident impacts.

id [required]

string

A unique identifier that represents the impact.

type [required]

enum

The incident impacts type. Allowed enum values: incident_impacts

incident_type

object

Relationship to an incident type.

data [required]

object

Relationship to incident type object.

id [required]

string

The incident type's ID.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

integrations

object

A relationship reference for multiple integration metadata objects.

data [required]

[object]

Integration metadata relationship array

id [required]

string

A unique identifier that represents the integration metadata.

type [required]

enum

Integration metadata resource type. Allowed enum values: incident_integrations

default: incident_integrations

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

responders

object

Relationship to incident responders.

data [required]

[object]

An array of incident responders.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident responders type. Allowed enum values: incident_responders

user_defined_fields

object

Relationship to incident user defined fields.

data [required]

[object]

An array of user defined fields.

id [required]

string

A unique identifier that represents the responder.

type [required]

enum

The incident user defined fields type. Allowed enum values: user_defined_field

type [required]

enum

Incident resource type. Allowed enum values: incidents

default: incidents

included

[ <oneOf>]

Included related resources that the user requested.

Option 1

object

User object returned by the API.

attributes

object

Attributes of user object returned by the API.

email

string

Email of the user.

handle

string

Handle of the user.

icon

string

URL of the user's icon.

name

string

Name of the user.

uuid

string

UUID of the user.

id

string

ID of the user.

type

enum

Users resource type. Allowed enum values: users

default: users

Option 2

object

Incident type response data.

attributes

object

Incident type's attributes.

createdAt

date-time

Timestamp when the incident type was created.

createdBy

string

A unique identifier that represents the user that created the incident type.

description

string

Text that describes the incident type.

is_default

boolean

If true, this incident type will be used as the default incident type if a type is not specified during the creation of incident resources.

lastModifiedBy

string

A unique identifier that represents the user that last modified the incident type.

modifiedAt

date-time

Timestamp when the incident type was last modified.

name [required]

string

The name of the incident type.

prefix

string

The string that will be prepended to the incident title across the Datadog app.

id [required]

string

The incident type's ID.

relationships

object

The incident type's resource relationships.

created_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

google_meet_configuration

object

A reference to a Google Meet Configuration resource.

data [required]

object

The Google Meet configuration relationship data object.

id [required]

string

The unique identifier of the Google Meet configuration.

type [required]

string

The type of the Google Meet configuration.

last_modified_by_user

object

Relationship to user.

data [required]

object

Relationship to user object.

id [required]

string

A unique identifier that represents the user.

type [required]

enum

Users resource type. Allowed enum values: users

default: users

microsoft_teams_configuration

object

A reference to a Microsoft Teams Configuration resource.

data [required]

object

The Microsoft Teams configuration relationship data object.

id [required]

string

The unique identifier of the Microsoft Teams configuration.

type [required]

string

The type of the Microsoft Teams configuration.

zoom_configuration

object

A reference to a Zoom configuration resource.

data [required]

object

The Zoom configuration relationship data object.

id [required]

string

The unique identifier of the Zoom configuration.

type [required]

string

The type of the Zoom configuration.

type [required]

enum

Incident type resource type. Allowed enum values: incident_types

default: incident_types

Code Example
Curl
# Curl command
curl -X POST "https://api.datadoghq.com/api/v2/incidents/import" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
-d @- << EOF
{
  "data": {
    "type": "incidents",
    "attributes": {
      "title": "Example-Incident",
      "visibility": "organization"
    }
  }
}
EOF