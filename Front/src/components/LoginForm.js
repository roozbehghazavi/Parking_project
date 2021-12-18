import { Link } from "react-router-dom";
import { useState } from "react";
import {
  passwordValidation,
  validateEmail,
} from "../functions/loginValidations";
import { useHistory } from "react-router";
import mySwal from "sweetalert";

///api import///
import { loginApi } from "../api/loginApi";

const LoginForm = () => {
  const history = useHistory();
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");

  const [role, setRole] = useState("C");

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };
  const handlePass1Change = (e) => {
    setPassword1(e.target.value);
  };
  const handleMySubmit = (e) => {
    e.preventDefault();
    if (
      passwordValidation(password1) === false ||
      validateEmail(email) === false
    ) {
      mySwal({
        title: "!خطا",
        text: "اطلاعات وارد شده اشتباه است",
        buttons: "بستن",
      });
      return;
    } else {
      const info = {
        email: email,
        password: password1,
      };

      console.log(JSON.stringify(info));
      fetch(loginApi.url, {
        credentials: "omit",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // 'Access-Control-Allow-Origin': 'localhost:8000',
        },
        body: JSON.stringify(info),
      })
        .then((res) => {
          console.log(res);
          if (res.ok) {
            return res.json();
          }
          throw res;
        })
        .then((data) => {
          console.log("everything was ok!");
          console.log(data);
          setRole(data.role);

          if (data.role == "C") {
            localStorage.setItem("ctoken", data.key);
            history.push("/UserPannel");
          } else if (data.role == "P") {
            localStorage.setItem("ptoken", data.key);
            history.push("/HomeParkingOwner");
          }
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
    }
  };
  return (
    <form
      className="login100-form validate-form"
      onSubmit={(e) => handleMySubmit(e)}
    >
      <br />
      <br />

      <h2
        className="login100-form-title  p-b-5"
        style={{ marginBottom: "20px" }}
      >
        پارکش کن!
      </h2>

      <br />
      <br />
      <h2
        className="login100-form-title  p-b-5"
        style={{ marginBottom: "20px" }}
      >
        ورود
      </h2>
      <br />
      <br />

      <div className="wrap-input100 validate-input mx-auto w-75 m-t-100 m-b-20">
        <input
          value={email}
          onChange={(e) => handleEmailChange(e)}
          className="input100"
          type="text"
          name="username"
          placeholder="  ایمیل خود را وارد کنید"
        />
        <span className="focus-input100"></span>
      </div>
      <br />
      <br />

      <div className="wrap-input100 validate-input mx-auto w-75 m-b-25">
        <input
          value={password1}
          onChange={(e) => handlePass1Change(e)}
          className="input100"
          type="password"
          name="pass"
          placeholder="  رمز ورود خود را وارد کنید"
        />
        <span className="focus-input100"></span>
      </div>
      <br />

      <div className="container-login100-form-btn">
        <button className="login100-form-btn">ورود</button>
      </div>
      <br />
      <br />
      <br />

      <div className="text-center">
        <Link to="/Signup" className="txt2 hov1 h1">
          ثبت نام کنید
        </Link>
      </div>
      <br />
    </form>
  );
};

export default LoginForm;
