import React, { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import './Home.css'
import './bookshelf.jpg'

export default function Home() {
  const [user, setUser] = useState({});
  const [userRights, setUserRights] = useState(null);
  const [retrievals, setRetrievals] = useState([]);
  const [formData, setFormData] = useState({
    book_title: '',
    author: '',
    genre: '',
    file_id: ''
  });

  const [uploadFormData, setUploadFormData] = useState({
    file: "",
    title: "",
    author: "",
    genre: ""
  });


  const handleDownload = (id) => {
    console.log('ID:', id);
    // Construct the download URL using the ID
    const downloadUrl = `http://192.168.100.100:8000/items/${id}`;

    // Open the download URL in a new tab/window to trigger the download
    window.open(downloadUrl, '_blank');

    // Log the download URL
    console.log('Download URL:', downloadUrl);

    // If there's an error opening the download URL, log the error
    window.onerror = function(message, url, lineNumber) {
      console.error('Error downloading file:', message, 'at', url, 'line', lineNumber);
    };
  };

  const fetchEntries = async () => {
    const response = await axios.get("http://192.168.100.100:8000/items/");
    setRetrievals(response.data)
    console.log('Retrievals:', response.data);
  };

  useEffect(() => {
    fetchEntries();
    // get token from local storage
    const auth_token = localStorage.getItem("auth_token");
    console.log("token is ", auth_token)
    const auth_token_type = localStorage.getItem("auth_token_type");
    console.log("token is ", auth_token_type)
    const user_rights = localStorage.getItem("user_rights")
    console.log("the rights are", user_rights)
    setUserRights(user_rights)
    console.log("userRights:", userRights);
    const token = auth_token_type + " " + auth_token;

    //  fetch data from get user api
    axios
      .get("http://192.168.100.100:8000/users/", {
        headers: { Authorization: token },
      })
      .then((response) => {
        console.log(response);
        setUser(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const onChangeForm = (fieldName, event) => {
    setUploadFormData(prevState => ({
      ...prevState,
      [fieldName]: event.target.value
    }));
  };

const onFileChange = (event) => {
  setUploadFormData(prevState => ({
    ...prevState,
    file: event.target.files[0]
  }));
};

const onSubmitForm = async () => {
  try {
    const formDataToSend = new FormData();
    formDataToSend.append('input_file', uploadFormData.file);
    formDataToSend.append('book_title', uploadFormData.title);
    formDataToSend.append('author', uploadFormData.author);
    formDataToSend.append('genre', uploadFormData.genre);

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    };

    const response = await axios.post('http://192.168.100.100:8000/items/', formDataToSend, config);
    console.log(response.data);
    // Handle success response
  } catch (error) {
    console.error('Error:', error);
    // Handle error response
  }
};


  const onClickHandler = (event) => {
    event.preventDefault();

    // remove token form local storage
    localStorage.removeItem("auth_token");
    localStorage.removeItem("auth_token_type");

    // notif
    toast("See You !", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });

    // reload page
    setTimeout(() => {
      window.location.reload();
    }, 1500);
  };

  return (
    <div className="bg-gray-200 font-sans h-screen w-full flex flex-col justify-center items-center wallpaper">
      {/* <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white">Welcome to the Majestic and Marvellous Library of the Magnanimous Magurean</h1>
      </div> */}
      <div className="card w-3/4 mx-auto custom-card shadow-xl hover:shadow rounded-lg">
        <div className="text-center mt-2 text-3xl font-medium">{user.name}</div>
        <div className="text-center mt-2 font-light text-sm">
          @{user.username}
        </div>
        <div className="text-center font-normal text-lg">{user.email}</div>
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-black">Free Library</h1>
        </div>
        <hr className="mt-4"></hr>
        <table className="table table-striped table-bordered table-hover w-full">
          <thead className="text-lg font-bold"> {/* Increase font size and make it bold */}
            <tr className="border">
              <th className="border px-4 py-2 text-center green-header">Book name</th>
              <th className="border px-4 py-2 text-center green-header">Author</th>
              <th className="border px-4 py-2 text-center green-header">Genre</th>
              <th className="border px-4 py-2 text-center green-header">Download</th>
              {/* Add more columns as needed */}
            </tr>
          </thead>
          <tbody>
            {retrievals.map((retrieval) => (
            <tr key={retrieval.id} className="border-b-2 border-b">
              <td className="border-l-2 border-r-2 border-t-2 border-gray-400 px-4 py-2 text-center">{retrieval.book_title}</td> {/* Add padding, border, and center text */}
              <td className="border-l-2 border-r-2 border-t-2 border-gray-400 px-4 py-2 text-center">{retrieval.author}</td> {/* Add padding, border, and center text */}
              <td className="border-l-2 border-r-2 border-t-2 border-gray-400 px-4 py-2 text-center">{retrieval.genre}</td> {/* Add padding, border, and center text */}
              <td className="border-l-2 border-r-2 border-t-2 border-gray-400 px-4 py-2 text-center">
                <button onClick={() => handleDownload(retrieval.file_id)} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                  Download
                </button>
              </td> {/* Add padding, border, and center text */}
            </tr>
          )) }
          </tbody>
        </table>
        <hr className="mt-4"></hr>
        <div className="flex p-2">
          <div className="w-full text-center">
            <button
              onClick={(event) => {
                onClickHandler(event);
              }}
              className="py-3 w-64 text-xl text-black outline-none bg-gray-50 hover:bg-gray-100 active:bg-gray-200"
            >
              Log out
            </button>
          </div>
        </div>
      </div>
      {/* Conditional rendering of the button */}
      {userRights === "true" && (
        <div className="card w-1/3 mx-auto custom-card shadow-xl hover:shadow rounded-lg">
          <div className="card-body text-center">
            <div className="form-group">
              <input
                type="file"
                accept=".pdf,.epub"
                placeholder="File"
                className="block text-sm py-2 px-3 rounded-lg w-96 border outline-none focus:ring focus:outline-none focus:ring-yellow-400 mx-auto"
                onChange={onFileChange}
              />
            </div>
            <div className="form-group">
              <input
                type="text"
                placeholder="Book Title"
                className="block text-sm py-2 px-3 rounded-lg w-96 border outline-none focus:ring focus:outline-none focus:ring-yellow-400 mx-auto"
                onChange={(event) => {
                  onChangeForm("title", event);
                }}
              />
            </div>
            <div className="form-group">
              <input
                type="text"
                placeholder="Book Author"
                className="block text-sm py-2 px-3 rounded-lg w-96 border outline-none focus:ring focus:outline-none focus:ring-yellow-400 mx-auto"
                onChange={(event) => {
                  onChangeForm("author", event);
                }}
              />
            </div>
            <div className="form-group">
              <input
                type="text"
                placeholder="Book Genre"
                className="block text-sm py-2 px-3 rounded-lg w-96 border outline-none focus:ring focus:outline-none focus:ring-yellow-400 mx-auto"
                onChange={(event) => {
                  onChangeForm("genre", event);
                }}
              />
            </div>
            <button
              onClick={onSubmitForm}
              className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Upload
            </button>
          </div>
      </div>
      )}
  </div>
);

}
