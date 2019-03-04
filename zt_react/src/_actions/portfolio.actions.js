import * as d3 from 'd3';
import { portfolioConstants } from '../_constants';
import { portfolioService } from '../_services';
import { handleErrors } from '../_helpers';
import moment from 'moment';


function create(file, remarks) {
  function request() { return { type: portfolioConstants.CREATE_REQUEST }; }
  function success(portfolio) { return { type: portfolioConstants.CREATE_SUCCESS, portfolio }; }
  function failure(errors) { return { type: portfolioConstants.CREATE_FAILURE, errors }; }

  return (dispatch) => {
    dispatch(request());

    portfolioService.create(file, remarks)
      .then(
        (response) => {
          const portfolio = response.data;
          dispatch(success(portfolio));
        },
        (error) => {
          dispatch(failure(error.response.data));
          handleErrors(dispatch, error);
        },
      );
  };
}


function fetchDetail(id) {
  function request() { return { type: portfolioConstants.DETAIL_REQUEST }; }
  function success(portfolio) { return { type: portfolioConstants.DETAIL_SUCCESS, portfolio }; }
  function failure(errors) { return { type: portfolioConstants.DETAIL_FAILURE, errors }; }

  return (dispatch) => {
    dispatch(request());

    portfolioService.detail(id)
      .then(
        (response) => {
          const portfolio = response.data;
          dispatch(success(portfolio));
        },
        (error) => {
          dispatch(failure(error.response.data));
          handleErrors(dispatch, error);
        },
      );
  };
}

const fetchLoans = (code) => {
  const request = () => ({ type: portfolioConstants.LOANS_REQUEST });
  const success = loans => ({ type: portfolioConstants.LOANS_SUCCESS, loans });
  const failure = errors => ({ type: portfolioConstants.LOANS_FAILURE, errors });

  return (dispatch) => {
    dispatch(request());
    portfolioService.loans(code)
      .then(
        (response) => {
          const loans = d3.csvParse(response.data, d => (
            {
                ngr_cd: d.ngr_cd,
                cli_type: d.cli_type,
                init_date: moment(d.init_date, 'YYYY-MM-DD'),
                end_date: moment(d.end_date,'YYYY-MM-DD'),
                init_balance: +d.init_balance,
                default_interest: +d.default_interest,
                net_balance: +d.net_balance,
                real_guarantee: +d.real_guarantee,
                personal_guarantee: +d.personal_guarantee,
                other_guarantee: +d.other_guarantee,
                flag_forb: d.flag_forb,
            }
          ));
          dispatch(success(loans));
        },
        (error) => {
          dispatch(failure(error.response.data));
          handleErrors(dispatch, error);
        },
      );
  };
};

const portfolioActions = {
  create,
  fetchDetail,
  fetchLoans,
};

export default portfolioActions;
