import { useState, useEffect } from 'react';
import useFetchParking from '../../hooks/useFetchParking';
import ParkingCard from './ParkingCard';
import InfiniteScroll from 'react-infinite-scroll-component';
import { apiParkingList } from '../../api/apiList';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css';
import Loader from 'react-loader-spinner';

const ParkingList = () => {
  const [link, setLink] = useState(apiParkingList);
  const [page, setPage] = useState(1);

  const [parkings, hasMore] = useFetchParking(page);

  return (
    <InfiniteScroll
      dataLength={page * 6} // deghat inja manzooresh ine ke be ezaye har chand page i ke load mishe kollan chandta
      //data bayad namayesh dade beshe
      next={() => {
        setPage(page + 1);
      }}
      hasMore={hasMore}
      loader={
        <Loader
          type="Oval"
          color="#bd59d4"
          height={50}
          width={50}
          timeout={3000}
        />
      }
      style={{ zIndex: '-2', marginTop: '10px' }}
    >
      {parkings.map((parking) => (
        <ParkingCard
          parkingName={parking.parkingName}
          location={parking.location}
          parkingPicture={parking.parkingPicture}
          parkingId={parking.id}
          parkingCapacity={parking.capacity}
          number={parking.parkingPhoneNumber}
          rating={parking.rating}
          isPrivate={parking.isPrivate}
          pricePerHour={parking.pricePerHour}
        />
      ))}
    </InfiniteScroll>
  );
};

export default ParkingList;
