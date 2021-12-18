import React from "react";
import Table from "react-bootstrap/Table";
import "../css/CarOwnerTable.css";
import { useEffect, useState } from "react";
import axios from "axios";
import "../css/Global.css";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";

const ReserveTableCarOwner = () => {
  const [data, setData] = useState([]);
  const [dataPass, setDataPass] = useState([]);

  useEffect(() => {
    let token = localStorage.getItem("ctoken");
    let auth = `Token ${token}`;

    //current reserves
    axios
      .get("http://127.0.0.1:8000/carowner/reservelist/", {
        headers: {
          Authorization: auth,
        },
      })
      .then((response) => {
        console.log("فعلي ها: ", response);
        console.log(JSON.stringify(response.data));
        setData(response.data);
      });

    //passed reserves
    axios
      .get("http://127.0.0.1:8000/carowner/passedreservelist/", {
        headers: {
          Authorization: auth,
        },
      })
      .then((response) => {
        console.log("اتمام يافته ها: ", response);
        setDataPass(response.data);
      });
  }, []);

  const renderTableCurrent = () => {
    return data.map((user, index) => {
      //console.log(user);
      return (
        <tr>
          <td>{index}</td>
          <td>{user.trackingCode}</td>
          <td>{user.owner_email}</td>
          <td>{user.parking_name}</td>
          <td>{user.car_name}</td>
          <td>{user.car_color}</td>
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
          <td>{user.parking_name}</td>
          <td>{user.car_name}</td>
          <td>{user.car_color}</td>
          <td>{user.car_pelak}</td>
          <td>{user.startTime}</td>
          <td>{user.endTime}</td>
          <td>{user.cost}</td>
        </tr>
      );
    });
  };

  return (
    <div className="reserve-table">
      <div className="soheil-table">
        <div>
          <Tabs
            defaultActiveKey="current"
            transition={true}
            id="noanim-tab-example"
            className="mb-3"
          >
            <Tab eventKey="current" title="رزرو های فعلی شما">
              <Table responsive className="table-hover">
                <thead className="soheil-table-head">
                  <tr>
                    <th>ردیف</th>
                    <th>کد رهگیری</th>
                    <th>ايميل</th>
                    <th>نام پاركينگ</th>
                    <th>نام خودرو</th>
                    <th>رنگ خودرو</th>
                    <th>شماره پلاک خودرو</th>
                    <th>تاریخ و ساعت ورود</th>
                    <th>تاریخ و ساعت خروج</th>
                    <th>قیمت</th>
                  </tr>
                </thead>
                <tbody>{renderTableCurrent()}</tbody>
              </Table>
            </Tab>
            <Tab eventKey="passed" title="رزرو های گذشته شما">
              <Table responsive className="table-hover">
                <thead className="soheil-table-head">
                  <tr>
                    <th>ردیف</th>
                    <th>کد رهگیری</th>
                    <th>ايميل</th>
                    <th>نام پاركينگ</th>
                    <th>نام خودرو</th>
                    <th>رنگ خودرو</th>
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
      </div>
    </div>
  );
};

export default ReserveTableCarOwner;
