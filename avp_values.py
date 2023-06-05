avp_values = dict()

# The Media-Type AVP (AVP code 520) is of type Enumerated, and it determines the media type of a session
# component. The media types indicate the type of media in the same way as the SDP media types with the same names
# defined in RFC 4566 [13]. The following values are defined:
# - AUDIO (0)
# - VIDEO (1)
# - DATA (2)
# - APPLICATION (3)
# ETSI
# 3GPP TS 29.214 version 7.4.0 Release 7 23 ETSI TS 129 214 V7.4.0 (2008-04)
# - CONTROL (4)
# - TEXT (5)
# - MESSAGE (6)
# - OTHER (0xFFFFFFFF)
avp_values["diameter.Media-Type"] = dict()
avp_values["diameter.Media-Type"]["0"] = "AUDIO"
avp_values["diameter.Media-Type"]["1"] = "VIDEO"
avp_values["diameter.Media-Type"]["2"] = "DATA"


# 5.3.13 Specific-Action AVP
# The Specific-Action AVP (AVP code 513) is of type Enumerated.
# Within a PCRF initiated Re-Authorization Request, the Specific-Action AVP determines the type of the action.
# Within an initial AA request the AF may use the Specific-Action AVP to request specific actions from the server at the
# bearer events and to limit the contact to such bearer events where specific action is required. If the Specific-Action AVP
# is omitted within the initial AA request, no notification of any of the events defined below is requested.
# The following values are defined:
# ETSI
# 3GPP TS 29.214 version 7.4.0 Release 7 20 ETSI TS 129 214 V7.4.0 (2008-04)
# SERVICE_INFORMATION_REQUEST (0)
#  Within a RAR, this value shall be used when the server requests the service information from the AF for the
# bearer event. In the AAR, this value indicates that the AF requests the server to demand service information
# at each bearer authorization.
# CHARGING_CORRELATION_EXCHANGE (1)
#  Within a RAR, this value shall be used when the server reports the access network charging identifier to the
# AF. The Access-Network-Charging-Identifier AVP shall be included within the request. In the AAR, this
# value indicates that the AF requests the server to provide an access network charging identifier to the AF at
# each bearer establishment/modification, when a new access network charging identifier becomes available.
# INDICATION_OF_LOSS_OF_BEARER (2)
#  Within a RAR, this value shall be used when the server reports a loss of a bearer (e.g. in the case of GPRS
# PDP context bandwidth modification to 0 kbit) to the AF. The SDFs that are deactivated as a consequence of
# this loss of bearer shall be provided within the Flows AVP. In the AAR, this value indicates that the AF
# requests the server to provide a notification at the loss of a bearer.
# INDICATION_OF_RECOVERY_OF_BEARER (3)
#  Within a RAR, this value shall be used when the server reports a recovery of a bearer (e.g. in the case of
# GPRS, PDP context bandwidth modification from 0 kbit to another value) to the AF. The SDFs that are reactivated as a consequence of the recovery of bearer shall be provided within the Flows AVP. In the AAR,
# this value indicates that the AF requests the server to provide a notification at the recovery of a bearer.
# INDICATION_OF_RELEASE_OF_BEARER (4)
#  Within a RAR, this value shall be used when the server reports the release of a bearer (e.g. PDP context
# removal for GPRS) to the AF. The SDFs that are deactivated as a consequence of this release of bearer shall
# be provided within the Flows AVP. In the AAR, this value indicates that the AF requests the server to
# provide a notification at the removal of a bearer.
# INDICATION_OF_ESTABLISHMENT_OF_BEARER (5)
#  Within a RAR, this value shall be used when the server reports the establishment of a bearer (e.g. PDP
# context activation for GPRS) to the AF. In the AAR, this value indicates that the AF requests the server to
# provide a notification at the establishment of a bearer.
# IP-CAN_CHANGE (6)
# This value shall be used in RAR command by the PCRF to indicate a change in the IP-CAN type. When used in
# an AAR command, this value indicates that the AF is requesting subscription for IP-CAN change notification.
# When used in RAR it indicates that the PCRF generated the request because of an IP-CAN change. IP-CANType AVP shall be provided in the same request with the new value. For 3GPP IP-CAN type value, 3GPP-RATType AVP shall also be provided.
# SERVICE_INFORMATION_REQUEST is maintained for backward compatibility with previous releases and shall not
# be used in Rx messages in this release and shall be ignored in incoming messages. 

