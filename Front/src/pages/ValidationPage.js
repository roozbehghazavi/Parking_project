import '../css/Validation.css';
import {
  nationalCodeValidation,
  postalCodeValidation,
} from '../functions/validationfun';
import { useState } from 'react';
import mySwal from 'sweetalert';
import { ParkingValidation } from '../api/validationApi';
import { useHistory } from 'react-router';
import { useEffect } from 'react';
const Validation = () => {
  const history = useHistory();
  const [nationalCode, setnationalCode] = useState('');
  const [submitvalue, setSubmitvalue] = useState();
  const [location, setLocation] = useState();
  const [postalCode, setpostalCode] = useState('');
  const [validationCode, setvalidationCode] = useState(1);
  const [validationFiles, setValidationFiles] = useState(null);
  const handlenationalCode = (e) => {
    setnationalCode(e.target.value);
  };
  const handleFile = (e) => {
    setValidationFiles(e.target.value);
  };
  const handelvalidationCode = (e) => {
    setvalidationCode(parseInt(e.target.value));
  };
  const handelpostalCode = (e) => {
    setpostalCode(e.target.value);
  };
  let ParkingId = localStorage.getItem('pID');
  let token = localStorage.getItem('ptoken');
  let auth = `Token ${token}`;
  const fd2 = new FormData();
  fd2.append('id', ParkingId);
  useEffect(() => {
    fetch('http://127.0.0.1:8000/parkingowner/parkingdetail/', {
      method: 'POST',
      headers: {
        Authorization: auth,
      },
      body: fd2,
    })
      .then(function (Response) {
        // setParkingdetail(Response.results)
        return Response.json();
      })
      .then(function (data) {
        // console.log(ParkingId)
        console.log(data.location);
        console.log(data.validationStatus);
        setLocation(data.location);
        setSubmitvalue(data.validationStatus);
      });
  });
  const handleMySubmit = (e) => {
    if (
      postalCodeValidation(nationalCode) === false ||
      nationalCodeValidation(postalCode) === false
    ) {
      mySwal({
        title: '!خطا',
        text: 'اطلاعات وارد شده اشتباه است',
        buttons: 'بستن',
      });
      return;
    } else {
      mySwal({
        title: 'رواله',
        text: '',
        buttons: 'بستن',
      });
      let token = localStorage.getItem('ptoken');
      let auth = `Token ${token}`;
      const fd = new FormData();
      fd.append('id', ParkingId);
      fd.append('nationalCode', nationalCode);
      fd.append('validationCode', validationCode);
      fd.append('postalCode', postalCode);
      fd.append('validationFiles', validationFiles);
      fetch(ParkingValidation.url, {
        method: 'POST',
        headers: {
          Authorization: auth,
        },
        body: fd,
      })
        .then((res) => {
          console.log(res);
          if (res.ok) {
            return res.json();
          }
          throw res;
        })
        .then((data) => {
          console.log('everything was ok!');
          console.log(data.validationStatus);
          history.push('/Panel');
        })
        .catch((error) => {
          console.log(error);
          mySwal({
            title: '!خطا',
            text: 'اطلاعات وارد شده اشتباه است',
            buttons: 'بستن',
          });
          return;
        });
    }
  };
  return (
    <div class=" position-absolute top-50 start-45 translate-middle">
      <div class="wrapper">
        <div class="cardvalidation card-2-narges">
          <div class="card-heading-validation-narges"></div>
          <div class="card-body-validation-narges">
            <h2 class="title">احراز هویت</h2>
            <form>
              <div class=" m-2">
                <label for="validationCustom01" class="form-label">
                  کد ملی{' '}
                </label>
                <input
                  type="text"
                  className="input-validation-narges"
                  class="form-control"
                  onChange={(e) => handlenationalCode(e)}
                  required
                />
                <div class="valid-feedback">Looks good!</div>
              </div>
              <div class="m-2">
                <label for="validationCustom02" class="form-label">
                  کد پستی
                </label>
                <input
                  type="text"
                  class="form-control"
                  onChange={(e) => handelpostalCode(e)}
                  required
                />
                <div class="valid-feedback">Looks good!</div>
              </div>
              <div class="m-2">
                <label for="validationCustom01" class="form-label">
                  کد جواز کسب
                </label>
                <input
                  type="text"
                  class="form-control"
                  onChange={(e) => handelvalidationCode(e)}
                  required
                />
                <div class="valid-feedback">Looks good!</div>
              </div>
              <div class="m-2">
                <label for="staticEmail" class="col-sm-2 col-form-label">
                  آدرس:
                </label>
                <div class="">
                  <input
                    type="text"
                    readonly
                    class="form-control-plaintext"
                    value={location}
                    style={{ fontFamily: 'iransans' }}
                  />
                </div>
                <div class="invalid-feedback">Please provide a valid city.</div>
              </div>
              <div class="m-2">
                <label for="formFile" class="form-label">
                  فایل مستند را اینجا اپلود کنید
                </label>
                <input
                  class="form-control"
                  onChange={(e) => handleFile(e)}
                  type="file"
                  id="formFile"
                />
              </div>
              <div class="col-12">
                {
                  submitvalue === 'V' ? (
                    <button class="nargesbt3nvalidation m-3" onClick={false}>
                      اطلاعات ثبت شد
                    </button>
                  ) : submitvalue === 'I' ? (
                    <button
                      class="nargesbt4nvalidation m-3"
                      onClick={handleMySubmit}
                      type="submit"
                    >
                      ثبت اطلاعات
                    </button>
                  ) : (
                    <button
                      class="nargesbt2nvalidation m-3"
                      onClick={false}
                      type="submit"
                    >
                      در حال ثبت اطلاعات
                    </button>
                  )
                  // <button class="nargesbt5nvalidation m-3" onClick={false} type="submit">در حال ثبت اطلاعات</button>
                }
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Validation;
