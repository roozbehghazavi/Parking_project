import "../css/Global.css";
import "../css/ManageCapacity.css";
import axios from "axios";
import mySwal from "sweetalert";

const ManageCapacity = () => {
  const handelExitButton = () => {
    let ParkingId = localStorage.getItem("pID");
    let token = localStorage.getItem("ptoken");
    let auth = `Token ${token}`;
    let fd = new FormData();
    console.log("adsdff", ParkingId);
    console.log("token", auth);
    fd.append("parkingId", ParkingId);
    fd.append("status", "exit");

    const article = {
      headers: { authorization: auth },
      body: fd,
    };
    axios
      .put("https://reqres.in/api/articles/1", article)
      .then((response) => console.log("ress", response));
  };

  const handelEnterButton = () => {
    let ParkingId = localStorage.getItem("pID");
    let token = localStorage.getItem("ptoken");
    let auth = `Token ${token}`;
    let fd = new FormData();
    console.log("adsdff", ParkingId);
    console.log("token", auth);
    fd.append("parkingId", ParkingId);
    fd.append("status", "enter");

    const article = {
      headers: { authorization: auth },
      body: fd,
    };
    axios
      .put("https://reqres.in/api/articles/1", article)
      .then((response) => console.log("ress", response));
  };
  return (
    <div className="containerButtonGlobal">
      <button className="ButtonGlobal" onClick={handelEnterButton}>
        Enter
      </button>
      <button className="ButtonGlobal" onClick={handelExitButton}>
        Exit
      </button>
    </div>
  );
};
export default ManageCapacity;
