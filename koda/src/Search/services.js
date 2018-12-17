import axios from 'axios';

export function getResults(query) {
  const url = `http://localhost:9200/ics/packet/?q=${query}`;
  return axios.get(url);
};