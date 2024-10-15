from typing import List
from pymongo import UpdateOne
from models.taxon_model import (
    TaxonBaseModel, 
    TaxonBaseResponseModelObject, 
    TaxonDeleteModel, 
    TaxonGetDetailModel, 
    TaxonGetModel, 
    TaxonGetResponseModelObject
)
from utils.decorator.app_log_decorator import log_function
from database.mongo import client, taxon_collection, portal_collection
from utils.enum.message_enum import ResponseMessage, StatusMessage, InfoMessage, SpeciesMessage
from utils.enum.status_code_enum import StatusCode


# Create taxon in database
@log_function("Create taxon")
async def create_taxon(params: List[TaxonBaseModel]) -> List[TaxonBaseResponseModelObject]:
    if not params:
        raise Exception({
            "data": [],
            "message": ResponseMessage.INVALID_PAYLOAD.value,
            "status_code": StatusCode.BAD_REQUEST.value
        })

    # Use a single transaction for the bulk operation
    async with await client.start_session() as session:
        async with session.start_transaction():
            bulk_ops: List[UpdateOne] = [
                UpdateOne(
                    {"taxon_id": taxon.taxon_id},
                    {"$set": {
                        "taxon_id": taxon.taxon_id,
                        "ncbi_taxon_id": taxon.ncbi_taxon_id,
                        "species": taxon.species,
                    }},
                    upsert=True
                ) for taxon in params
            ]

            if bulk_ops:
                await taxon_collection.bulk_write(bulk_ops, session=session)

    # Prepare the response outside the transaction (as it doesn't require DB interaction)
    result: List[TaxonBaseResponseModelObject] = [
        TaxonBaseResponseModelObject(
            taxon_id=taxon.taxon_id,
            ncbi_taxon_id=taxon.ncbi_taxon_id,
            species=taxon.species or SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_CREATED.value
        ) for taxon in params
    ]
    
    return result

# Get taxa from database
@log_function("Get taxa")
async def get_taxon(params: TaxonGetModel) -> List[TaxonGetResponseModelObject]:
    taxon_id_for_query: List[str] = params.taxon_id or []

    query: dict = {'taxon_id': {'$in': taxon_id_for_query}} if taxon_id_for_query else {}
    
    taxa: List[dict] = await taxon_collection.find(query, {'_id': 0}).to_list(length=None)

    found_taxa: dict = {taxon.get('taxon_id'): taxon for taxon in taxa}
    not_found_taxa: List[str] = list(set(taxon_id_for_query) - set(found_taxa))

    result: List[TaxonGetResponseModelObject] = [
        TaxonGetResponseModelObject(
            taxon_id=taxon.get('taxon_id'),
            ncbi_taxon_id=taxon.get('ncbi_taxon_id'),
            species=taxon.get('species') or SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_RETRIEVED.value
        ) for taxon in taxa
    ]

    # Handle missing taxa
    result.extend(
        TaxonGetResponseModelObject(
            taxon_id=taxon_id,
            ncbi_taxon_id=None,
            species=SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_NOT_FOUND.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}."
        ) for taxon_id in not_found_taxa
    )

    return result


# Get taxon details from database
@log_function("Get taxon details")
async def get_taxon_details(params: TaxonGetDetailModel) -> TaxonGetResponseModelObject:
    taxon: dict = await taxon_collection.find_one(
        {'taxon_id': params.taxon_id},
        {'_id': 0}
    )

    if not taxon:
        return TaxonGetResponseModelObject(
            taxon_id=params.taxon_id,
            ncbi_taxon_id=None,
            species=SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_NOT_FOUND.value,
            info=f"{InfoMessage.DATA_NOT_RETRIEVED.value}: {InfoMessage.TAXON_NOT_EXIST.value}."
        )

    return TaxonGetResponseModelObject(
        taxon_id=taxon.get("taxon_id"),
        ncbi_taxon_id=taxon.get("ncbi_taxon_id"),
        species=taxon.get("species") or SpeciesMessage.SPECIES_NOT_FOUND.value,
        status=StatusMessage.DATA_SUCCESS.value,
        info=InfoMessage.DATA_RETRIEVED.value
    )

# Delete taxon from database
@log_function("Delete taxon")
async def delete_taxon(params: TaxonDeleteModel) -> List[TaxonBaseResponseModelObject]:
    taxon_id_for_query: List[str] = params.taxon_id or []

    if not taxon_id_for_query:
        raise Exception({
            "data": [],
            "message": ResponseMessage.INVALID_PAYLOAD_SECURITY.value,
            "status_code": StatusCode.BAD_REQUEST.value
        })

    # Use a single session for both retrieval and deletion
    async with await client.start_session() as session:
        async with session.start_transaction():
            # Fetch taxa and check if they are used in the portal collection
            taxa: List[dict] = await taxon_collection.find(
                {'taxon_id': {'$in': taxon_id_for_query}},
                {'_id': 0},
                session=session
            ).to_list(length=None)

            found_taxa_ids = {taxon['taxon_id'] for taxon in taxa}
            used_taxon = await portal_collection.distinct(
                'taxon_id',
                {'taxon_id': {'$in': list(found_taxa_ids)}},
                session=session
            )

            used_taxon_ids: List[str] = []
            not_used_taxon_ids: List[str] = []

            for taxon in taxa:
                if taxon['taxon_id'] in used_taxon:
                    used_taxon_ids.append(taxon['taxon_id'])

                else:
                    not_used_taxon_ids.append(taxon['taxon_id'])

            # Delete taxa that are not used in portal collection
            await taxon_collection.delete_many(
                {'taxon_id': {'$in': list(found_taxa_ids - set(used_taxon_ids))}},
                session=session
            )

    not_found_taxa = list(set(taxon_id_for_query) - {taxon['taxon_id'] for taxon in taxa})

    # result for not used taxa
    result: List[TaxonBaseResponseModelObject] = [
        TaxonBaseResponseModelObject(
            taxon_id=taxon['taxon_id'],
            ncbi_taxon_id=taxon.get('ncbi_taxon_id'),
            species=taxon.get('species') or SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_SUCCESS.value,
            info=InfoMessage.DATA_DELETED.value
        ) for taxon in taxa if taxon['taxon_id'] in not_used_taxon_ids
    ]

    # result for used taxa
    result.extend(
        TaxonBaseResponseModelObject(
            taxon_id=taxon['taxon_id'],
            ncbi_taxon_id=taxon.get('ncbi_taxon_id'),
            species=taxon.get('species') or SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_FAILED.value,
            info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.TAXON_USED.value}"
        ) for taxon in taxa if taxon['taxon_id'] in used_taxon_ids
    )

    result.extend(
        TaxonBaseResponseModelObject(
            taxon_id=taxon_id,
            ncbi_taxon_id=None,
            species=SpeciesMessage.SPECIES_NOT_FOUND.value,
            status=StatusMessage.DATA_FAILED.value,
            info=f"{InfoMessage.DATA_NOT_DELETED.value}: {InfoMessage.TAXON_NOT_EXIST.value}."
        ) for taxon_id in not_found_taxa
    )

    return result
