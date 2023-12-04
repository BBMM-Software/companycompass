import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.scss";
import { Layout } from "./layout/Layout";
import { Homepage } from "./pages/Homepage/Homepage";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<Layout />} path="/">
                    <Route index element={<Homepage />}  />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
