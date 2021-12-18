import { useState, useEffect, useRef } from 'react';
import { useHistory } from 'react-router';
import mySwal from 'sweetalert';
import '.././index.css';
import '../css/form.css';
import '../css/RegisterCar.css';
import '../css/Global.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const RegisterCar = () => {
  const history = useHistory();

  //Input fields
  const [licensePlateID_2, setlicensePlateID_2] = useState();
  const [lpChar, setLPChar] = useState();
  const [lpLeft_2, setLPLeft_2] = useState();
  const [lpRight_3, setLPRight_3] = useState();

  const [carName, setCarName] = useState();
  const [carColor, setCarColor] = useState();


  //Handling the states
  const handleCarName = (e) => {
    setCarName(e.target.value);
  };

  const handleLicensePlate = (e) => {
    setlicensePlateID_2(e.target.value);
  };

  const handleCarColor = (e) => {
    setCarColor(e.target.value);
  };

  const handleLPChar = (e) => {
    setLPChar(e.target.value);
  };

  const handleLPLeft_2 = (e) => {
    setLPLeft_2(e.target.value);
  };

  const handleLPRight_3 = (e) => {
    setLPRight_3(e.target.value);
  };

  const handleMySubmit = (e) => {
    e.preventDefault();

    let token = localStorage.getItem('ctoken');
    let auth = `Token ${token}`;

    const fd = new FormData();
    const p = lpLeft_2 + lpChar + lpRight_3 + licensePlateID_2;
    fd.append('carName', carName);
    fd.append('pelak', p);
    fd.append('color', carColor);
    console.log(p);
    const formValues = { carName: carName, pelak: p, color: carColor };
    console.log(formValues);

    fetch('http://127.0.0.1:8000/carowner/carcreate/', {
      method: 'POST',
      headers: {
        Authorization: auth,
        // 'Access-Control-Allow-Origin': 'localhost:8000',
      },
      body: fd,
    })
      .then((res) => {
        if (res.ok) {
          console.log('everything was ok!');
          history.push('/UserPannel');
          return res.json();
        }
        throw res;
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
  };

  //=================================================================
  const handleAddCar = (e) => {
      e.preventDefault();

      let token = localStorage.getItem('ctoken');//ctoken: Car Owner
      let auth = `Token ${token}`;
      var myHeaders = new Headers();
      myHeaders.append("Authorization", auth);

      const p = lpLeft_2 + lpChar + lpRight_3 + licensePlateID_2;
      var formdata = new FormData();
      formdata.append("carName", carName);
      formdata.append("pelak", p);
      formdata.append("color", carColor);

      var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
      };

      fetch("http://127.0.0.1:8000/carowner/carcreate/", requestOptions)
        .then(response => response.text())
        .then(result =>{
                mySwal({
                  title: 'پیغام!',
                  text: 'خودرو با موفقیت اضافه شد',
                  buttons: 'بستن',
                });
                history.push('/UserPannel', {isRefreshed:true});
              } )
        .catch(error => console.log('error', error));
  }


//const handleAddCar = (e) =>
  // {
  //   e.preventDefault();

  //   let token = localStorage.getItem('ctoken');//ctoken: Car Owner
  //   let auth = `Token ${token}`;

  //   var myHeaders = new Headers();
  //   myHeaders.append("Authorization", auth);
  //   const p = lpLeft_2 + lpChar + lpRight_3 + licensePlateID_2;

  //   var formdata = new FormData();
  //   formdata.append("carName", carName);
  //   formdata.append("pelak", p);
  //   formdata.append("color", carColor);

  //   var requestOptions = {
  //     method: 'POST',
  //     headers: myHeaders,
  //     body: formdata,
  //     redirect: 'follow'
  //   };

  //   fetch("http://127.0.0.1:8000/carowner/carcreate/", requestOptions)
  //     .then(response => response.text())
  //     .then(result =>{
  //       mySwal({
  //         title: 'پیغام!',
  //         text: 'خودرو با موفقیت اضافه شد',
  //         buttons: 'بستن',
  //       });
  //       history.push('/UserPannel');
  //     } )
  //     .catch(error => console.log('error', error));
  // };

  //=================================================================

  return (
    <div className="c-regcar d-flex justify-content-center align-items-center ">
      <div className="two_main_cols1 bg-light d-flex flex-column flex-lg-row newAlignMent">
        <div>
          <form className="validate-form" >
            <br />
            <br />

            <h2 className="login-form-title"> افزودن خودرو</h2>
            <br />

            <div className="d-flex">
              <div
                className="wrap-input-regcar validate-input"
                style={{ width: '60%' }}
              >
                <input
                  value={carName}
                  onChange={(e) => handleCarName(e)}
                  className="input100"
                  type="text"
                  name="carName"
                  placeholder="نوع خودرو"
                />
                <span className="focus-input100"></span>
              </div>

              <div
                className=" wrap-input-regcar validate-input"
                style={{ width: '40%' }}
              >
                <input
                  value={carColor}
                  onChange={(e) => handleCarColor(e)}
                  className="input100"
                  type="text"
                  name="carColor"
                  placeholder="رنگ"
                />
                <span className="focus-input100"></span>
              </div>
            </div>
            <br />

            <h6 className="myTitle">مشخصات پلاک</h6>

            <div className="d-flex">
              <div className=" wrap-input-regcar validate-input " >
                <input
                  value={lpRight_3}
                  onChange={(e) => handleLPRight_3(e)}
                  className="input100"
                  type="text"
                  name="LPRight_3"
                  placeholder="سه رقم راست "
                />
                <span className="focus-input100"></span>
              </div>

              <div className="wrap-input-regcar validate-input ">
                <input
                  value={lpLeft_2}
                  onChange={(e) => handleLPLeft_2(e)}
                  className="input100"
                  type="text"
                  name="LPLeft_2"
                  placeholder="دو رقم چپ "
                />
                <span className="focus-input100"></span>
              </div>
            </div>

            <div className="d-flex">
              <div className=" wrap-input-regcar validate-input" style={{ width: '60%' }}>
                <input
                  value={licensePlateID_2}
                  onChange={(e) => handleLicensePlate(e)}
                  className="input100"
                  type="text"
                  name="licensePlateID_2"
                  placeholder="شناسه (دو رقم) "
                />
                <span className="focus-input100"></span>
              </div>

              <select
                className="plate_class"
                dir="rtl"
                name="LPChar"
                value={lpChar}
                onChange={(e) => handleLPChar(e)}
                style={{ width: '40%' }}
              >
                <option disabled selected>
                  حرف پلاک
                </option>
                <option value="الف">الف</option>
                <option value="ب">ب</option>
                <option value="پ">پ</option>
                <option value="ت">ت</option>
                <option value="ث">ث</option>
                <option value="ج">ج</option>
                <option value="چ">چ</option>
                <option value="ح">ح</option>
                <option value="خ">خ</option>
                <option value="د">د</option>
                <option value="ذ">ذ</option>
                <option value="ر">ر</option>
                <option value="ز">ز</option>
                <option value="ژ">ژ</option>
                <option value="س">س</option>
                <option value="َش">ش</option>
                <option value="ص">ص</option>
                <option value="ض">ض</option>
                <option value="ط">ط</option>
                <option value="ظ">ظ</option>
                <option value="ع">ع</option>
                <option value="غ">غ</option>
                <option value="ف">ف</option>
                <option value="ق">ق</option>
                <option value="ک">ک</option>
                <option value="گ">گ</option>
                <option value="ل">ل</option>
                <option value="م">م</option>
                <option value="ن">ن</option>
                <option value="و">و</option>
                <option value="ه">ه</option>
                <option value="ی">ی</option>
              </select>
            </div>

            <div className="containerButtonGlobal">
              <button className="ButtonGlobal" onClick = {(e) => handleAddCar(e)}>ثبت خودرو</button>
            </div>
            <br />
          </form>
        </div>
      </div>
    </div>
  );
};

export default RegisterCar;
