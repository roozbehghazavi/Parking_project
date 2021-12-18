import 'bootstrap/dist/css/bootstrap.min.css';
import ParkingCard from '../components/userpannel/ParkingCard';
import '../css/userpannel/userpannel.css';
import ParkingList from '../components/userpannel/ParkingList';

const UserPannel = () => {
  return (
    <div className="p-lg-5 outeruserpannel">
      <div
        className="userpannel d-flex flex-column justify-content-center align-items-end align-items-end-center"
        style={{ zIndex: '-3' }}
        >
        <ParkingList />
      </div>
    </div>
  );
};

export default UserPannel;
