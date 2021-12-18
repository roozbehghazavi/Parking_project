import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import {
  passResetValidation,
  validateEmail,
} from "../functions/loginValidations";
import { useHistory } from "react-router";

import mySwal from "sweetalert";

// import '../css/formUtill.css';
import "../css/form.css";
///api///
import { register } from "../api/registerApi";

const SignupForm = () => {
  const history = useHistory();

  useEffect(() => {
    mySwal({
      title: "توجه",
      text: "اگر ارائه دهنده خدمات هستید گزینه مربوطه را روشن نمایید",
      button: "باشه",
    });
  }, []);

  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [role, setRole] = useState("C");
  const [checkbox, setCheckbox] = useState(false);
  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };
  const handlePass1Change = (e) => {
    setPassword1(e.target.value);
  };
  const handlePass2Change = (e) => {
    setPassword2(e.target.value);
  };
  const handleCheckboxChange = (e) => {
    setCheckbox(e.target.value);
  };
  const handleRoleChange = (e) => {
    handleCheckboxChange(e);
    if (checkbox === true) setRole("P");
    else setRole("C");
  };

  const handleMySubmit = (e) => {
    e.preventDefault();
    if (
      passResetValidation(password1, password2) === false ||
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
        password1: password1,
        password2: password2,
        role: role,
      };

      console.log(JSON.stringify(info));
      fetch(register.url, {
        credentials: "omit",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // 'Access-Control-Allow-Origin': 'localhost:8000',
        },
        body: JSON.stringify(info),
      })
        .then((res) => {
          if (res.ok) {
            console.log("everything was ok!");
            history.push("/");
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
        عضویت
      </h2>
      <br />
      <br />

      <div className="wrap-input100 validate-input mx-auto w-75 m-t-100 m-b-20">
        <input
          value={email}
          onChange={(e) => handleEmailChange(e)}
          className="input100"
          type="text"
          name="email"
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
          name="password1"
          placeholder="  رمز عبور خود را وارد کنید"
        />
        <span className="focus-input100"></span>
      </div>
      <br />
      <div className="wrap-input100 validate-input mx-auto w-75 m-b-25">
        <input
          value={password2}
          onChange={(e) => handlePass2Change(e)}
          className="input100"
          type="password"
          name="password2"
          placeholder="  تکرار رمز عبور"
        />
        <span className="focus-input100"></span>
      </div>
      <br />

      <div class="form-check form-switch mx-auto w-75">
        <input
          value={checkbox}
          onChange={(event) => {
            if (event.target.checked === true) setRole("P");
            else setRole("C");
          }}
          class="form-check-input"
          type="checkbox"
          id="flexSwitchCheckDefault"
        />
        <label class="form-check-label" for="flexSwitchCheckDefault">
          ثبت نام به عنوان متصدی پارکینگ
        </label>
      </div>
      <br />
      <br />

      <div className="container-login100-form-btn">
        <button className="login100-form-btn">ثبت نام</button>
      </div>
      <br />
      <br />
      <br />
      <div className="text-center">
        <Link to="/" className="txt2 hov1 h1">
          ورود
        </Link>
      </div>

      <br />
    </form>
  );
};

export default SignupForm;
