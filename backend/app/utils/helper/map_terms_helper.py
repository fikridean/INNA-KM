async def mapping(params: list) -> dict:
    try:
        combined_data = {}
        
        for item in params:
            match item['web']:
                case 'ncbi':
                    if item['data'].get('Lineage') and item['data'].get('LineageEx'):
                        combined_data["Name and taxonomic classification"] = {
                            "Lineage": item['data']['Lineage'],
                            "LineageEx": item['data']['LineageEx'],
                        }
                
                case 'bacdive':
                    if item['data'].get('Morphology'):
                        combined_data["Morphology"] = item['data']['Morphology']

                    if item['data'].get('Culture and growth conditions'):
                        combined_data["Culture and growth conditions"] = item['data']['Culture and growth conditions']
                        
                    if item['data'].get('Physiology and metabolism'):
                        combined_data["Physiology and metabolism"] = item['data']['Physiology and metabolism']
                        
                    if item['data'].get('Isolation, sampling and environmental information'):
                        combined_data["Isolation, sampling and environmental information"] = item['data']['Isolation, sampling and environmental information']
                        
                    if item['data'].get('Safety information'):
                        combined_data["Safety information"] = item['data']['Safety information']
                    
                    if item['data'].get('Sequence information'):
                        combined_data["Sequence information"] = item['data']['Sequence information']

                    if item['data'].get('Genome-based predictions'):    
                        combined_data["Genome-based predictions"] = item['data']['Genome-based predictions']
                
                case 'gbif':
                    if item.get('data'):
                        combined_data["Occurence (geoference records)"] = item['data']
                case _:
                    pass

        data = {
            "taxon_id": params[0]['taxon_id'],
            "species": params[0]['species'],
            "data": combined_data
        }

        return data

    except Exception as e:
        raise Exception(f"An error occurred while mapping terms: {str(e)}")