import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  origin: 'http://localhost:8000/api/v1'
});


export const getTaxa = async () => {
  // Service untuk memanggil semua daftar bakteri
  try {
    const response = await api.post(`/taxa/get`, {
      "taxon_id": []
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const getTaxonDetail = async (taxon_id) => {
  // Service untuk memanggil detail taxon
  try {
    const response = await api.get(`/taxa/detail?taxon_id=${taxon_id}`);
    // console.log("taxa data detail");
    // console.log(response.data.data.ncbi_taxon_id);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const createTaxa = async (data) => {
  // Service untuk memanggil semua daftar bakteri
  try {
    const response = await api.post(`/taxa/create`,
      [
        {
          "species": `${data.species}`,
          "ncbi_taxon_id": `${data.ncbi_taxon_id}`,
          "taxon_id": `${data.taxon_id}`
        }
      ]
    );
    // console.log("taxa data create");
    // console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const deleteTaxa = async (taxon_id) => {
  // service untuk mengambil detail dari bakteri
  try {
    const response = await api.delete(`/taxa/delete`, {
      data: { taxon_id: [taxon_id] }, // Sending the taxon_id in the body
    });
    console.log("delete response.data");
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const getPortals = async () => {
  // Service untuk memanggil semua daftar bakteri
  try {
    const response = await api.post(`/portals/get`, {
      "portal_id": []
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const getPortalDetail = async (portal_id) => {
  // Service untuk memanggil detail taxon
  try {
    const response = await api.get(`/portals/detail?portal_id=${portal_id}`);
    // console.log("taxa data detail");
    // console.log(response.data.data.ncbi_taxon_id);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const createPortal = async (portal_id) => {
  // Service untuk memanggil semua daftar bakteri
  try {
    const response = await api.post(`/portals/create`,
      [
        {
          "taxon_id": `${portal_id}`,
          "portal_id": `${portal_id}`,
          "web": [
            "gbif",
            "bacdive",
            "wikidata",
            "ncbi"
          ]
        }
      ]
    );
    // console.log("taxa data create");
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const deletePortal = async (portal_id) => {
  // service untuk mengambil detail dari bakteri
  try {
    const response = await api.delete(`/portals/delete`, {
      data: { portal_id: [portal_id] }, // Sending the taxon_id in the body
    });
    console.log("delete response.data");
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const getRaws = async (ncbi_taxon_id) => {
  // Service untuk memanggil semua daftar bakteri
  try {
    const response = await api.post(`/raws/get`, {
      "ncbi_taxon_id": [ncbi_taxon_id],
      "web": []
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const storeRaws = async (ncbi_taxon_id) => {
  // Service untuk memanggil semua daftar bakteri
  try {
    const response = await api.post(`/raws/store`, {
      "ncbi_taxon_id": [ncbi_taxon_id],
      "web": [
        "wikidata",
        "ncbi",
        "bacdive",
        "gbif"
      ]
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const deleteRaws = async (ncbi_taxon_id) => {
  // service untuk mengambil detail dari bakteri
  try {
    const response = await api.delete(`/raws/delete`, {
      data: {
        ncbi_taxon_id: [ncbi_taxon_id],
        web: [
          "gbif",
          "bacdive",
          "wikidata",
          "ncbi"
        ]
      }, // Sending the taxon_id in the body
    });
    console.log("delete response.data");
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const getTerms = async (ncbi_taxon_id) => {
  // service untuk mengambil detail dari bakteri
  try {
    const response = await api.post(`/terms/get`, {
      "ncbi_taxon_id": [`${ncbi_taxon_id}`]
    });
    // console.log("data", response.data);
    return response.data.data[0];
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const storeTerms = async (ncbi_taxon_id) => {
  try {
    const response = await api.post(`/terms/create`, {
      "ncbi_taxon_id": [`${ncbi_taxon_id}`]
    });
    // console.log("data", response.data);
    return response.data.data[0];
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const deleteTerms = async (ncbi_taxon_id) => {
  // service untuk mengambil detail dari bakteri
  try {
    const response = await api.delete(`/terms/delete`, {
      data: {
        ncbi_taxon_id: [ncbi_taxon_id]
      }, // Sending the taxon_id in the body
    });
    console.log("delete response.data");
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export const postSearch = async (keyword) => {
  // service search
  try {
    const response = await api.post(`/terms/search`, {
      "search": `${keyword}`
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export default api;
