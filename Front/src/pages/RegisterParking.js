import { useState, useEffect, useRef } from "react";
import { useHistory } from "react-router";
import mySwal from "sweetalert";
import "../css/form.css";
import "../css/RegisterCar.css";
import "../css/RegisterParking.css";
import ".././index.css";
import "../css/Global.css";
import "bootstrap/dist/css/bootstrap.min.css";
import defparking from "../images/opalParking.jpg";
import { isPrivate } from "@babel/types";

const RegisterParking = () => {
  const history = useHistory();

  //Input fields
  const [parkingName, setParkingName] = useState("");
  const [parkingCapacity, setParkingCapacity] = useState();
  const [parkingAddress, setParkingAddress] = useState("");
  const [parkingPhoneNum, setParkingPhoneNum] = useState();
  const [pricePerHour, setPricePerHour] = useState();

  const [parkingImage, setParkingImage] = useState();
  const [preview, setPreview] = useState();
  const fileInputRef = useRef();

  //Checkbox for private or public parking
  const [role, setRole] = useState("C");
  const [checkbox, setCheckbox] = useState(false);


  const handleCheckboxChange = (e) => {
    setCheckbox(e.target.value);
  };

  const handleRoleChange = (e) => {
    handleCheckboxChange(e);
    if (checkbox === true) setRole("Private");
    else setRole("Public");
  };

  //Handling the states
  const handleParkingName = (e) => {
    setParkingName(e.target.value);
  };

  const handleParkingCapacity = (e) => {
    setParkingCapacity(e.target.value);
  };

  const handleParkingAddress = (e) => {
    setParkingAddress(e.target.value);
  };

  const handleParkingPhoneNum = (e) => {
    setParkingPhoneNum(e.target.value);
  };

  const handleParkingPrice = (e) => {
    setPricePerHour(e.target.value);
    console.log("مایه تیله:", e.target.value);
  };

  const handleMySubmit = (e) => {
    e.preventDefault();

    let token = localStorage.getItem("ptoken");
    let auth = `Token ${token}`;
    const fd = new FormData();
    // console.log('parkingimag:');
    // console.log(parkingImage);
    // console.log('image:');
    // const image = '/media/parkingpictures/' + parkingImage.name;
    // setParkingImage({ name: image });
    // const info = {
    //   isPrivate: checkbox,
    //   parkingName: parkingName,
    //   location: parkingAddress,
    //   parkingPhoneNumber: parkingPhoneNum,
    //   capacity: parkingCapacity,
    //   parkingPicture: parkingImage,
    // };

    if (!parkingImage) {
      console.log("عکسم", defparking);
      setParkingImage({ src: " '../images/opalParking.jpg'" });
      //formdata.append("parkingPicture", fileInput.files[0], "/path/to/file");
    }

    fd.append("isPrivate", checkbox);
    fd.append("parkingName", parkingName);
    fd.append("location", parkingAddress);
    fd.append("parkingPhoneNumber", parkingPhoneNum);
    fd.append("capacity", parkingCapacity);
    fd.append("parkingPicture", parkingImage);
    // console.log(fd.get('parkingName'));
    // for (var pair of fd.entries()) {
    //   console.log(pair[0] + ', ' + pair[1]);
    // }

    fetch("http://127.0.0.1:8000/parkingowner/createparking/", {
      method: "POST",
      headers: {
        // 'Content-Type': 'application/json',
        // 'Content-Type': 'multipart/form-data',
        Authorization: auth,
        // 'Access-Control-Allow-Origin': '*',
        // 'Access-Control-Allow-Origin': 'localhost:8000',
      },
      body: fd,
    })
      .then((res) => {
        console.log(res);
        if (res.ok) {
          console.log("everything was ok!");
          history.push("/HomeParkingOwner");
          return res.json();
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
  };

  //َAdd new parking
  const handleAddParking = (e) => {
    e.preventDefault();
    let token = localStorage.getItem("ptoken");
    let auth = `Token ${token}`;

    var axios = require("axios");
    var FormData = require("form-data");
    var fs = require("fs");
    var data = new FormData();
    data.append("isPrivate", checkbox);
    data.append("parkingName", parkingName);
    data.append("location", parkingAddress);
    data.append("parkingPhoneNumber", parkingPhoneNum);
    data.append("capacity", parkingCapacity);
    data.append("parkingPicture", parkingImage);
    data.append("pricePerHour", pricePerHour);

    var config = {
      method: "post",
      url: "http://127.0.0.1:8000/parkingowner/createparking/",
      headers: { "Content-Type": "application/json", Authorization: auth },
      data: data,
    };

    axios(config)
      .then(function (response) {
        console.log(JSON.stringify(response.data));
        history.push("/HomeParkingOwner");
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  //Upload image and preview => Note!: The image is just a preview and must be saved!
  // useEffect(() => {
  //   if (parkingImage) {
  //     const reader = new FileReader();
  //     reader.onloadend = () => {
  //       setPreview(reader.result);
  //     };
  //     reader.readAsDataURL(parkingImage);
  //   } else {
  //     setPreview(defparking);
  //   }
  // }, [parkingImage]);

  return (
    <div className="c-regpar d-flex justify-content-center align-items-center">
      <div className="two_main_cols2 bg-light  d-flex flex-column flex-lg-row newAlignMent">
        <div>
          <form className="validate-form">
            {/* onSubmit={(e) => handleMySubmit(e)} */}
            <br />
            <br />

            <h2 className="login-form-title"> افزودن پارکینگ</h2>
            <br />

            <div className="d-flex">
              <div className="wrap-input-regcar validate-input  " style={{ width: '55%' }}>
                <input
                  value={parkingName}
                  onChange={(e) => handleParkingName(e)}
                  className="input100"
                  type="text"
                  name="ParkingName"
                  placeholder="   نام پارکینگ"
                />
                <span className="focus-input100"></span>
              </div>

              <div className="wrap-input-regcar validate-input" style={{ width: '45%' }}>
                <input
                  value={parkingCapacity}
                  onChange={(e) => handleParkingCapacity(e)}
                  className="input100"
                  type="text"
                  name="ParkingCapacity"
                  placeholder="   ظرفیت"
                />
                <span className="focus-input100"></span>
                {/* <label class="form-label" for="form1Example2"></label> */}
              </div>
            </div>

            <div className="d-flex">
              <div className="wrap-input-regcar validate-input">
                <input
                  value={parkingAddress}
                  onChange={(e) => handleParkingAddress(e)}
                  className="input100"
                  type="text"
                  name="ParkingAddress"
                  placeholder="  آدرس "
                />
                <span className="focus-input100"></span>
              </div>
            </div>

            <div className="d-flex">
              <div className="wrap-input-regcar validate-input">
                <input
                  value={parkingPhoneNum}
                  onChange={(e) => handleParkingPhoneNum(e)}
                  className="input100"
                  type="text"
                  name="ParkingPhoneNum"
                  placeholder=" شماره تماس "
                />
                <span className="focus-input100"></span>
              </div>

              <div className="wrap-input-regcar validate-input">
                <input
                  value={pricePerHour}
                  onChange={(e) => handleParkingPrice(e)}
                  className="input100"
                  type="text"
                  name="pricePerHour"
                  placeholder=" قیمت "
                />
                <span className="focus-input100"></span>
              </div>
              <br />
              <br />
            </div>

            <div class="form-check form-switch mx-auto w-75">
              <input
                value={checkbox}
                onChange={(event) => {
                  if (event.target.checked === true) setCheckbox(true);
                  else setRole(false);
                }}
                class="form-check-input"
                type="checkbox"
                id="flexSwitchCheckDefault"
              />
              <label class="form-check-label" for="flexSwitchCheckDefault">
                پارکینگ خصوصی
              </label>
            </div>
            <br />

            <div className="d-flex">
              <div className="mb-4">
                <label className="mb-2" style={{ fontFamily: "iransans" }}>
                  افزودن عکس
                </label>
                <input
                  class="form-control form-control-sm"
                  type="file"
                  ref={fileInputRef}
                  accept="image/*"
                  onChange={(e) => {
                    const file = e.target.files[0];
                    console.log(e.target.files[0]);
                    setParkingImage(e.target.files[0]);
                  }}
                />
              </div>
              <br />
            </div>

            <div className="containerButtonGlobal">
              <button
                onClick={(e) => handleAddParking(e)}
                className="ButtonGlobal"
              >
                ثبت پارکینگ
              </button>
            </div>
            <br />
          </form>
        </div>
      </div>
    </div>
  );
};

export default RegisterParking;
