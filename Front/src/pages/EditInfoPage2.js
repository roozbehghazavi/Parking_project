import "../css/form.css";
import "../css/EditInfoPage.css";
import "../css/Global.css";
import { useState, useRef, useEffect } from "react";
import mySwal from "sweetalert";
import { validateEmail } from "../functions/loginValidations";
import defprof from "../images/carGif.gif";
import { useHistory } from "react-router";
import backpg from "../images/206.jpg";
import axios from "axios";

const EditInfoPage2 = () => {
  const fileSelectedHandler = (e) => {
    console.log(e);
  };
  const history = useHistory();
  const [Name, SetName] = useState("");
  const [LastName, SetLastName] = useState("");
  const [email, SetEmail] = useState("");
  const [image, setImage] = useState();
  const [preview, setPreview] = useState();
  const fileInputRef = useRef();
  const handleNameChanged = (e) => {
    SetName(e.target.value);
  };
  const handleLastNameChanged = (e) => {
    SetLastName(e.target.value);
  };
  const handleEmailChanged = (e) => {
    SetEmail(e.target.value);
  };
  useEffect(()=>{
    let token = localStorage.getItem("ctoken");
    let auth = `Token ${token}`;
    axios.get("http://127.0.0.1:8000/users/rest-auth/user/",{
      headers:{
        Authorization:auth,
      }
    })
    .then((res)=>
    {
      console.log(res.data.LastName)
      setImage(res.data.image)
      setPreview(res.data.image)
    })
    .catch((error)=>console.log(error))
  },[])
  const SubmitInfo = (e) => {
    e.preventDefault();
    if (validateEmail(email) === false) {
      mySwal({
        title: "خطا",
        text: "ایمیل وارد شده معتبر نیست",
        buttons: "بستن",
      });
      return;
    } else {
      //option 1 :
      let token = localStorage.getItem("ctoken");
      let auth = `Token ${token}`;
      const fd = new FormData();
      fd.append("firstName", Name);
      fd.append("lastName", LastName);
      fd.append("email", email);
      fd.append("image", image);
      fetch("http://127.0.0.1:8000/users/update/", {
        method: "PUT",
        headers: {
          Authorization: auth,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(fd),
      })
        .then((res) => {
          if (res.ok) {
            console.log(res)
            console.log("fetch was successfull");
            history.push("/UserPannel");
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

      //oprion 2 :
      // const info = {
      //   firstName: Name,
      //   lastName: LastName,
      //   email: email,
      // };
      // let token = localStorage.getItem('ctoken');
      // let auth = `Token ${token}`;

      // fetch('http://127.0.0.1:8000/users/update/', {
      //   credentials: 'omit',
      //   method: 'PUT',
      //   headers: {
      //     Authorization: auth,
      //     'Access-Control-Allow-Origin': '*',
      //     'Content-Type': 'application/json',
      //     // 'Access-Control-Allow-Origin': 'localhost:8000',
      //   },
      //   body: JSON.stringify(info),
      // })
      //   .then((res) => {
      //     if (res.ok) {
      //       console.log('everything was ok!');
      //       history.push('/UserPannel');
      //       return res.json();
      //     }
      //     throw res;
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //     mySwal({
      //       title: '!خطا',
      //       text: 'اطلاعات وارد شده اشتباه است',
      //       buttons: 'بستن',
      //     });
      //     return;
      //   });
    }
  };

  useEffect(() => {
    let token = localStorage.getItem("ctoken");
    let auth = `Token ${token}`;
    var axios = require("axios");
    var config = {
      method: "get",
      url: "http://127.0.0.1:8000/users/rest-auth/user/",
      headers: {
        "Content-Type": "application/json",
        Authorization: auth,
      },
    };

    axios(config)
      .then(function (response) {
        SetName(response.data.Name);
        SetName(response.data.Name);
        console.log("myInfo:", response.data.results);
      })
      .catch(function (error) {
        console.log(error);
      });
  }, []);

  const savePro = () => {
    alert("success");
    <div className="custom-file text-center">
      <input type="file" className="custom-file-input" id="customFile" />
      <label className="custom-file-label" for="customFile">
        Choose file
      </label>
    </div>;
  };
  useEffect(() => {
    if (image) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(image);
    } else {
      setPreview(null);
    }
  });
  return (
    <div className="MainDiv">
      <div className="SecondDiv shadow-lg p-3 bg-white rounded FormDiv wrapper">
        <div className="flex-container">
          <div className="image">
            {preview ? (
              <img
                src={preview}
                style={{
                  objectFit: "cover",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "18px",
                  border: "none",
                  background: "#cacaca",
                  color: "#000",
                  width: "170px",
                  height: "170px",
                  borderRadius: "50%",
                  cursor: "pointer",
                }}
                onClick={() => {
                  setImage(null);
                }}
              />
            ) : (
              <button
                src={"../images/206.jpg"}
                // src={"../images/Edit2.jpeg"}
                style={{
                  // display: 'flex',
                  // alignItems: 'center',
                  // justifyContent: 'center',
                  // fontSize: '14px',
                  // border: 'none',
                  // objectFit: 'cover',
                  // color: 'white',
                  // borderRadius: '10px',
                  // cursor: 'pointer',
                  // backgroundColor: '#bd59d4',
                  objectFit: "cover",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "18px",
                  border: "none",
                  background: "#cacaca",
                  color: "#000",
                  width: "170px",
                  height: "170px",
                  borderRadius: "50%",
                  cursor: "pointer",
                  // backgroundImage:`url(${backpg})`
                  // backgroundColor:"black",
                  // background:`url(${backpg})`
                }}
                // className="imagebutton"
                // className ="img1"
                // style ={{backgroundImage: `url(${"../images/Edit2.jpeg"})`}}
                // style ={{backgroundColor : "black"}}
                onClick={(e) => {
                  e.preventDefault();
                  fileInputRef.current.click();
                }}
              >
                انتخاب عکس
              </button>
            )}
            <input
              type="file"
              style={{ display: "none" }}
              ref={fileInputRef}
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files[0];
                if (file && file.type.substr(0, 5) === "image") {
                  setImage(file);
                  setPreview(file);
                } else {
                  setImage(null);
                  setPreview(defprof);
                }
              }}
            ></input>
          </div>
          <div className="text-center">
            {/* <p className="h1 p-3 text-center InfoTitle">پروفایل</p> */}
            {/* <p className="h3 p-4 text-left NameTitle" > نرگس مشایخی</p> */}
            {/* <input value={Name}/> */}
          </div>
        </div>

        <div class="text-center">
          <div class="InputFieldGlobal mx-auto w-75 m-b-25 m-2">
            <h2>پروفایل</h2>
          </div>
          <div class="InputFieldGlobal mx-auto w-75 m-b-25">
            <input
              value={Name}
              type="text"
              className="shadow p-2 mb-4 WarpInputGlobal"
              placeholder="نام"
              onChange={(e) => {
                SetName(e.target.value);
              }}
            />
          </div>
          <br />
          <div class="InputFieldGlobal mx-auto w-75 m-b-25">
            <input
              value={LastName}
              type="text"
              className="shadow p-2 mb-4 WarpInputGlobal"
              placeholder="نام خانوادگی "
              onChange={(e) => {
                SetLastName(e.target.value);
              }}
            />
          </div>
          <br />
          <div class="InputFieldGlobal mx-auto w-75 m-b-25">
            <input
              type="email"
              onChange={(e) => handleEmailChanged(e)}
              className="shadow p-2 mb-4 WarpInputGlobal"
              placeholder="ایمیل"
              // style={{borderRadius:"10px"}}
            />
          </div>
          <br />
          <div class="containerButtonGlobal">
            <button
              className="ButtonGlobal"
              type="submit"
              onClick={(e) => SubmitInfo(e)}
            >
              {" "}
              ثبت
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
export default EditInfoPage2;
