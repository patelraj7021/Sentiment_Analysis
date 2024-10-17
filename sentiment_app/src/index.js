import App from "./components/App";
import { createRoot } from "react-dom/client";
import React from "react";

const domNode = document.getElementById("app");
const root = createRoot(domNode);
root.render(<App />);
