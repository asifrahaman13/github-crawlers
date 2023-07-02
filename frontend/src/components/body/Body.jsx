import React, { useState } from "react";
import axios from "axios";
import Select from "react-select";

const Body = () => {
  const [selectedOption, setSelectedOption] = useState(null);

  const handleSelect = (option) => {
    setSelectedOption(option);
    setUser((prevUser) => ({ ...prevUser, service: option.value }));
  };
 
  // Define the options available to the user for the services
  const options = [
    {
      value: "chroma_service",
      label: "chroma (open sources) Less accurate but takes lesser time.",
    },
    {
      value: "pinecone_service",
      label:
        "pinecone (Peripheral Software service)-More accurate but takes more time.",
    },
  ];

  // Define all the states.
  const [needemail, setNeedemail] = useState(false);

  // Control the inoputs by the user.
  const [user, setUser] = useState({
    username: "",
    email: "",
    service: "",
  });
  // Other states 
  const [submitted, setIsSubmitted] = useState(false);
  const [msg, setMsg] = useState("");
  const [linktorepo, setLinktorepo] = useState("");
  const [reasons, setReasons] = useState("");

  const handleChange = (e) => {
    setUser((prevState) => ({
      ...prevState,
      [e.target.name]: e.target.value,
    }));
  };
 
  // Handle waht happens when the user clicks on the submit button.
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("https://final-github-backend.onrender.com/postdata", {
        username: user.username,
        email_id: user.email,
        service: user.service,
      });
      // Status is equal to 200 if the request is successful 
      if (response.status == 200) {
        setIsSubmitted(true);
      }
      setMsg(response.data.response1);
      setLinktorepo(
        `https://github.com/${
          user.username
        }/${response.data.response1.substring(7)}`
      );
      setReasons(response.data.response2);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <section className="text-gray-600 body-font relative">
        <div className="container px-5 py-24 mx-auto">
          <div className="flex flex-col text-center w-full mb-12">
            <h1 className="sm:text-3xl text-2xl font-medium title-font mb-4">
              🔥🔥🔥 GET THE MOST COMPLEX REPOSITORY INFORMATION 🔥🔥🔥
            </h1>
            <p className="lg:w-2/3 mx-auto leading-relaxed text-base">
              We will crawl through all the repositories and codebases of the
              person and tell you the most complex codebased among them. However
              since the amount of codebase can be significantly long we may take
              some time. Typically it may take around 10-15 min. or longer.
              <p className="text-green-500">
           ~ If you want personalized email of the result we got you covered. Click on the button "CLICK FOR EMAIL"  ~
              </p>
            </p>
          </div>
          <div className="lg:w-1/2 md:w-2/3 mx-auto">
            <div className="flex flex-wrap -m-2">
              <div className="p-2 w-full">
                <div className="relative">
                  <label
                    htmlFor="name"
                    className="leading-7 text-sm text-gray-600"
                  >
                    ENTER THE USERNAME HERE
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="username"
                    onChange={(e) => handleChange(e)}
                    placeholder="tomjohnson67"
                    className="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                  />
                </div>
                {needemail && (
                  <div className="relative my-10">
                    <label
                      htmlFor="name"
                      className="leading-7 text-sm text-gray-600"
                    >
                      ENTER YOUR EMAIL HERE
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="email"
                      onChange={(e) => handleChange(e)}
                      placeholder="jonathon@gamil.com"
                      className="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                    />
                  </div>
                )}
                <div className="relative">
                  <label
                    htmlFor="name"
                    className="leading-7 text-sm text-gray-600"
                  >
                    ENTER THE USERNAME HERE
                  </label>
                  <div className="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out">
                    <Select
                      id="name"
                      name="service"
                      options={options}
                      value={selectedOption}
                      onChange={handleSelect}
                      isSearchable
                      placeholder="Select an option"
                    />
                  </div>
                </div>
              </div>

              <div className="p-2 w-full">
                <button
                  className="flex mx-auto text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg"
                  onClick={(e) => {
                    handleSubmit(e);
                  }}
                >
                  CLICK HERE
                </button>

                {!needemail && (
                  <button
                    className="flex mx-auto mt-16 text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg"
                    onClick={(e) => {
                      setNeedemail(true);
                    }}
                  >
                    CLICK FOR EMAIL
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {!submitted && (
        <section className="text-gray-600 body-font bg-gradient-to-r ">
          <div className="container px-5 mx-auto ">
            <div className="flex flex-wrap -m-4">
              <div className="p-4 lg:w-full">
                <div className="h-full bg-gray-100 bg-opacity-75 px-8 pt-16 pb-24 rounded-lg overflow-hidden text-center relative">
                  <h2 className="tracking-widest text-xs title-font font-medium text-gray-400 mb-1">
                    GREETINGS!😊😊😊
                  </h2>
                  <h1 className="title-font sm:text-2xl text-xl font-medium text-gray-900 mb-3">
                    Your response and analysis will appear here
                  </h1>
                  <p className="leading-relaxed mb-3">
                    Thank you for visiting our site. Please enter the Username
                    of the target user and we would fetch the most complex
                    repository for you.
                    <br />
                    Note that since we would crawl through the entire codebase
                    it may take some time.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}


      {submitted && (
        <section className="text-gray-600 body-font ">
          <div className="container px-5 py-24 mx-auto">
            <div className="text-center mb-20">
              <h1 className="sm:text-3xl text-2xl font-medium title-font text-gray-800 mb-4">
                Analysis
              </h1>
              <div className="flex mt-6 justify-center">
                <div className="w-16 h-1 rounded-full bg-indigo-500 inline-flex"></div>
              </div>
            </div>
            <div className="flex flex-wrap sm:-m-4 -mx-4 -mb-10 -mt-4 md:space-y-0 space-y-6">
              <div className="p-4 md:w-1/2 flex flex-col text-center items-center">
                <div className="w-20 h-20 inline-flex items-center justify-center rounded-full bg-indigo-100 text-indigo-500 mb-5 flex-shrink-0">
                  <svg
                    fill="none"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    className="w-10 h-10"
                    viewBox="0 0 24 24"
                  >
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                  </svg>
                </div>
                <div className="flex-grow">
                  <h2 className="text-base title-font font-medium mb-3 italic">
                    MOST COMPLEX REPOSITORY
                  </h2>
                  <p className="leading-relaxed text-lg font-bold">
                    {msg.substring(7)}
                  </p>
                  <h2 classNameName="mt-10 font-bold text-gray-100">Link:</h2>
                  <a className="mt-3 text-indigo-500 inline-flex items-center">
                    {linktorepo}
                    <svg
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="w-4 h-4 ml-2"
                      viewBox="0 0 24 24"
                    >
                      <path d="M5 12h14M12 5l7 7-7 7"></path>
                    </svg>
                  </a>
                </div>
              </div>
              <div className="p-4 md:w-1/2 flex flex-col text-center items-center">
                <div className="w-20 h-20 inline-flex items-center justify-center rounded-full bg-indigo-100 text-indigo-500 mb-5 flex-shrink-0">
                  <svg
                    fill="none"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    className="w-10 h-10"
                    viewBox="0 0 24 24"
                  >
                    <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <div className="flex-grow">
                  <h2 className="text-base title-font font-medium mb-3 italic">
                    REASON
                  </h2>
                  <p className="leading-relaxed text-base">{reasons}</p>
                  <h2 classNameName="mt-10 font-bold">Here is the link:</h2>
                  <a
                    className="mt-3 text-indigo-500 inline-flex items-center"
                    href={linktorepo}
                  >
                    {linktorepo}
                    <svg
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="w-4 h-4 ml-2"
                      viewBox="0 0 24 24"
                    >
                      <path d="M5 12h14M12 5l7 7-7 7"></path>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
          <button
            className="flex mx-auto mt-16 text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg"
            onClick={(e) => {
              setIsSubmitted(false);
            }}
          >
            CLEAR RESPONSE
          </button>{" "}
        </section>
      )}
    </>
  );
};

export default Body;
