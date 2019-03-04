import React from 'react';
import 'icheck/skins/all.css';
import DateCell from './DateCell.jsx';
import {Checkbox, Radio} from 'react-icheck';
import CurrencyCell from './CurrencyCell.jsx'

const LoanRow = (props) => {
  const { loan } = props;

  let forb_mark;
  if (loan.flag_forb=='0'){
      forb_mark = <Checkbox checkboxClass="icheckbox_square-green" increaseArea="20%" checked='True' />
  }

  if (loan.flag_forb=='1'){
      forb_mark = <Radio name="aa" radioClass="iradio_square-red" increaseArea="20%" checked='True' />
  }

  return (
    <tr>
        <td className="text-center">{loan.ngr_cd}</td>
        <td className="text-center">{loan.cli_type}</td>
        <DateCell date={loan.init_date} />
        <DateCell date={loan.end_date} />
        <CurrencyCell ammount={loan.init_balance} />
        <CurrencyCell ammount={loan.default_interest} />
        <CurrencyCell ammount={loan.net_balance} />
        <CurrencyCell ammount={loan.real_guarantee} />
        <CurrencyCell ammount={loan.personal_guarantee} />
        <CurrencyCell ammount={loan.other_guarantee} />
        <td className="text-center">{forb_mark}</td>
    </tr>
  );
};

export default LoanRow;