avp_values["diameter.Specific-Action"] = dict()
avp_values["diameter.Specific-Action"]["0"] = "SERVICE_INFORMATION_REQUEST"
avp_values["diameter.Specific-Action"]["1"] = "CHARGING_CORRELATION_EXCHANGE"
avp_values["diameter.Specific-Action"]["2"] = "INDICATION_OF_LOSS_OF_BEARER"
avp_values["diameter.Specific-Action"]["3"] = "INDICATION_OF_RECOVERY_OF_BEARER"
avp_values["diameter.Specific-Action"]["4"] = "INDICATION_OF_RELEASE_OF_BEARER"
avp_values["diameter.Specific-Action"]["5"] = "INDICATION_OF_ESTABLISHMENT_OF_BEARER"
avp_values["diameter.Specific-Action"]["6"] = "IP-CAN_CHANGE"

# 5.3.12 Flow-Usage AVP
# The Flow-Usage AVP (AVP code 512) is of type Enumerated, and provides information about the usage of IP Flows.
# The following values are defined:
# NO_INFORMATION (0)
#  This value is used to indicate that no information about the usage of the IP flow is being provided.
# RTCP (1)
#  This value is used to indicate that an IP flow is used to transport RTCP.
# AF_SIGNALLING (2)
#  This value is used to indicate that the IP flow is used to transport AF Signalling Protocols (e.g. SIP/SDP).
# NO_INFORMATION is the default value.
# NOTE: An AF may choose not to identify RTCP flows, e.g. in order to avoid that RTCP flows are always
# enabled by the server

avp_values["diameter.Flow-Usage"] = dict()
avp_values["diameter.Flow-Usage"]["0"] = "NO_INFORMATION"
avp_values["diameter.Flow-Usage"]["1"] = "RTCP"
avp_values["diameter.Flow-Usage"]["2"] = "AF_SIGNALLING"


# 5.3.11 Flow-Number AVP
# The Flow-Number AVP (AVP code 511) is of type Unsigned32, and provides a unique identifier for an IP Flow within a
# session.
# NOTE: The Flow-Number AVP is used to identify the IP Flow within a session. The Flow-Number AVP is not used to
# identify the IP Flow within the IP-CAN bearer. The Flow-Number AVP is used to identify the IP Flow within the
# session, e.g. in the Flows AVP.


avp_values["diameter.RAT-Type"] = dict()
avp_values["diameter.RAT-Type"]["1004"] = "EUTRAN"
avp_values["diameter.RAT-Type"]["1000"] = "UTRAN"
avp_values["diameter.RAT-Type"]["1001"] = "GERAN"
avp_values["diameter.RAT-Type"]["1002"] = "GAN"
avp_values["diameter.RAT-Type"]["1003"] = "HSPA-Evolution"
avp_values["diameter.RAT-Type"]["0"] = "WLAN"



# 5.3.27 IP-CAN-Type AVP (All access types)
# The IP-CAN-Type AVP (AVP code 1027) is of type Enumerated, and it shall indicate the type of Connectivity Access
# Network in which the user is connected.
# The IP-CAN-Type AVP shall always be present during the IP-CAN session establishment. During an IP-CAN session
# modification, this AVP shall be present when there has been a change in the IP-CAN type and the PCRF requested to be
# informed of this event. The Event-Trigger AVP with value IP-CAN_CHANGE shall be provided together with the IPCAN-Type AVP.
# NOTE: The informative Annex C presents a mapping between the code values for different access network types.
# The following values are defined:
# 3GPP-GPRS (0)
# This value shall be used to indicate that the IP-CAN is associated with a 3GPP GPRS access that is connected to
# the GGSN based on the Gn/Gp interfaces and is further detailed by the RAT-Type AVP. RAT-Type AVP will
# include applicable 3GPP values, except EUTRAN.
# DOCSIS (1)
# This value shall be used to indicate that the IP-CAN is associated with a DOCSIS access.
# xDSL (2)
# This value shall be used to indicate that the IP-CAN is associated with an xDSL access.
# WiMAX (3)
# This value shall be used to indicate that the IP-CAN is associated with a WiMAX access (IEEE 802.16).
# 3GPP2 (4)
# This value shall be used to indicate that the IP-CAN is associated with a 3GPP2 access connected to the 3GPP2
# packet core as specified in 3GPP2 X.S0011 [20] and is further detailed by the RAT-Type AVP.
# 3GPP-EPS (5)
# This value shall be used to indicate that the IP-CAN is associated with a 3GPP EPS access and is further detailed
# by the RAT-Type AVP.
#  Non-3GPP-EPS (6)
# This value shall be used to indicate that the IP-CAN is associated with an EPC based non-3GPP access and is
# further detailed by the RAT-Type AVP. 

