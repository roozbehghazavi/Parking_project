import '.././index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import SignupForm from '../components/SignupForm';

const SignupPage = () => {
  return (
    <div className="container-login100">
      <div className="wrap-login100 p-l-55 p-r-55 p-t-80 p-b-30">
        <SignupForm />
      </div>
    </div>
  );
};

export default SignupPage;
