import ReserveTable from "../components/ReserveTable";
import "../css/parkingReserve.css";
import "../css/Global.css";
// import ManageCapacity from "../components/ManageCapacity";

const PrkingReserve = () => {
  return (
    // <div  className="p-reserve">
    <div className="reserve-po">
      <div style={{ paddingTop: "2%", paddingBottom: "0%", maxHeight: "100%" }}>
        <ReserveTable />
      </div>
    </div>
  );
};

export default PrkingReserve;
