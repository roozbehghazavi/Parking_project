import "../css/panel.css";
import { BsFillPersonFill } from "react-icons/bs";
import { FaCar } from "react-icons/fa";
import { FaMoneyBill } from "react-icons/fa";
import { GiEmptyHourglass } from "react-icons/gi";
import { TiTick } from "react-icons/ti";
import { useHistory } from "react-router";
const Panel = () => {
  const history = useHistory();
  const validationbuttonchange = (e) => {
    history.push("/ValidationPage", { id: "1" });
  };

  const handleMoveToEditCar = (e) => {
    history.push("/EditCar");
  };
  return (
    <div className="MainDivPanel h-100">
      <div class="container CardDivPanel position-absolute top-50 start-50 translate-middle">
        <div class="row gap-2 m-5">
          <div class="col-md-4 col-xl-3 nargescardhover">
            <div class="card nargescard order-card bg-c-white">
              <button
                class="card-block bg-c-white"
                onClick={(e) => handleMoveToEditCar(e)}
              >
                <i class="bi bi-align-bottom"></i>
                <h2>
                  <br />
                </h2>
                <TiTick size={40} color="black" className="mb-2" />
                <h6 class="m-b-20" style={{ color: "black" }}>
                  ویرایش اطلاعات{" "}
                </h6>
                <h2>
                  <br />
                </h2>
              </button>
            </div>
          </div>

          <div class="col-md-4 col-xl-3">
            <div class="card nargescard bg-c-purple order-card">
              <button class="card-block">
                <i class="bi bi-align-bottom"></i>
                <h2>
                  <br />
                </h2>
                <GiEmptyHourglass size={40} color="black" className="mb-2" />
                <h6 class="m-b-20" style={{ color: "black" }}>
                  {" "}
                  به این بخش چیزی اضافه نشده است{" "}
                </h6>
                <h2>
                  <br />
                </h2>
              </button>
            </div>
          </div>

          <div class="col-md-4 col-xl-3">
            <div class="card nargescard bg-c-purple order-card">
              <button class="card-block">
                <i class="bi bi-align-bottom"></i>
                <h2>
                  <br />
                </h2>
                <GiEmptyHourglass size={40} color="black" className="mb-2" />
                <h6 class="m-b-20" style={{ color: "black" }}>
                  {" "}
                  به این بخش چیزی اضافه نشده است{" "}
                </h6>
                <h2>
                  <br />
                </h2>
              </button>
            </div>
          </div>

          <div class="col-md-4 col-xl-3">
            <div class="card nargescard bg-c-purple order-card">
              <button class="card-block">
                <i class="bi bi-align-bottom"></i>
                <h2>
                  <br />
                </h2>
                <GiEmptyHourglass size={40} color="black" className="mb-2" />
                <h6 class="m-b-20" style={{ color: "black" }}>
                  {" "}
                  به این بخش چیزی اضافه نشده است{" "}
                </h6>
                <h2>
                  <br />
                </h2>
              </button>
            </div>
          </div>

          <div class="col-md-4 col-xl-3">
            <div class="card nargescard bg-c-purple order-card">
              <button class="card-block">
                <i class="bi bi-align-bottom"></i>
                <h2>
                  <br />
                </h2>
                <GiEmptyHourglass size={40} color="black" className="mb-2" />
                <h6 class="m-b-20" style={{ color: "black" }}>
                  {" "}
                  به این بخش چیزی اضافه نشده است{" "}
                </h6>
                <h2>
                  <br />
                </h2>
              </button>
            </div>
          </div>

          <div class="col-md-4 col-xl-3">
            <div class="card nargescard bg-c-purple order-card">
              <button class="card-block">
                <i class="bi bi-align-bottom"></i>
                <h2>
                  <br />
                </h2>
                <GiEmptyHourglass size={40} color="black" className="mb-2" />
                <h6 class="m-b-20" style={{ color: "black" }}>
                  {" "}
                  به این بخش چیزی اضافه نشده است{" "}
                </h6>
                <h2>
                  <br />
                </h2>
              </button>
            </div>
          </div>

          <div class="col-md-4 col-xl-3">
            <div class="card nargescard bg-c-purple order-card">
              <button class="card-block">
                <i class="bi bi-align-bottom"></i>
                <h2>
                  <br />
                </h2>
                <GiEmptyHourglass size={40} color="black" className="mb-2" />
                <h6 class="m-b-20" style={{ color: "black" }}>
                  {" "}
                  به این بخش چیزی اضافه نشده است{" "}
                </h6>
                <h2>
                  <br />
                </h2>
              </button>
            </div>
          </div>

          <div class="col-md-4 col-xl-3">
            <div class="card nargescard bg-c-purple order-card">
              <button class="card-block">
                <i class="bi bi-align-bottom"></i>
                <h2>
                  <br />
                </h2>
                <GiEmptyHourglass size={40} color="black" className="mb-2" />
                <h6 class="m-b-20" style={{ color: "black" }}>
                  {" "}
                  به این بخش چیزی اضافه نشده است{" "}
                </h6>
                <h2>
                  <br />
                </h2>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Panel;