avp_values["diameter.IP-CAN-Type"] = dict()
avp_values["diameter.IP-CAN-Type"]["0"] = "3GPP-GPRS"
avp_values["diameter.IP-CAN-Type"]["1"] = "DOCSIS"
avp_values["diameter.IP-CAN-Type"]["2"] = "xDSL"
avp_values["diameter.IP-CAN-Type"]["3"] = "WiMAX"
avp_values["diameter.IP-CAN-Type"]["4"] = "3GPP2"
avp_values["diameter.IP-CAN-Type"]["5"] = "3GPP-EPS"
avp_values["diameter.IP-CAN-Type"]["6"] = "Non-3GPP-EPS"



# 5.3.7 Event-Trigger AVP (All access types)
# The Event-Trigger AVP (AVP code 1006) is of type Enumerated. When sent from the PCRF to the PCEF the EventTrigger AVP indicates an event that shall cause a re-request of PCC rules. When sent from the PCEF to the PCRF the
# Event-Trigger AVP indicates that the corresponding event has occurred at the gateway.
# NOTE 1: An exception to the above is the Event Trigger AVP set to NO_EVENT_TRIGGERS that indicates that
# PCEF shall not notify PCRF of any event that requires to be provisioned.
# NOTE 2: There are events that do not require to be provisioned by the PCRF, according to the value definition
# included in this clause. These events will always be reported by the PCEF even though the PCRF has not
# provisioned them in a RAR or CCA command.
# Whenever the PCRF subscribes to one or more event triggers by using the RAR command, the PCEF shall send the
# corresponding currently applicable values (e.g. 3GPP-SGSN-Address AVP or 3GPP-SGSN-IPv6-Address AVP, RATType, 3GPP-User-Location-Info, etc.) to the PCRF in the RAA if available, and in this case, the Event-Trigger AVPs
# shall not be included.
# Whenever one of these events occurs, the PCEF shall send the related AVP that has changed together with the event
# trigger indication.
# Unless stated for a specific value, the Event-Trigger AVP applies to all access types.
# The values 8, 9 and 10 are obsolete and shall not be used.
# The following values are defined:
# SGSN_CHANGE (0)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon the change of the
# serving SGSN PCC rules shall be requested. When used in a CCR command, this value indicates that the PCEF
# generated the request because the serving SGSN changed. The new value of the serving SGSN shall be indicated
# in either 3GPP-SGSN-Address AVP or 3GPP-SGSN-IPv6-Address AVP. Applicable only to 3GPP-GPRS and
# 3GPP-EPS access types.
# QOS_CHANGE (1)
# ETSI
# 3GPP TS 29.212 version 8.6.0 Release 8 42 ETSI TS 129 212 V8.6.0 (2010-01)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon any QoS change (even
# within the limits of the current authorization) at bearer or APN level PCC rules shall be requested. When used in
# a CCR command, this value indicates that the PCEF generated the request because there has been a change in the
# requested QoS for a specific bearer (e.g. the previously maximum authorized QoS has been exceeded) or APN.
# The Bearer-Identifier AVP shall be provided to indicate the affected bearer. QoS-Information AVP is required to
# be provided in the same request with the new value.
# RAT_CHANGE (2)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon a RAT change PCC
# rules shall be requested. When used in a CCR command, this value indicates that the PCEF generated the request
# because of a RAT change. The new RAT type shall be provided in the RAT-Type AVP.
# TFT_CHANGE (3)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon a TFT change at bearer
# level PCC rules shall be requested. When used in a CCR command, this value indicates that the PCEF generated
# the request because of a change in the TFT. The Bearer-Identifier AVP shall be provided to indicate the affected
# bearer. All the TFT values for this bearer shall be provided in TFT-Packet-Filter-Information AVP. This event
# trigger shall be provisioned by the PCRF at the PCEF. Applicable only to 3GPP-GPRS.
# PLMN_CHANGE (4)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon a PLMN change PCC
# rules shall be requested. When used in a CCR command, this value indicates that the PCEF generated the request
# because there was a change of PLMN. 3GPP-SGSN-MCC-MNC AVP shall be provided in the same request with
# the new value.
# LOSS_OF_BEARER (5)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon loss of bearer, GW
# should inform PCRF. When used in a CCR command, this value indicates that the PCEF generated the request
# because the bearer associated with the PCC rules indicated by the corresponding Charging-Rule-Report AVP
# was lost. The PCC-Rule-Status AVP within the Charging-Rule-Report AVP shall indicate that these PCC rules
# are temporarily inactive. Applicable to those access-types that handle multiple bearers within one single IP-CAN
# session (e.g. GPRS).
# The mechanism of indicating loss of bearer to the GW is IP-CAN access type specific. For GPRS, this is
# indicated by a PDP context modification request with Maximum Bit Rate (MBR) in QoS profile changed to 0
# kbps.
# When the PCRF performs the bearer binding, the PCEF shall provide the Bearer-Identifier AVP to indicate the
# bearer that has been lost.
# RECOVERY_OF_BEARER (6)
# This value shall be in CCA and RAR commands by the PCRF used to indicate that upon recovery of bearer, GW
# should inform PCRF. When used in a CCR command, this value indicates that the PCEF generated the request
# because the bearer associated with the PCC rules indicated by the corresponding Charging-Rule-Report AVP
# was recovered. The PCC-Rule-Status AVP within the Charging-Rule-Report AVP shall indicate that these rules
# are active again. Applicable to those access-types that handle multiple bearers within one single IP-CAN session
# (e.g. GPRS).
# The mechanism for indicating recovery of bearer to the GW is IP-CAN access type specific. For GPRS, this is
# indicated by a PDP context modification request with Maximum Bit Rate (MBR) in QoS profile changed from 0
# kbps to a valid value.
# When the PCRF performs the bearer binding, the PCEF shall provide the Bearer-Identifier AVP to indicate the
# bearer that has been recovered.
# IP-CAN_CHANGE (7)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon a change in the IP-CAN
# type PCC rules shall be requested. When used in a CCR command, this value indicates that the PCEF generated
# the request because there was a change of IP-CAN type. IP-CAN-Type AVP shall be provided in the same
# request with the new value. The RAT-Type AVP shall also be provided when applicable to the specific IP-CAN
# Type (e.g. 3GPP IP-CAN Type)
# ETSI
# 3GPP TS 29.212 version 8.6.0 Release 8 43 ETSI TS 129 212 V8.6.0 (2010-01)
# QOS_CHANGE_EXCEEDING_AUTHORIZATION (11)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that only upon a requested QoS
# change beyond the current authorized value(s) at bearer level PCC rules shall be requested. When used in a CCR
# command, this value indicates that the PCEF generated the request because there has been a change in the
# requested QoS beyond the authorized value(s) for a specific bearer. The Bearer-Identifier AVP shall be provided
# to indicate the affected bearer. QoS-Information AVP is required to be provided in the same request with the
# new value.
# RAI_CHANGE (12)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon a change in the RAI,
# PCEF shall inform the PCRF. When used in a CCR command, this value indicates that the PCEF generated the
# request because there has been a change in the RAI. The new RAI value shall be provided in the RAI AVP. If
# the user location has been changed but the PCEF can not get the detail location information for some reasons
# (eg. handover from 3G to 2G network), the PCEF shall send the RAI AVP to the PCRF by setting the LAC of
# the RAI to value 0x0000. Applicable only to 3GPP-GPRS and 3GPP-EPS access types.
# USER_LOCATION_CHANGE (13)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon a change in the user
# location, PCEF shall inform the PCRF. When used in a CCR command, this value indicates that the PCEF
# generated the request because there has been a change in the user location. The new location value shall be
# provided in the 3GPP-User-Location-Info AVP. If the user location has been changed but the PCEF can not get
# the detail location information for some reasons (eg. handover from 3G to 2G network), the PCEF shall send the
# 3GPP-User-Location-Info AVP to the PCRF by setting the LAC of the CGI/SAI to value 0x0000. Applicable
# only to 3GPP-GPRS and 3GPP-EPS access types.
# NO_EVENT_TRIGGERS (14)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that PCRF does not require any
# Event Trigger notification except for those events that do not require subscription and are always provisioned.
# OUT_OF_CREDIT (15)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that the PCEF shall inform the
# PCRF about the PCC rules for which credit is no longer available, together with the applied termination action.
# When used in a CCR command, this value indicates that the PCEF generated the request because the PCC rules
# indicated by the corresponding Charging-Rule-Report AVP have run out of credit, and that the termination
# action indicated by the corresponding Final-Unit-Indication AVP applies applies (3GPP TS 32.240 [21] and
# 3GPP TS 32.299 [19]).
# REALLOCATION_OF_CREDIT (16)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that the PCEF shall inform the
# PCRF about the PCC rules for which credit has been reallocated after the former out of credit indication. When
# used in a CCR command, this value indicates that the PCEF generated the request because the PCC rules
# indicated by the corresponding Charging-Rule-Report AVP have been reallocated credit after the former out of
# credit indication (3GPP TS 32.240 [21] and 3GPP TS 32.299 [19]).
# REVALIDATION_TIMEOUT (17)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon revalidation timeout,
# PCEF shall inform the PCRF. When used in a CCR command, this value indicates that the PCEF generated the
# request because there has been a PCC revalidation timeout.
# UE_IP_ADDRESS_ALLOCATE (18)
# When used in a CCR command, this value indicates that the PCEF generated the request because a UE IPv4
# address is allocated. The Framed-IP-Address AVP shall be provided in the same request. This event trigger does
# not require to be provisioned by the PCRF. This event trigger shall be reported when the corresponding event
# occurs, even if the event trigger is not provisioned by the PCRF.
# UE_IP_ADDRESS_RELEASE (19)
# ETSI
# 3GPP TS 29.212 version 8.6.0 Release 8 44 ETSI TS 129 212 V8.6.0 (2010-01)
# When used in a CCR command, this value indicates that the PCEF generated the request because a UE IPv4
# address is released. The Framed-IP-Address AVP shall be provided in the same request. This event trigger does
# not require to be provisioned by the PCRF. This event trigger shall be reported when the corresponding event
# occurs, even if the event trigger is not provisioned by the PCRF.
# DEFAULT_EPS_BEARER_QOS_CHANGE (20)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon a change in the default
# EPS Bearer QoS, PCEF shall inform the PCRF. When used in a CCR command, this value indicates that the
# PCEF generated the request because there has been a change in the default EPS Bearer QoS. The new value shall
# be provided in the Default-EPS-Bearer-QoS AVP. Not applicable in 3GPP-GPRS access type.
# AN_GW_CHANGE (21)
#  This value shall be used in CCA and RAR commands by the PCRF to indicate that upon the change of the
# serving Access Node Gateway, PCC rules shall be requested. When used in a CCR command, this value
# indicates that the PCEF generated the request because the serving Access Node gateway changed. The new value
# of the serving Access Node gateway shall be indicated in the AN-GW-Address AVP.
# SUCCESSFUL_RESOURCE_ALLOCATION (22)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that the PCEF can inform the
# PCRF of successful resource allocation for those rules that requires so.
# When used in a CCR or RAA command, this value indicates that the PCEF informs the PCRF that the resources
# for a rule have been successfully allocated. The affected rules are indicated within the Charging-Rule-Report
# AVP with the PCC-Rule-Status AVP set to the value ACTIVE (0).
# RESOURCE_MODIFICATION_REQUEST (23)
# This value shall be used in a CCR command to indicate that PCC rules are requested for a resource modification
# request initiated by the UE. The Packet-Filter-Operation and Packet-Filter-Information AVPs shall be provided
# in the same request. This event trigger does not require to be provisioned by the PCRF. It shall be reported by the
# PCEF when the corresponding event occurs even if the event trigger is not provisioned by the PCRF.
# PGW_TRACE_CONTROL (24)
# This value indicates that the command contains a trace activation or deactivation request for the P-GW. Trace
# activation is indicated with the presence of the Trace-Data AVP with the relevant trace parameters. Trace
# deactivation is indicated with the presence of the Trace-Reference AVP. This event trigger needs no
# subscription.
# UE_TIME_ZONE_CHANGE (25)
# This value shall be used in CCA and RAR commands by the PCRF to indicate that upon a change to the time
# zone the UE is currently located in, PCC rules shall be requested. When used in a CCR command, this value
# indicates that the PCEF generated the request because the time zone the UE is currently located in has changed.
# The new value of the UE"s time zone shall be indicated in the 3GPP-MS-TimeZone AVP.

