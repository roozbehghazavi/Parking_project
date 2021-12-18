import { useState } from "react";
import "../css/comment.css";
import ReactStars from "react-rating-stars-component";
import React from "react";
import { render } from "react-dom";
import { useLocation } from "react-router-dom";
import axios from "axios";
import "../css/Global.css";
import useFetchrate from "../hooks/useFetchRate";

const CommentForm = ({
  handleSubmit,
  submitLabel,
  hasCancelButton = false,
  handleCancel,
  initialText = "",
}) => {
  const [text, setText] = useState(initialText);
  const isTextareaDisabled = text.length === 0;
  const onSubmit = (event) => {
    event.preventDefault();
    handleSubmit(text);
    setText("");
  };
  const location = useLocation();
  const ratingChanged = (newRating) => {
    console.log(newRating);

    let token = localStorage.getItem("ctoken");
    let auth = `Token ${token}`;

    const article = { id: location.state.id, value: newRating };
    axios
      .put("http://127.0.0.1:8000/carowner/addrate/", article, {
        headers: {
          Authorization: auth,
        },
      })
      .then((response) => {
        console.log("response: ", response.data.rating);
      });
  };

  let [rate] = useFetchrate(location.state.id);
  console.log("rate in commentFrom.js: ", rate);
  console.log("rate in commeasdasdadsatFrom.js: ", !Boolean(rate));

  let rated = 1;

  const isRated = () => {
    let token = localStorage.getItem("ctoken");
    let auth = `Token ${token}`;

    const article = { id: location.state.id };
    axios
      .get("http://127.0.0.1:8000/carowner/israted/", {
        headers: {
          Authorization: auth,
        },
        params: {
          id: location.state.id,
        },
      })
      .then((response) => {
        console.log("response israted : ", response.data.isRated);
        rated = response.data.isRated;
        console.log("bool", Boolean(rated));
      });
  };

  return (
    <form onSubmit={onSubmit}>
      <div class="mb-3">
        <textarea
          className="comment-form-textarea"
          placeholder="نظر خود را در مورد پارکینگ وارد کنید..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>
      <ReactStars
        count={5}
        onChange={ratingChanged}
        size={24}
        activeColor="#ffd700"
        classNames="rating-stars"
        value={2}
        edit={!Boolean(rate)}
      />
      <button className="comment-form-button" disabled={isTextareaDisabled}>
        {submitLabel}
      </button>
      {hasCancelButton && (
        <button
          type="button"
          className="comment-form-button comment-form-cancel-button"
          onClick={handleCancel}
        >
          لغو
        </button>
      )}
    </form>
  );
};

export default CommentForm;
