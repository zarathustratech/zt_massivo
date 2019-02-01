import axios from 'axios';
import { authHeader } from '../_helpers';


const portfolioService = {
  create,
  list,
  detail,
  loans,
};

export default portfolioService;


function create(file, remarks) {
  let data = new FormData();
  data.append('file', file[0]);

  const response = axios({
    method: 'post',
    url: `${process.env.API_BASE_URL}/api/portfolios/`,
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
    data: data,
  });
  return response;
}

function list() {
  const response = axios({
    method: 'get',
    url: `${process.env.API_BASE_URL}/api/portfolios/`,
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
  });
  return response;
}

function detail(portfolioCode) {
  const response = axios({
    method: 'get',
    url: `${process.env.API_BASE_URL}/api/portfolios/${portfolioCode}/`,
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
  });
  return response;
}

function loans(portfolioCode) {
  const response = axios({
    method: 'get',
    url: `${process.env.API_BASE_URL}/api/portfolios/${portfolioCode}/loans/`,
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
  });
  return response;
}
