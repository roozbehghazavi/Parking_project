import "../css/Validation.css";
import "../css/Global.css";
import axios from "axios";
import {
  nationalCodeValidation,
  postalCodeValidation,
} from "../functions/validationfun";
import { useState } from "react";
import mySwal from "sweetalert";
import { ParkingValidation } from "../api/validationApi";
import { useHistory } from "react-router";
import { useEffect } from "react";
const Validation = () => {
  const history = useHistory();
  let ParkingLocation = localStorage.getItem("pAddress");
  const [nationalCode, setnationalCode] = useState("0");
  const [submitvalue, setSubmitvalue] = useState();
  const [location, setLocation] = useState(localStorage.getItem("pAddress"));
  const [postalCode, setpostalCode] = useState("0");
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
  let ParkingId = localStorage.getItem("pID");
  let token = localStorage.getItem("ptoken");
  let auth = `Token ${token}`;

  useEffect(()=>{
    setLocation(localStorage.getItem("pAddress"))
  },[])
  ///////////////////this is okay/////////////////////////////////////////////
  // useEffect(() => {
  //   let ParkingId = localStorage.getItem("pID");
  //   let token = localStorage.getItem("ptoken");
  //   let auth = `Token ${token}`;
  //   var axios = require("axios");
  //   var config = {
  //     method: "get",
  //     url: "http://127.0.0.1:8000/parkingowner/validation/",
  //     params: {
  //       id: ParkingId,
  //     },
  //     headers: {
  //       // 'Content-Type': 'application/json',
  //       Authorization: auth,
  //     },
  //   };
  //   axios(config)
  //     .then(function (response) {
  //       // console.log("location for this parking is :",response.data.location);
  //       setLocation(response.data.location);
  //       console.log("location", location);
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  // }, []);

  /////////////////////////////////////////////////////////////////

  // const handleMySubmit =(e)=>{
  //   console.log("here")
  //   mySwal({
  //     title: '!خطا',
  //     text: 'اطلاعات وارد شده اشتباه است',
  //     buttons: 'بستن',
  //   });

  // }

  const handelGoToPanel = (e) => {
    history.push("/Panel");
  };

  const handleMySubmit = (e) => {
    let ParkingId = localStorage.getItem("pID");
    let token = localStorage.getItem("ptoken");
    let auth = `Token ${token}`;
    const fd = new FormData();
    fd.append("id", ParkingId);
    fd.append("nationalCode", nationalCode);
    fd.append("validationCode", validationCode);
    fd.append("postalCode", postalCode);
    fd.append("validationFiles", validationFiles);

    console.log(fd);
    // console.log(fd.postalCode)
    // console.log(fd.ParkingId)
    // console.log(fd.nationalCode)
    console.log(nationalCode);

    let axiosConfig = {
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
        Authorization:auth,
      },
    };
    const body = {
      id: ParkingId,
      nationalCode: nationalCode,
      postalCode: postalCode,
      validationCode: validationCode,
      validationFiles:validationFiles
    };
    axios
      .post(`http://127.0.0.1:8000/parkingowner/validation/`, body, axiosConfig)
      .then((res) => {
        if (res.ok) {
          console.log("everything was ok!");
          // history.push("/");
          // return res.json();
        }
        throw res;
      })
      .catch((error) => {
        console.log(error);
        mySwal({
          title: "!خطا",
          text: "اطلاعات وارد شده اشتباه است",
          buttons: "بستن",
        });
        return;
      });
      // .then((res) => console.log("yeeeessss",res))
      // .catch((err) => console.log("Login: ", err));
    history.push("Panel")

    // fetch('http://127.0.0.1:8000/parkingowner/validation/',{
    //   method:'POST',
    //   headers:{
    //     Authorization:auth,
    //   },
    //   body:{
    //     id:ParkingId,
    //     nationalCode:nationalCode,
    //     postalCode:postalCode,
    //     validationCode:validationCode,
    //     // validationCode:validationCode
    //   }
    // })
    // .then(function(response){
    //   console.log("kheyli khariiiiiii")
    //   console.log("response :",response)
    // })
    // .catch(function(error){
    //   console.log("kheyli khariiiiiii222222222")
    //   console.log(error);
    // })
  };
  return (
    <div class="MainDivGlobal">
      <div class="SecondDiv position-absolute top-50 start-50 translate-middle">
        <br />
        <h2 class="title">احراز هویت</h2>
        <br />
        {/* <form */}
        {/* // onSubmit={(e) => handleMySubmit(e)} */}
        
          <div class="m-2 WarpInputGlobal mx-auto w-75 m-b-25">
            <input
              type="text"
              className="InputFieldGlobal"
              //   class="form-control"
              placeholder="کد ملی"
              onChange={(e) => handlenationalCode(e)}
              required
            />
            <div class="valid-feedback">Looks good!</div>
          </div>
          <br />

          <div class="m-2 WarpInputGlobal mx-auto w-75 m-b-25">
            <input
              type="text"
              class="InputFieldGlobal"
              placeholder="کد پستی"
              onChange={(e) => handelpostalCode(e)}
              required
            />
            <div class="valid-feedback">Looks good!</div>
          </div>
          <br />

          <div class="m-2 WarpInputGlobal  mx-auto w-75 m-b-25">
            <input
              type="text"
              class="InputFieldGlobal"
              placeholder="کد جواز کسب"
              onChange={(e) => handelvalidationCode(e)}
              required
            />
            <div class="valid-feedback">Looks good!</div>
          </div>
          <br />

          <div class="m-2 ">
            <h6>آدرس:</h6>
            <input
              type="text"
              readonly
              class="text-center"
              value={location}
              style={{ fontFamily: "iransans",background:"none" }}
            />
          </div>
          <div class="m-2  mx-auto w-75 m-b-25">
            <label class="form-label m-2  mx-auto w-75 m-b-25">
              فایل مستند را اینجا اپلود کنید
            </label>
          </div>
          <div>
            <input
              class="form-control "
              onChange={(e) => handleFile(e)}
              type="file"
              id="formFile"
            />
          </div>
          <div class="col-12 containerButtonGlobal">
            <button class="ButtonGlobal m-3" onClick={(e) => handleMySubmit(e)}>
              ثبت اطلاعات
            </button>
            <button class="ButtonGlobal m-3" onClick={handelGoToPanel}>
              بازگشت به صفحه قبل
            </button>
          </div>
        {/* </form> */}
      </div>
    </div>
  );
};
export default Validation;
