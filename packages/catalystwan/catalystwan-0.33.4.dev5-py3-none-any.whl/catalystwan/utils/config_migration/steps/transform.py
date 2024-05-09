# Copyright 2023 Cisco Systems, Inc. and its affiliates
import logging
from typing import List, cast
from uuid import uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import TransformedParcel, TransformHeader, UX1Config, UX2Config
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import (
    MulticastBasicAttributes,
    MulticastParcel,
)
from catalystwan.utils.config_migration.converters.feature_template.parcel_factory import create_parcel_from_template

logger = logging.getLogger(__name__)


"""Artificial constants to represent the VPN template types"""
CISCO_VPN_TRANSPORT_AND_MANAGEMENT = "cisco_vpn_transport_and_management"
CISCO_VPN_SERVICE = "cisco_vpn_service"


def _merge_to_multicast(ux2: UX2Config, vpn: TransformedParcel) -> None:
    transformed_sub_parcel_list: List[TransformedParcel] = []
    for sub_parcel_uuid in vpn.header.subelements:
        for parcel in ux2.profile_parcels:
            if parcel.header.origin == sub_parcel_uuid and parcel.header.type == "routing/multicast":
                transformed_sub_parcel_list.append(parcel)

    if len(transformed_sub_parcel_list) <= 1:
        # Nothing to merge
        return

    basic = MulticastBasicAttributes()
    igmp = None
    pim = None

    for transformed_parcel in transformed_sub_parcel_list:
        # Remove the subelements from the VPN
        vpn.header.subelements.remove(transformed_parcel.header.origin)
        mp = cast(MulticastParcel, transformed_parcel.parcel)
        if mp.igmp is None and mp.pim is None:
            # If Multicast parcel has no IGMP or PIM,
            # it was converted from Multicast Feature Template
            basic = mp.basic
        elif mp.igmp is not None:
            igmp = mp.igmp
        elif mp.pim is not None:
            pim = mp.pim

    parcel_description = (
        f"Merged from: {', '.join(sorted([tp.parcel.parcel_name for tp in transformed_sub_parcel_list]))}"
    )
    new_origin_uuid = uuid4()
    transformed_parcel = TransformedParcel(
        header=TransformHeader(
            type="routing/multicast",
            origin=new_origin_uuid,
        ),
        parcel=MulticastParcel(
            parcel_name="Merged_Service_Multicast",
            parcel_description=parcel_description,
            basic=basic,
            igmp=igmp,
            pim=pim,
        ),
    )
    # Add the merged parcel uuid to the VPN
    vpn.header.subelements.add(new_origin_uuid)
    ux2.profile_parcels.append(transformed_parcel)


def merge_parcels(ux2: UX2Config) -> UX2Config:
    """There is inconsitency between Feature Templates and Parcels.
    There is many to one relation occuring.

    For now this function covers Feature Template merges:
    -  Multicast, PIM, IGMP -> Parcel Multicast (Subelements of VPN Service parcel)
    """

    vpns = [
        parcel
        for parcel in ux2.profile_parcels
        if parcel.header.type == "lan/vpn" and len(parcel.header.subelements) > 0
    ]
    for vpn in vpns:
        _merge_to_multicast(ux2, vpn)
    return ux2


def resolve_template_type(template: GeneralTemplate, ux1_config: UX1Config):
    for feature_template in ux1_config.templates.feature_templates:
        if feature_template.id == template.templateId:
            vpn_id = create_parcel_from_template(feature_template).vpn_id.value  # type: ignore
            if vpn_id in [0, 512]:
                template.templateType = CISCO_VPN_TRANSPORT_AND_MANAGEMENT
            else:
                template.templateType = CISCO_VPN_SERVICE
            break
        logger.debug(f"Resolved {template.name} template to type {template.templateType}")
