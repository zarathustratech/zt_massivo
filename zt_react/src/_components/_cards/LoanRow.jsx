import React from 'react';
import 'icheck/skins/all.css';
import {Checkbox, Radio} from 'react-icheck';
import ProgressCircleCell from './ProgressCircleCell.jsx';
import CurrencyCell from './CurrencyCell.jsx'

const LoanRow = (props) => {
  const { loan } = props;
  let prediction_mark;
  if (loan.prediction=='0'){
      prediction_mark = <Checkbox checkboxClass="icheckbox_square-green" increaseArea="20%" checked='True' />
  }

  if (loan.prediction=='1'){
      prediction_mark = <Radio name="aa" radioClass="iradio_square-red" increaseArea="20%" checked='True' />
  }

  let status_mark;
  if (loan.status=='0'){
      status_mark = <Checkbox checkboxClass="icheckbox_square-green" increaseArea="20%" checked='True' />
  }

  if (loan.status=='1'){
      status_mark = <Radio name="aa" radioClass="iradio_square-red" increaseArea="20%" checked='True' />
  }

  return (
    <tr>
        <td className="text-center">{loan.ngr_cd}</td>
        <td className="text-center">{status_mark}</td>
        <td className="text-center">{loan.num_events}</td>
        <CurrencyCell ammount={loan.im_acc_cassa}/>
        <CurrencyCell ammount={loan.im_util_cassa}/>
        <ProgressCircleCell percentage={loan.util_rate} />
        <td className="text-center">{prediction_mark}</td>
    </tr>
  );
};

export default LoanRow;
