import '.././index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import LoginForm from '../components/LoginForm';
// import '../css/formUtill.css';
import '../css/form.css';
const LoginPage = () => {
  return (
    <div className="container-login100">
      <div className="wrap-login100 p-l-55 p-r-55 p-t-80 p-b-30">
        <LoginForm />
      </div>
    </div>
  );
};

export default LoginPage;
