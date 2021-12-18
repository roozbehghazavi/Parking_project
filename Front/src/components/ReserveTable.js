import React from "react";
import Table from "react-bootstrap/Table";
import "../css/table.css";
import { useEffect, useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import "../css/Global.css";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import mySwal from "sweetalert";

const ReserveTable = () => {
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
      // .then((response) => console.log("ress", response));
      .then(function (response) {
        console.log(response);
        mySwal({
          title: "موفق",
          text: "ظرفیت پارکینگ افزایش یافت",
          buttons: "بستن",
        });
      });
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
      // .then((response) => console.log("ress", response));
      .then(function (response) {
        console.log(response);
        mySwal({
          title: "موفق",
          text: "ظرفیت پارکینگ کاهش یافت",
          buttons: "بستن",
        });
      });
  };

  const [data, setData] = useState([]);
  const [dataPass, setDataPass] = useState([]);

  useEffect(() => {
    const id = localStorage.getItem("pID");
    let token = localStorage.getItem("ptoken");
    let auth = `Token ${token}`;
    console.log(id);
    axios
      .get("http://127.0.0.1:8000/parkingowner/reservelist/", {
        headers: {
          Authorization: auth,
        },
        params: {
          parkingId: id,
        },
      })
      .then((response) => {
        console.log("response reserveList current: ", response.data);
        response.data.sort((a, b) => {
          return new Date(a.startTime) - new Date(b.startTime); // ascending
        });
        setData(response.data);
      });
    //give passed reserves
    axios
      .get("http://127.0.0.1:8000/parkingowner/passedreservelist/", {
        headers: {
          Authorization: auth,
        },
        params: {
          parkingId: id,
        },
      })
      .then((response) => {
        console.log("response reserveList Passed: ", response.data);
        response.data.sort((a, b) => {
          return new Date(a.startTime) - new Date(b.startTime); // ascending
        });
        setDataPass(response.data);
      });
  }, []);

  const renderTableCurrent = () => {
    return data.map((user, index) => {
      return (
        <tr>
          <td>{index}</td>
          <td>{user.trackingCode}</td>

          <td>{user.owner_email}</td>
          <td>
            {user.car_name} {user.car_color}
          </td>
          {/* <td>{user.carColor}</td> */}
          <td>{user.car_pelak}</td>
          <td>{user.startTime}</td>
          <td>{user.endTime}</td>
          <td>{user.cost}</td>
        </tr>
      );
    });
  };

  const renderTablePassed = () => {
    return dataPass.map((user, index) => {
      return (
        <tr>
          <td>{index}</td>
          <td>{user.trackingCode}</td>

          <td>{user.owner_email}</td>
          <td>
            {user.car_name} {user.car_color}
          </td>
          {/* <td>{user.carColor}</td> */}
          <td>{user.car_pelak}</td>
          <td>{user.startTime}</td>
          <td>{user.endTime}</td>
          <td>{user.cost}</td>
        </tr>
      );
    });
  };

  return (
    <div className="table-mmd ">
      <div className="containerButtonGlobal">
        <button className="ButtonGlobal m-3" onClick={handelEnterButton}>
          Enter
        </button>
        <button className="ButtonGlobal m-3" onClick={handelExitButton}>
          Exit
        </button>
        <br />
        <br />
        <br />
        <br />
        <br />
      </div>
      <div>
        <Tabs
          defaultActiveKey="current"
          transition={true}
          id="noanim-tab-example"
          className="mb-3"
        >
          <Tab eventKey="current" title="رزرو های موجود">
            {/* <div>{currentReserve()}</div> */}
            <Table responsive className="table-hover">
              <thead className="table-header-mmd">
                <tr>
                  <th>#</th>
                  <th>کد رهگیری</th>

                  <th>نام رزرو کننده</th>
                  <th>خودرو</th>
                  {/* <th>رنگ خودرو</th> */}
                  <th>شماره پلاک خودرو</th>
                  <th>تاریخ و ساعت ورود</th>
                  <th>تاریخ و ساعت خروج</th>
                  <th>قیمت</th>
                </tr>
              </thead>
              <tbody>{renderTableCurrent()}</tbody>
            </Table>
          </Tab>
          <Tab eventKey="passed" title="رزرو های گذشته">
            {/* <div>{passedReserve()}</div> */}
            <Table responsive className="table-hover">
              <thead className="table-header-mmd">
                <tr>
                  <th>#</th>
                  <th>کد رهگیری</th>

                  <th>نام رزرو کننده</th>
                  <th>خودرو</th>
                  {/* <th>رنگ خودرو</th> */}
                  <th>شماره پلاک خودرو</th>
                  <th>تاریخ و ساعت ورود</th>
                  <th>تاریخ و ساعت خروج</th>
                  <th>قیمت</th>
                </tr>
              </thead>
              <tbody>{renderTablePassed()}</tbody>
            </Table>
          </Tab>
        </Tabs>
      </div>
      {/* <div>{currentReserve()}</div> */}
    </div>
  );
};

export default ReserveTable;
