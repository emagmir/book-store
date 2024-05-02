/* eslint-disable default-case */
import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";

export default function Login(props) {
  const [loginForm, setLoginform] = useState({
    grant_type: "",
    username: "",
    password: "",
    scope: "",
    client_id: "",
    client_secret: ""
  });

  const onChangeForm = (label, event) => {
    switch (label) {
      case "username":
        setLoginform({ ...loginForm, username: event.target.value });
        break;
      case "password":
        setLoginform({ ...loginForm, password: event.target.value });
        break;
    }
  };

  const onSubmitHandler = async (event) => {
    event.preventDefault();
    console.log(loginForm);

    const formData = new URLSearchParams();
    Object.entries(loginForm).forEach(([key, value]) => {
      formData.append(key, value);
    });

    // call api login
    await axios
  .post("http://bookstore-be-dep:8000/auth/login", formData.toString(), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
  .then((response) => {
    console.log(response);
    // Save token to local storage
    localStorage.setItem("auth_token", response.data.access_token);
    localStorage.setItem(
      "auth_token_type",
      response.data.token_type
    );

    // add successfully notif
    toast.success(response.data.detail);
    // reload page after success login
    setTimeout(() => {
      window.location.reload();
    }, 1000);
  })
  .catch((error) => {
    // Check if error.response exists before accessing it
    if (error.response) {
      // Handle error with response from server
      console.error(error.response.data.detail);
      toast.error(error.response.data.detail);
    } else {
      // Handle unexpected error without response from server
      console.error("An unexpected error occurred:", error.message);
      // Example: Notify user about unexpected error
      toast.error("An unexpected error occurred. Please try again later.");
    }
  });
  };

  return (
    <React.Fragment>
      <div>
        <h1 className="text-3xl font-bold text-center mb-4 cursor-pointer">
          Welcome to Book store
        </h1>
        <p className="w-80 text-center text-sm mb-8 font-semibold text-gray-700 tracking-wide cursor-pointer mx-auto">
          Please login to your account!
        </p>
      </div>
      <form onSubmit={onSubmitHandler}>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-yellow-400"
            onChange={(event) => {
              onChangeForm("username", event);
            }}
          />
          <input
            type="password"
            placeholder="Password"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-yellow-400"
            onChange={(event) => {
              onChangeForm("password", event);
            }}
          />
        </div>
        <div className="text-center mt-6">
          <button
            type="submit"
            className="py-3 w-64 text-xl text-white bg-yellow-400 rounded-2xl hover:bg-yellow-300 active:bg-yellow-500 outline-none"
          >
            Sign In
          </button>
          <p className="mt-4 text-sm">
            You don't have an account?{" "}
            <Link
              to="/?register"
              onClick={() => {
                props.setPage("register");
              }}
            >
              <span className="underline cursor-pointer">Register</span>
            </Link>{" "}
            or{" "}
            <Link
              to="/?forgot"
              onClick={() => {
                props.setPage("forgot");
              }}
            >
              <span className="underline cursor-pointer">Forgot Password?</span>
            </Link>
          </p>
        </div>
      </form>
    </React.Fragment>
  );
}