import { useState, useEffect } from 'react';
import CommentForm from './CommentForm';
import Comment from './Comment';
import '../css/comment.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Accordion } from 'react-bootstrap';
import '../css/Global.css';

const Comments = (props) => {
  const location = useLocation();
  const [backendComments, setBackendComments] = useState([]);
  const [activeComment, setActiveComment] = useState(null);
  const rootComments = backendComments.filter(
    (backendComment) => backendComment.parent === null
  );

  const getReplies = (commentId) => {
    const res = backendComments
      .filter((backendComment) => backendComment.parent === commentId)
      .sort(
        (a, b) =>
          new Date(a.dateAdded).getTime() - new Date(b.dateAdded).getTime()
      );
    return res;

    console.log(backendComments);
  };

  const addComment = (text, parent = null) => {
    //ok

    let token = localStorage.getItem('ctoken');
    let auth = `Token ${token}`;
    if (parent === null) {
      const body = {
        // parkingId: props.id,
        parkingId: location.state.id,
        content: text,
      };
      let fd = new FormData();
      // fd.append("parkingId", props.id);
      fd.append('parkingId', location.state.id);
      fd.append('content', text);
      fetch('http://127.0.0.1:8000/carowner/addcomment/', {
        headers: { authorization: auth },
        method: 'POST',
        body: fd,
      })
        .then((response) => response.json())
        .then((comment) => {
          let tmp = {
            id: `${comment.id}`,
            content: comment.content,
            author: comment.author,
            userId: localStorage.getItem('ctoken'),
            parent: null,
            dateAdded: comment.dateAdded,
          };

          console.log(tmp);
          setBackendComments([tmp, ...backendComments]);

          //console.log(activeComment);
          setActiveComment(null);
        });
      // } else {
      //   const body = {
      //     parent: parent,
      //     content: text,
      //   };
      //   fetch("http://127.0.0.1:8000/carowner/addreply/", {
      //     headers: { authorization: auth },
      //     method: "POST",
      //     body: JSON.stringify(body),
      //   })
      //     .then((response) => {
      //       if (response.ok) {
      //         return response.json;
      //       }
      //     })
      //     .then((comment) => {
      //       setBackendComments([comment, ...backendComments]);
      //       setActiveComment({ userId: localStorage.getItem("ctoken") });
      //       console.log(activeComment);
      //       setActiveComment(null);
      //     });
    }
  };

  const updateComment = (text, commentId) => {
    //OK
    let token = localStorage.getItem('ctoken');
    let auth = `Token ${token}`;
    const body = { id: commentId, content: text };
    let fd = new FormData();
    fd.append('id', commentId);
    fd.append('content', text);
    fetch('http://127.0.0.1:8000/carowner/editcomment/', {
      headers: { authorization: auth },
      method: 'PUT',
      body: fd,
    })
      .then((response) => response.json())
      .then(() => {
        const updatedBackendComments = backendComments.map((backendComment) => {
          if (backendComment.id === commentId) {
            return { ...backendComment, content: text };
          }
          return backendComment;
        });
        setBackendComments(updatedBackendComments);
        setActiveComment(null);
      });
  };
  const deleteComment = (commentId) => {
    //OK
    if (window.confirm('Are you sure you want to remove comment?')) {
      let token = localStorage.getItem('ctoken');
      let auth = `Token ${token}`;
      const body = { id: commentId };
      let fd = new FormData();
      fd.append('id', commentId);
      fetch('http://127.0.0.1:8000/carowner/deletecomment/', {
        headers: { authorization: auth },
        method: 'DELETE',
        body: fd,
      })
        .then((response) => {})
        .then(() => {
          const updatedBackendComments = backendComments.filter(
            (backendComment) => backendComment.id !== commentId
          );
          setBackendComments(updatedBackendComments);
        });
    }
  };

  useEffect(() => {
    //ok

    // const id = props.id;
    const id = location.state.id;
    // let token = localStorage.getItem("ctoken");
    // let auth = `Token ${token}`;

    // let fd = new FormData();
    // fd.append("id", id);
    // fetch(`http://127.0.0.1:8000/carowner/commentlist/`, {
    //   headers: { authorization: auth },
    //   method: "POST",
    //   body: fd,
    // })
    //   .then((response) => response.json())
    //   .then((data) => {
    //     console.log(data);
    //     setBackendComments(data);
    //   });

    let token = localStorage.getItem('ctoken');
    let auth = `Token ${token}`;

    axios
      .get('http://127.0.0.1:8000/carowner/commentlist/', {
        headers: {
          Authorization: auth,
        },
        params: {
          id: id,
        },
      })
      .then((response) => {
        console.log('response: ', response.data);
        setBackendComments(response.data);
      });
  }, []);

  return (
    <Accordion defaultActiveKey="0" style={{ margin: '10px' }}>
      <Accordion.Item
        className="accor-mmd"
        // style={{
        //   marginLeft: "5%",
        //   marginTop: "10%",
        //   marginRight: "30%",
        //   overflow: "auto",
        // }}
      >
        <div className="comments">
          <Accordion.Header style={{ marginBottom: '8%' }}>
            <h3 className="comments-title">نظرات</h3>
          </Accordion.Header>
          <Accordion.Body>
            <div className="comment-form-title"></div>
            <CommentForm submitLabel="اضافه کردن" handleSubmit={addComment} />
            <div className="comments-container">
              {rootComments.map((rootComment) => (
                <Comment
                  key={rootComment.id}
                  comment={rootComment}
                  replies={getReplies(rootComment.id)}
                  activeComment={activeComment}
                  setActiveComment={setActiveComment}
                  addComment={addComment}
                  deleteComment={deleteComment}
                  updateComment={updateComment}
                  //currentUserId={currentUserId}
                  currentUserId={localStorage.getItem('ctoken')}
                />
              ))}
            </div>
          </Accordion.Body>
        </div>
      </Accordion.Item>
    </Accordion>
  );
};

export default Comments;
