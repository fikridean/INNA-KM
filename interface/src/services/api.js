import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  origin: 'http://localhost:8000/api/v1'
});


export const getMyBookings = async () => {
  try {
    // console.log(token);
    const response = await api.post(`/portals/get`,{
      "taxon_id": [],
      "web": []
    });
    // console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const getSearch = async (keyword) => {
  try {
    // console.log(token);
    const response = await api.post(`/terms/search`,{
      "search": `${keyword}`
    });
    // console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};


export const getPortalsWithWebDetail = async () => {
  try {
    // console.log(token);
    const response = await api.post(`/portals/get/web-detail`,{
      "taxon_id": [],
      "web": [
        "wikidata",
        "bacdive",
        "ncbi",
        "gbif"
      ]
    });
    // console.log(response.data);
    return response.data.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};



export const getTerms = async (taxon_id) => {
  try {
    const response = await api.post(`/terms/get`, {
      "ncbi_taxon_id": [`${taxon_id}`]
    });
    // console.log("data", response.data);
    return response.data.data[0];
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};



export const getTaxonDetail = async (taxon_id) => {
  try {
    const response = await api.get(`/taxa/detail?taxon_id=${taxon_id}`);
    // console.log(response.data.data);
    return response.data.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};


export default api;
