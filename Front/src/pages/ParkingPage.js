import { useLocation } from 'react-router';
import { useState } from 'react';
import axios from 'axios';
import { useEffect } from 'react';
const ParkingPage = () => {
  const location = useLocation();
  const [comments, setComments] = useState([]);
  useEffect(() => {
    let token = localStorage.getItem('ctoken');
    let auth = `Token ${token}`;
    // const body = { parkingId: location.state.id };
    axios
      .post('http://127.0.0.1:8000/carowner/commentlist/', {
        headers: {
          Authorization: auth,
          'Content-Type': 'application/json',
        },
        data: { id: 1 },
      })
      .then((res) => {
        console.log(res.data);
        setComments(res.data);
      });
  }, []);

  return (
    <div className="parkingpage">
      <h2>id is: bemir mamad id is:</h2>
      <h1>{location.state.id}</h1>
      <button>mahan</button>
      {comments ? (
        <div>
          {comments.map((comment) => {
            <div>3</div>;
          })}
        </div>
      ) : null}
    </div>
  );
};

export default ParkingPage;
