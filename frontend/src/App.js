import "./App.css";
import Navbar from "./components/Navbar/Navbar";
import Body from "./components/body/Body";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Footer from "./components/Footer/Footer";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route
            path="/hello"
            element={
              <>
                <p>Hello world</p>
              </>
            }
          />
        </Routes>
        <Navbar />
        <Body />
        <Footer />
      </BrowserRouter>
    </>
  );
}

export default App;
