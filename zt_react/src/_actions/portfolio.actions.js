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
                status: d.status,
                num_events: d.num_events,
                prediction: d.prediction,
                confidence_score: d.confidence_score,
                im_acc_cassa: d.im_acc_cassa,
                im_util_cassa: d.im_util_cassa,
                util_rate: d.util_rate,
                latitude: +d.latitude,
                longitude: +d.longitude,
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
