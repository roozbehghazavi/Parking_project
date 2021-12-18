import CommentForm from "./CommentForm";
import UpdateForm from "./UpdateForm";
import "../css/comment.css";
import { BsReplyFill } from "react-icons/bs";
import { BiEdit } from "react-icons/bi";
import { RiDeleteBin7Line } from "react-icons/ri";
import { CgProfile } from "react-icons/cg";
import { Accordion } from "react-bootstrap";
import ReactStars from "react-rating-stars-component";
import axios from "axios";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import "../css/Global.css";
import useFetchrate from "../hooks/useFetchRate";

const Comment = ({
  comment,
  replies,
  setActiveComment,
  activeComment,
  updateComment,
  deleteComment,
  addComment,
  parent = null,
  currentUserId,
}) => {
  // const [rate, setRate] = useState(0);
  const location = useLocation();

  let [rate] = useFetchrate(location.state.id);
  console.log("rate in comment.js: ", rate);

  //console.log(replies);
  const isEditing =
    activeComment &&
    activeComment.id === comment.id &&
    activeComment.type === "editing";
  const isReplying =
    activeComment &&
    activeComment.id === comment.id &&
    activeComment.type === "replying";
  const fiveMinutes = 300000;
  const timePassed = new Date() - new Date(comment.dateAdded) > fiveMinutes;
  const canDelete =
    currentUserId === comment.userId && replies.length === 0 && !timePassed;
  const canReply = Boolean(currentUserId);
  const canEdit = currentUserId === comment.userId && !timePassed;
  const replyId = parent ? parent : comment.id;
  const dateAdded = new Date(comment.dateAdded).toLocaleDateString();

  let rateRes = null;

  let token = localStorage.getItem("ctoken");
  let auth = `Token ${token}`;

  const article = { id: location.state.id };
  // useEffect(() => {
  //   // axios
  //   //   .get("http://127.0.0.1:8000/carowner/israted/", {
  //   //     headers: {
  //   //       Authorization: auth,
  //   //     },
  //   //     params: {
  //   //       id: location.state.id,
  //   //     },
  //   //   })
  //   //   .then((response) => {
  //   //     console.log("response israted : ", response.data.isRated);
  //   //     setRate(response.data.isRated);

  //   //     // setRate(response.data.isRated);
  //   //     console.log("asdasdasd", rate);
  //   //   })
  //   //   // .then((data) => {
  //   //   //   setRate(data.isRated);
  //   //   //   console.log("sec then", rate);
  //   //   // })
  //   //   .catch(() => {
  //   //     console.log("ERROR");
  //   //     setRate(1);
  //   //   });

  //   fetch(`http://127.0.0.1:8000/carowner/israted/?id=${location.state.id}`, {
  //     method: "GET",
  //     headers: {
  //       Authorization: auth,
  //     },
  //   })
  //     .then((response) => {
  //       if (response.ok) {
  //         return response.json();
  //       }
  //     })
  //     .then((data) => {
  //       console.log("response israted : ", data.isRated);
  //       setRate(data.isRated);
  //       console.log("rate:", rate);
  //     })
  //     .catch((e) => {
  //       console.log("error:", e);
  //     });
  // });

  // const renderRate = () => {
  //   return rate;
  // };

  return (
    <Accordion defaultActiveKey="0">
      <Accordion.Item>
        <div key={comment.id} className="comment">
          <div className="comment-right-part ">
            <Accordion.Header>
              <div className="comment-content">
                <div style={{ margin: "1px 0 0 7px" }}>
                  <CgProfile size={18} />
                </div>
                <div className="comment-author">{comment.author}</div>
                <div className="comment-date">{dateAdded}</div>

                {/* <ReactStars
                  count={5}
                  size={24}
                  activeColor="#ffd700"
                  classNames="rating-stars"
                  value={rate}
                  edit={false}
                /> */}
              </div>
            </Accordion.Header>
            <Accordion.Body>
              {!isEditing && (
                <div className="comment-text">{comment.content}</div>
              )}
              <br />

              <ReactStars
                count={5}
                size={24}
                activeColor="#ffd700"
                classNames="rating-stars"
                value={rate}
                edit={false}
              />
              {isEditing && (
                <UpdateForm
                  submitLabel="بروزرسانی"
                  hasCancelButton
                  initialText={comment.content}
                  handleSubmit={(text) => updateComment(text, comment.id)}
                  handleCancel={() => {
                    setActiveComment(null);
                  }}
                />
              )}

              <div className="comment-actions">
                {canEdit && (
                  <div
                    className="comment-action"
                    onClick={() =>
                      setActiveComment({ id: comment.id, type: "editing" })
                    }
                  >
                    <BiEdit size={18} />
                  </div>
                )}
                {canDelete && (
                  <div
                    className="comment-action"
                    onClick={() => deleteComment(comment.id)}
                  >
                    <RiDeleteBin7Line size={18} />
                  </div>
                )}
              </div>
            </Accordion.Body>
            {isReplying && (
              <UpdateForm
                submitLabel="اضافه کردن"
                handleSubmit={(text) => addComment(text, replyId)}
              />
            )}
            {replies.length > 0 && (
              <div className="replies">
                {replies.map((reply) => (
                  <Comment
                    comment={reply}
                    key={reply.id}
                    setActiveComment={setActiveComment}
                    activeComment={activeComment}
                    updateComment={updateComment}
                    deleteComment={deleteComment}
                    addComment={addComment}
                    parent={comment.id}
                    replies={[]}
                    currentUserId={currentUserId}
                    //currentUserId={localStorage.getItem("ctoken")}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </Accordion.Item>
    </Accordion>
  );
  {
    console.log(replies);
  }
};

export default Comment;
