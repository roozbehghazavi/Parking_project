import parkingOpal from '../../images/opalParking.jpg';
import './../../css/Global.css';
import { useHistory } from 'react-router';
import StarIcon from '@mui/icons-material/Star';

const privateStr = 'خصوصی';
const publicStr = 'عمومی';
const rateStr = 'امتیاز : ';
const ParkingCard = (props) => {
  const history = useHistory();
  const handleReserveButton = () => {
    history.push('/ParkingPage', {
      id: props.parkingId,
      image: props.parkingPicture,
      capacity: props.parkingCapacity,
      rating: props.rating,
      isPrivate: props.isPrivate,
      parkingName: props.parkingName,
      number: props.number,
      location: props.location,
      pricePerHour: props.pricePerHour,
    });
  };

  return (
    <div
      className="card mahancard mb-3 mx-auto"
      style={{
        zIndex: '0',
        height: '550px',
        marginTop: '60px',
      }}
    >
      <div className="row no-gutters">
        <div className="col-6">
          <div className="card-body mahancard-body pt-5">
            <h2 className="parkingtitle">{props.parkingName}</h2>
            <div className="d-flex justify-content-start mt-4">
              <h3 style={{ fontSize: '18px' }}>آدرس: </h3>
              <p
                className="display-4"
                style={{ fontSize: '14px', overflowWrap: 'break-word' }}
              >
                {props.location}
              </p>
            </div>
            <br />
            <div className="d-flex justify-content-start">
              <h3 style={{ fontSize: '18px' }}>ظرفیت : </h3>
              <p style={{ fontSize: '16px' }}>{props.parkingCapacity}</p>
            </div>
            <div className="d-flex justify-content-start mt-1">
              <h3 style={{ fontSize: '18px' }}>تلفن : </h3>
              <p style={{ fontSize: '16px' }}>{props.number}</p>
            </div>
            <div className="d-flex justify-content-start mt-1">
              <h3 style={{ fontSize: '18px' }}>وضعیت : </h3>
              <p style={{ fontSize: '16px' }}>
                {props.isPrivate ? privateStr : publicStr}
              </p>
            </div>
            <div className="d-flex justify-content-center mt-3">
              <h3 style={{ fontSize: '22px' }}>{rateStr}</h3>
              <p style={{ fontSize: '20px' }}>
                <StarIcon color="warning" fontSize="small" />
                {props.rating}
              </p>
            </div>
          </div>
          <div className="col-6 position-absolute bottom-0 d-flex justify-content-center mb-2">
            <button
              onClick={handleReserveButton}
              className="ButtonGlobal mt-auto "
            >
              رزرو کنید
            </button>
          </div>
        </div>
        <div className="class col-6 p-3">
          <img
            src={props.parkingPicture}
            className="mt-2 me-2"
            style={{ maxWidth: '75vw', height: '550px' }}
          />
        </div>
      </div>
    </div>
  );
};

export default ParkingCard;
