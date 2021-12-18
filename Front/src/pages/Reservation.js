import React from 'react';
import moment from 'moment';
import jMoment from 'moment-jalaali';
import './../css/Reserve/Reservation.css';
import './../css/Global.css';
import { useState, useEffect } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import JalaliUtils from '@date-io/jalaali';
import {
  TimePicker,
  DateTimePicker,
  DatePicker,
  MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import { Typography } from '@mui/material';
import StarIcon from '@mui/icons-material/Star';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Box from '@mui/material/Box';
import axios from 'axios';
import Comments from '../components/Comments';

jMoment.loadPersian({ dialect: 'persian-modern', usePersianDigits: true });

const persianNumbers = [
  /۰/g,
  /۱/g,
  /۲/g,
  /۳/g,
  /۴/g,
  /۵/g,
  /۶/g,
  /۷/g,
  /۸/g,
  /۹/g,
];
const arabicNumbers = [
  /٠/g,
  /١/g,
  /٢/g,
  /٣/g,
  /٤/g,
  /٥/g,
  /٦/g,
  /٧/g,
  /٨/g,
  /٩/g,
];

const fixNumbers = function (str) {
  if (typeof str === 'string') {
    for (var i = 0; i < 10; i++) {
      str = str.replace(persianNumbers[i], i).replace(arabicNumbers[i], i);
    }
  }
  return str;
};

const Reservation = () => {
  const histo = useHistory();
  const location = useLocation();
  const [image, setImage] = useState();
  // const [totalCost, setTotalCost] = useState(null);
  const [enter, handleEnterChange] = useState(moment());
  const [exit, handleExitChange] = useState(moment());
  const [car, setCar] = useState(0);
  const [cars, setCars] = useState([]);
  const [resData, setResData] = useState(null);

  const handleCarChange = (e) => {
    setCar(e.target.value);
  };

  let token = localStorage.getItem('ctoken');
  let auth = `Token ${token}`;
  ///////////////////////////////////////////////
  useEffect(() => {
    axios
      .get('http://127.0.0.1:8000/carowner/carlist/', {
        headers: { 'Content-Type': 'application/json', Authorization: auth },
      })
      .then((res) => {
        //console.log(res.data.results);
        setCars(res.data.results);
        //console.log(cars);
      })
      .catch((e) => {
        console.log('error occured in fetch');
      });
  }, []);
  //////////////////////////////////////////////
  const handleSubmitButton = (e) => {
    const enEnter = fixNumbers(enter.format('YYYY/MM/DD hh:mm:ss'));
    const enExit = fixNumbers(exit.format('YYYY/MM/DD hh:mm:ss'));
    const info = {
      parking_id: location.state.id,
      enter: enEnter,
      exit: enExit,
      car_id: car,
    };
    console.log(info);
    axios
      .post('http://localhost:8000/carowner/reserve/', info, {
        headers: { 'Content-Type': 'application/json', Authorization: auth },
      })
      .then((res) => {
        console.log(res.data);
        setResData(res.data);
      })
      .catch((e) => {
        console.log('Error', e);
      });
  };
  return (
    <div className="reservation px-sm-5 pt-4 pb-4">
      <div className="resimgcontain py-5">
        <img
          src={location.state.image}
          alt="parking image"
          style={{ width: '90%', maxHeight: '30vh', borderRadius: '5px' }}
        />
      </div>

      <div className="mt-3 rinfosect py-2">
        <div className="d-flex justify-content-center">
          <Typography variant="h3">{location.state.parkingName}</Typography>
        </div>
      </div>
      <div className="mt-3 rinfosect">
        <div className="d-flex justify-content-around">
          {' '}
          <Typography variant="h5" className="mx-4">
            امتیاز :
          </Typography>
          <Typography variant="h5" className="mx-4">
            <StarIcon color="warning" fontSize="large" />
            {location.state.rating}
          </Typography>
        </div>
      </div>
      <div className="mt-1 rinfosect">
        <div className="d-flex justify-content-around">
          <Typography variant="h5" className="mx-4">
            ظرفیت :{' '}
          </Typography>
          <Typography variant="h5" className="mx-4">
            {location.state.capacity}
          </Typography>
        </div>
      </div>
      <div className="mt-1 rinfosect">
        <div className="d-flex justify-content-around">
          <Typography variant="h5" className="mx-4">
            تلفن :
          </Typography>
          <Typography
            style={{ wordWrap: 'break-word' }}
            variant="h5"
            className=""
          >
            {location.state.number}
          </Typography>
        </div>
      </div>
      <div className="mt-1 rinfosect">
        <div className="d-flex justify-content-around">
          <Typography variant="h5" className="me-4">
            آدرس :
          </Typography>
          <Typography
            style={{ wordWrap: 'break-word' }}
            variant="body1"
            className=""
          >
            {location.state.location}
          </Typography>
        </div>
      </div>

      <div className="mt-1 rinfosect">
        <div className="d-flex justify-content-around">
          <Typography variant="h5" className="mx-4">
            هزینه به ازای هر ساعت :
          </Typography>
          <Typography
            style={{ wordWrap: 'break-word' }}
            variant="h5"
            className=""
          >
            {location.state.pricePerHour}
          </Typography>
        </div>
      </div>
      <Comments />
      <MuiPickersUtilsProvider utils={JalaliUtils} locale="fa">
        <div className="mt-5 rselectsect py-4">
          <div className="d-flex justify-content-around">
            <Typography variant="h5" className="mx-4">
              انتخاب تاریخ و ساعت ورود :
            </Typography>
            <Typography
              style={{ wordWrap: 'break-word' }}
              variant="h5"
              className=""
            >
              <DateTimePicker
                okLabel="تأیید"
                cancelLabel="لغو"
                labelFunc={(date) =>
                  date ? date.format('YYYY/MM/DD hh:mm:ss') : ''
                }
                value={enter}
                onChange={handleEnterChange}
                disablePast
              />
            </Typography>
          </div>
        </div>
        <div className="mt-5 rselectsect py-4">
          <div className="d-flex justify-content-around">
            <Typography variant="h5" className="mx-4">
              انتخاب تاریخ و ساعت خروج :
            </Typography>
            <Typography
              style={{ wordWrap: 'break-word' }}
              variant="h5"
              className=""
            >
              <DateTimePicker
                okLabel="تأیید"
                cancelLabel="لغو"
                labelFunc={(date) =>
                  date ? date.format('YYYY/MM/DD hh:mm:ss') : ''
                }
                value={exit}
                onChange={handleExitChange}
                minutesStep={30}
                disablePast
              />
            </Typography>
          </div>
        </div>
      </MuiPickersUtilsProvider>
      <div className="mt-5 rselectsect py-4">
        <div className="d-flex justify-content-around">
          <Box sx={{ minWidth: 200 }}>
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">خودرو</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={car}
                label="Age"
                onChange={(e) => handleCarChange(e)}
              >
                {cars.map((car) => {
                  return <MenuItem value={car.id}>{car.carName}</MenuItem>;
                })}
                {/* <MenuItem value={10}>Ten</MenuItem>
                <MenuItem value={20}>Twenty</MenuItem>
                <MenuItem value={30}>Thirty</MenuItem> */}
              </Select>
            </FormControl>
          </Box>
        </div>
      </div>
      {resData ? (
        <div className="mt-3 rinfosect py-5">
          <div className="d-flex justify-content-around">
            <Typography variant="body1">
              رزرو شما با موفقیت انجام شد. هزینه رزرو :{' '}
            </Typography>
            <Typography>{resData.cost} تومان</Typography>
          </div>
        </div>
      ) : null}
      <div className="mt-3 rselectsect py-5">
        <div className="d-flex justify-content-around">
          <button
            onClick={handleSubmitButton}
            className="ButtonGlobal mt-auto "
          >
            رزرو!
          </button>
          <button
            onClick={(e) => {
              histo.push('/UserPannel');
            }}
            className="ButtonGlobal mt-auto "
          >
            بازگشت به صفحه اصلی
          </button>
        </div>
      </div>
    </div>
  );
};

export default Reservation;
