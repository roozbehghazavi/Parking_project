import { useState, useEffect, useRef } from "react";
import { useHistory } from "react-router";
import mySwal from "sweetalert";
import "../css/form.css";
import "../css/EditCar.css";
import "../css/EditParking.css";
import ".././index.css";
import "../css/Global.css";
import "bootstrap/dist/css/bootstrap.min.css";
import defparking from "../images/opalParking.jpg";

import axios from "axios";
import defParkingImg from "../images/parking.jpg"

const EditParking = () => {
  const history = useHistory();

  const id = localStorage.getItem("pID");

  //Input fields
  const [parkingName, setParkingName] = useState(localStorage.getItem("pName"));
  const [parkingCapacity, setParkingCapacity] = useState(
    localStorage.getItem("pCapacity")
  );
  const [parkingAddress, setParkingAddress] = useState(
    localStorage.getItem("pAddress")
  );
  const [parkingPhoneNum, setParkingPhoneNum] = useState(
    localStorage.getItem("pPhoneNum")
  );

  const [parkingImage, setParkingImage] = useState(
    localStorage.getItem("pImage")
  );

  const [pricePerHour, setPricePerHour] = useState(
    localStorage.getItem("pricePerHour")
  );

  const fileInputRef = useRef();

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

  const handleParkingImg = (e) => {
    const file = e.target.files[0];
    console.log(e.target.files[0]);
    setParkingImage(e.target.files[0]);
  };

  const handleParkingPrice = (e) => {
    setPricePerHour(e.target.value);
    
  };

  useEffect(() => {
    console.log("عکس اصلی:", parkingImage);
    console.log("عکس پیشفرض:", defParkingImg);
    setParkingImage(defParkingImg);
    console.log("قیمت", pricePerHour);
  }, []);

  const handleEdit = (e) => {
    e.preventDefault();
    setParkingImage(defParkingImg);
    let token = localStorage.getItem("ptoken"); //ptoken: Parking Owner
    let auth = `Token ${token}`;

    var myHeaders = new Headers();
    myHeaders.append("Authorization", auth);

    var formdata = new FormData();
    formdata.append("id", id);
    formdata.append("parkingName", parkingName);
    formdata.append("location", parkingAddress);
    formdata.append("parkingPhoneNumber", parkingPhoneNum);
    formdata.append("capacity", parkingCapacity);
    formdata.append("parkingPicture", parkingImage);
    formdata.append("pricePerHour", pricePerHour);

    var requestOptions = {
      method: "PUT",
      headers: myHeaders,
      body: formdata,
      redirect: "follow",
    };

    fetch("http://127.0.0.1:8000/parkingowner/updateparking/", requestOptions)
      .then((response) => {
        response.text();
        mySwal({
          title: "پیغام!",
          text: "پارکینگ با موفقیت ویرایش شد",
          buttons: "بستن",
        });
      })
      .then((result) => console.log("نتیجه ویرایش", result))
      .catch((error) => console.log("error", error));
  };

  //Delete button
  const handleDelete = (e) => {
    e.preventDefault();
    let token = localStorage.getItem("ptoken");
    let auth = `Token ${token}`;
    var data = JSON.stringify({
      id: id,
    });

    axios
      .delete("http://127.0.0.1:8000/parkingowner/deleteparking", {
        headers: { "Content-Type": "application/json", Authorization: auth },
        data: data,
      })
      .then((response) => {
        console.log("Parking deleted successfully!");
        console.log(response);
        mySwal({
          title: "پیغام!",
          text: "پارکینگ با موفقیت حذف شد",
          buttons: "بستن",
        });
        history.push("/HomeParkingOwner");
      })
      .catch((err) => {
        console.log("Could not delete the Parking! I'm sorry bro :( ");
        console.log("The error: ", err);
      });
  };

  //Return Button
  const handleReturn = (e) => {
    history.push("/HomeParkingOwner");
  };

  return (
    <div className="c-regpar d-flex justify-content-center align-items-center">
      <div className="two_main_cols2 bg-light  d-flex flex-column flex-lg-row newAlignMent">
        <div>
          <form className="validate-form">
            <br />
            <br />

            <h2 className="login-frm-title"> تغییر اطلاعات پارکینگ</h2>
            <br />

            <div className="d-flex">
              <div className="wrap-inpt-regcar validate-input  " style={{ width: '60%' }}>
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

              <div className="wrap-inpt-regcar validate-input" style={{ width: '40%' }}>
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
              <div className="wrap-inpt-regcar validate-input">
                <input
                  value={parkingAddress}
                  onChange={(e) => handleParkingAddress(e)}
                  className="input100"
                  type="text"
                  name="ParkingAddress"
                  placeholder="   آدرس "
                />
                <span className="focus-input100"></span>
              </div>
            </div>

            <div className="d-flex">
              <div className="wrap-inpt-regcar validate-input" style={{ width: '60%' }}>
                <input
                  value={parkingPhoneNum}
                  onChange={(e) => handleParkingPhoneNum(e)}
                  className="input100"
                  type="text"
                  name="ParkingPhoneNum"
                  placeholder="   شماره تماس "
                />
                <span className="focus-input100"></span>
              </div>

              <div className="wrap-input-regcar validate-input" style={{ width: '40%' }}>
                <input
                  value={pricePerHour}
                  onChange={(e) => handleParkingPrice(e)}
                  className="input100"
                  type="text"
                  name="pricePerHour"
                  placeholder="  قیمت"
                />
                <span className="focus-input100"></span>
              </div>
              <br />
            </div>

            <div className="d-flex">
              <div className="mb-4">
                <label className="mb-3" style={{ fontFamily: "iransans" }}>
                  تغییر عکس
                </label>
                <input
                  class="form-control form-control-sm"
                  type="file"
                  ref={fileInputRef}
                  accept="image/*"
                  onChange={(e) => {
                    handleParkingImg(e);
                  }}
                />
              </div>
              <br />
            </div>

            <div className="containerButtonGlobal">
              <button onClick={(e) => handleEdit(e)} className="ButtonGlobal">
                ذخیره تغییرات
              </button>
            </div>
            <br />
            <div className="containerButtonGlobal">
              <button
                onClick={(e) => {
                  const confirmBox = window.confirm(
                    "آیا از حذف پارکینگ اطمینان دارید؟"
                  );
                  if (confirmBox === true) {
                    handleDelete(e);
                  }
                }}
                className="ButtonGlobal"
              >
                حذف پارکینگ!
              </button>
            </div>
            <br />

            <div className="containerButtonGlobal">
              <button onClick={(e) => handleReturn(e)} className="ButtonGlobal">
                بازگشت به پنل اصلی
              </button>
            </div>
            <br />
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditParking;