#Create the dictionary for the Event-Trigger AVP
avp_values["diameter.Event-Trigger"] = dict()
avp_values["diameter.Event-Trigger"]["0"] = "SGSN_CHANGE"
avp_values["diameter.Event-Trigger"]["1"] = "QOS_CHANGE"
avp_values["diameter.Event-Trigger"]["2"] = "RAT_CHANGE"
avp_values["diameter.Event-Trigger"]["3"] = "TFT_CHANGE"
avp_values["diameter.Event-Trigger"]["4"] = "PLMN_CHANGE"
avp_values["diameter.Event-Trigger"]["5"] = "LOSS_OF_BEARER"
avp_values["diameter.Event-Trigger"]["6"] = "RECOVERY_OF_BEARER"
avp_values["diameter.Event-Trigger"]["7"] = "IP-CAN_CHANGE"
avp_values["diameter.Event-Trigger"]["11"] = "QOS_CHANGE_EXCEEDING_AUTHORIZATION"
avp_values["diameter.Event-Trigger"]["12"] = "RAI_CHANGE"
avp_values["diameter.Event-Trigger"]["13"] = "USER_LOCATION_CHANGE"
avp_values["diameter.Event-Trigger"]["14"] = "NO_EVENT_TRIGGERS"
avp_values["diameter.Event-Trigger"]["15"] = "OUT_OF_CREDIT"
avp_values["diameter.Event-Trigger"]["16"] = "REALLOCATION_OF_CREDIT"
avp_values["diameter.Event-Trigger"]["17"] = "REVALIDATION_TIMEOUT"
avp_values["diameter.Event-Trigger"]["18"] = "UE_IP_ADDRESS_ALLOCATE"
avp_values["diameter.Event-Trigger"]["19"] = "UE_IP_ADDRESS_RELEASE"
avp_values["diameter.Event-Trigger"]["20"] = "DEFAULT_EPS_BEARER_QOS_CHANGE"
avp_values["diameter.Event-Trigger"]["21"] = "AN_GW_CHANGE"
avp_values["diameter.Event-Trigger"]["22"] = "SUCCESSFUL_RESOURCE_ALLOCATION"
avp_values["diameter.Event-Trigger"]["23"] = "RESOURCE_MODIFICATION_REQUEST"
avp_values["diameter.Event-Trigger"]["24"] = "PGW_TRACE_CONTROL"
avp_values["diameter.Event-Trigger"]["25"] = "UE_TIME_ZONE_CHANGE"

class EventTrigger:
    SGSN_CHANGE = 0
    QOS_CHANGE = 1
    RAT_CHANGE = 2
    TFT_CHANGE = 3
    PLMN_CHANGE = 4
    LOSS_OF_BEARER = 5
    RECOVERY_OF_BEARER = 6
    IP_CAN_CHANGE = 7
    QOS_CHANGE_EXCEEDING_AUTHORIZATION = 11
    RAI_CHANGE = 12
    USER_LOCATION_CHANGE = 13
    NO_EVENT_TRIGGERS = 14
    OUT_OF_CREDIT = 15
    REALLOCATION_OF_CREDIT = 16
    REVALIDATION_TIMEOUT = 17
    UE_IP_ADDRESS_ALLOCATE = 18
    UE_IP_ADDRESS_RELEASE = 19
    DEFAULT_EPS_BEARER_QOS_CHANGE = 20
    AN_GW_CHANGE = 21
    SUCCESSFUL_RESOURCE_ALLOCATION = 22
    RESOURCE_MODIFICATION_REQUEST = 23
    PGW_TRACE_CONTROL = 24
    UE_TIME_ZONE_CHANGE = 25