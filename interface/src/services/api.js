import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  origin: 'http://localhost:8000/api/v1'
});


export const getTaxa = async () => {
  // Service untuk memanggil semua daftar bakteri
  try {
    const response = await api.post(`/taxa/get`,{
      "taxon_id": []
    });
    // console.log(response.data);
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

export const postSearch = async (keyword) => {
  // service search
  try {
    const response = await api.post(`/terms/search`,{
      "search": `${keyword}`
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch user profile');
  }
};

export default api;
