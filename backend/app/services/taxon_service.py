from typing import List
from pymongo import UpdateOne
from models.taxon_model import (
    TaxonBaseModel,
    TaxonBaseResponseModelObject,
    TaxonDeleteModel,
    TaxonGetDetailModel,
    TaxonGetModel,
    TaxonGetResponseModelObject,
)
from utils.decorator.app_log_decorator import log_function
from database.mongo import client, taxon_collection, portal_collection
from utils.enum.message_enum import (
    ResponseMessage,
    StatusMessage,
    InfoMessage,
    SpeciesMessage,
)
from utils.enum.status_code_enum import StatusCode


# Create taxon in database
@log_function("Create taxon")
async def create_taxon(
    params: List[TaxonBaseModel],
) -> List[TaxonBaseResponseModelObject]:
    """Create taxon in database using bulk write operation."""

    # Check if the payload is empty
    if not params:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # Use a single transaction for the bulk operation
    async with await client.start_session() as session:
        async with session.start_transaction():
            bulk_ops: List[UpdateOne] = [
                UpdateOne(
                    {"taxon_id": taxon.taxon_id},
                    {
                        "$set": {
                            "taxon_id": taxon.taxon_id,
                            "ncbi_taxon_id": taxon.ncbi_taxon_id,
                            "species": taxon.species,
                        }
                    },
                    upsert=True,
                )
                for taxon in params
            ]

            # bulk write the operations
            if bulk_ops:
                await taxon_collection.bulk_write(bulk_ops, session=session)

    # prepare response
    result: List[TaxonBaseResponseModelObject] = [
        TaxonBaseResponseModelObject(
            taxon_id=taxon.taxon_id,
            ncbi_taxon_id=taxon.ncbi_taxon_id,
            species=taxon.species or SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_CREATED.value,
        )
        for taxon in params
    ]

    return result


# Get taxa from database
@log_function("Get taxa")
async def get_taxon(params: TaxonGetModel) -> List[TaxonGetResponseModelObject]:
    """Get taxa from database using taxon_id."""

    # prepare query
    taxon_id_for_query: List[str] = params.taxon_id or []

    # If taxon_id is not provided, return all taxa
    query: dict = (
        {"taxon_id": {"$in": taxon_id_for_query}} if taxon_id_for_query else {}
    )

    # Fetch taxa from database
    taxa: List[dict] = await taxon_collection.find(query, {"_id": 0}).to_list(
        length=None
    )

    # Gather found and not found taxa
    found_taxa: dict = {taxon.get("taxon_id"): taxon for taxon in taxa}
    not_found_taxa: List[str] = list(set(taxon_id_for_query) - set(found_taxa))

    # prepare response
    # Combine found and not found taxa response
    result: List[TaxonGetResponseModelObject] = [
        TaxonGetResponseModelObject(
            taxon_id=taxon.get("taxon_id"),
            ncbi_taxon_id=taxon.get("ncbi_taxon_id"),
            species=taxon.get("species") or SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_RETRIEVED.value,
        )
        for taxon in taxa
    ] + [
        TaxonGetResponseModelObject(
            taxon_id=taxon_id,
            ncbi_taxon_id=None,
            species=SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_FAILED.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}.",
        )
        for taxon_id in not_found_taxa
    ]

    return result


# Get taxon details from database
@log_function("Get taxon details")
async def get_taxon_details(params: TaxonGetDetailModel) -> TaxonGetResponseModelObject:
    """Get taxon details from database using taxon_id."""

    # prepare query
    taxon_id_for_query: str = params.taxon_id

    # If taxon_id is not provided, raise an exception
    if not taxon_id_for_query:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # fetch taxon from database
    taxon: dict = await taxon_collection.find_one(
        {"taxon_id": taxon_id_for_query}, {"_id": 0}
    )

    # prepare response
    # Return not found message if taxon not found
    if not taxon:
        return TaxonGetResponseModelObject(
            taxon_id=taxon_id_for_query,
            ncbi_taxon_id=None,
            species=SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_FAILED.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}.",
        )

    # Return taxon details if found
    return TaxonGetResponseModelObject(
        taxon_id=taxon.get("taxon_id"),
        ncbi_taxon_id=taxon.get("ncbi_taxon_id"),
        species=taxon.get("species") or SpeciesMessage.SPECIES_NOT_FOUND.value,
        status=StatusMessage.DATA_SUCCESS.value,
        info=InfoMessage.DATA_RETRIEVED.value,
    )


# Delete taxon from database
@log_function("Delete taxon")
async def delete_taxon(params: TaxonDeleteModel) -> List[TaxonBaseResponseModelObject]:
    """Delete taxon from database using taxon_id."""

    # Check if taxon_id is provided
    if not params.taxon_id:
        raise Exception(
            {
                "data": [],
                "message": ResponseMessage.INVALID_PAYLOAD_SECURITY.value,
                "status_code": StatusCode.BAD_REQUEST.value,
            }
        )

    # prepare query
    taxon_id_for_query: List[str] = params.taxon_id

    # Use a single session for both retrieval and deletion
    async with await client.start_session() as session:
        async with session.start_transaction():
            # fetch taxa from database
            taxa: List[dict] = await taxon_collection.find(
                {"taxon_id": {"$in": taxon_id_for_query}}, {"_id": 0}, session=session
            ).to_list(length=None)

            # gather found taxa
            found_taxa_ids: List[str] = {taxon["taxon_id"] for taxon in taxa}

            # Check if taxa are used in portal collection
            used_taxon: List[int] = await portal_collection.distinct(
                "taxon_id", {"taxon_id": {"$in": list(found_taxa_ids)}}, session=session
            )

            used_taxon_ids: List[str] = []
            not_used_taxon_ids: List[str] = []

            for taxon in taxa:
                # store used and not used taxa
                if taxon["taxon_id"] in used_taxon:
                    used_taxon_ids.append(taxon["taxon_id"])

                else:
                    not_used_taxon_ids.append(taxon["taxon_id"])

            # Delete taxa that are not used in portal collection
            await taxon_collection.delete_many(
                {"taxon_id": {"$in": list(found_taxa_ids - set(used_taxon_ids))}},
                session=session,
            )

    # gather not found taxa
    not_found_taxa: List[int] = list(
        set(taxon_id_for_query) - {taxon["taxon_id"] for taxon in taxa}
    )

    # prepare response
    # result for not used taxa
    result: List[TaxonBaseResponseModelObject] = (
        [
            TaxonBaseResponseModelObject(
                taxon_id=taxon["taxon_id"],
                ncbi_taxon_id=taxon.get("ncbi_taxon_id"),
                species=taxon.get("species") or SpeciesMessage.SPECIES_NOT_FOUND.value,
                status=StatusMessage.DATA_SUCCESS.value,
                info=InfoMessage.DATA_DELETED.value,
            )
            for taxon in taxa
            if taxon["taxon_id"] in not_used_taxon_ids
        ]
        + [  # result for used taxa
            TaxonBaseResponseModelObject(
                taxon_id=taxon["taxon_id"],
                ncbi_taxon_id=taxon.get("ncbi_taxon_id"),
                species=taxon.get("species") or SpeciesMessage.SPECIES_NOT_FOUND.value,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.TAXON_USED.value}",
            )
            for taxon in taxa
            if taxon["taxon_id"] in used_taxon_ids
        ]
        + [  # result for not found taxa
            TaxonBaseResponseModelObject(
                taxon_id=taxon_id,
                ncbi_taxon_id=None,
                species=SpeciesMessage.SPECIES_NOT_FOUND.value,
                status=StatusMessage.DATA_FAILED.value,
                info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.TAXON_NOT_EXIST.value}.",
            )
            for taxon_id in not_found_taxa
        ]
    )

    return result
